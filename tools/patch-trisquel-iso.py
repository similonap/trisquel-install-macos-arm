#!/usr/bin/env python3
"""Pre-patch a Trisquel/Debian installer ISO to work around the debootstrap
SHA512 checksum bug.

Background
----------
A few packages in the Trisquel archive (bash among them) carry no SHA512 field
in the Packages file.  pkgdetails then hands debootstrap the SHA512 of the
*previous* stanza and the download of such a package fails with a checksum
mismatch.  Every package does have a SHA256, so debootstrap has to be pinned to
SHA256 by changing SHA_SIZE=512 to SHA_SIZE=256 in
/usr/share/debootstrap/functions.

That file is not on the ISO: it arrives with the debootstrap-udeb that anna
fetches from the mirror during the install.  So instead of editing a file, this
script adds one startup script to the installer's initrd.  It runs at installer
startup and watches for /usr/share/debootstrap/functions to appear, then
rewrites that line -- long before the base system step needs it.

Usage
-----
    ./patch-trisquel-iso.py trisquel-netinst_12.0_arm64.iso
    ./patch-trisquel-iso.py in.iso -o out.iso
    ./patch-trisquel-iso.py --check some.iso

Needs python3 and xorriso (brew install xorriso / apt install xorriso), no root.
Works on any d-i based ISO: it finds every initrd in the image, patches each
distinct one, and rebuilds the ISO reproducing its original boot layout.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time

HOOK_PATH = "usr/lib/debian-installer-startup.d/S99debootstrap-sha256"

HOOK = b"""#!/bin/sh
# Work around the debootstrap checksum bug seen on Trisquel ecne.
#
# A few packages in the Trisquel archive (bash among them) carry no SHA512
# field in the Packages file.  pkgdetails then hands debootstrap the SHA512 of
# the *previous* stanza, and the download of such a package fails with a
# checksum mismatch.  Every package does have a SHA256, so pin debootstrap to
# SHA256 instead.
#
# /usr/share/debootstrap/functions only appears once anna has installed
# debootstrap-udeb, which happens well after this script runs, so watch for
# the file in the background and patch it as soon as it settles.

F=/usr/share/debootstrap/functions

(
\tprev=""
\twhile true; do
\t\tif [ -f "$F" ]; then
\t\t\tsize="$(wc -c < "$F")"
\t\t\tif [ "$size" = "$prev" ] && grep -q 'SHA_SIZE=512' "$F"; then
\t\t\t\tif sed 's/SHA_SIZE=512/SHA_SIZE=256/' "$F" > "$F.sha256" &&
\t\t\t\t   cat "$F.sha256" > "$F"; then
\t\t\t\t\tlogger -t debootstrap-sha256 "patched $F to use SHA256"
\t\t\t\telse
\t\t\t\t\tlogger -t debootstrap-sha256 "failed to patch $F"
\t\t\t\tfi
\t\t\t\trm -f "$F.sha256"
\t\t\tfi
\t\t\tprev="$size"
\t\tfi
\t\tsleep 2
\tdone
) < /dev/null > /dev/null 2>&1 &
"""


# --------------------------------------------------------------- newc cpio --

MAGIC = b"070701"
HDR = 110


def pad4(n):
    return (4 - n % 4) % 4


def _fields(buf, off):
    vals = [int(buf[off + 6 + i * 8: off + 14 + i * 8], 16) for i in range(13)]
    ino, mode, uid, gid, nlink, mtime, size, _, _, _, _, nsize, _ = vals
    return ino, size, nsize


def walk(data):
    """Yield (offset, name, ino) for every entry of every archive in data.

    Handles several cpio archives concatenated into one blob, which is what a
    kernel accepts as an initramfs.
    """
    off = 0
    end = len(data)
    while off < end:
        if data[off:off + 6] != MAGIC:
            # Zero padding between archives, or trailing slack: skip it.
            if data[off] == 0:
                off += 1
                continue
            raise ValueError("not a newc cpio archive at offset %d" % off)
        ino, size, nsize = _fields(data, off)
        name = data[off + HDR: off + HDR + nsize - 1].decode("utf-8", "replace")
        yield off, name, ino
        off += HDR + nsize
        off += pad4(off)
        off += size
        off += pad4(off)


def contains(data, path):
    return any(name == path for _, name, _ in walk(data))


def header(path, data, mode, ino):
    name = path.encode() + b"\0"
    f = [ino, mode, 0, 0, 1, 0, len(data), 0, 0, 0, 0, len(name), 0]
    return MAGIC + b"".join(b"%08X" % v for v in f) + name


def insert(data, entries):
    """Insert entries just before the final TRAILER!!! of the last archive."""
    last_trailer = None
    max_ino = 0
    for off, name, ino in walk(data):
        max_ino = max(max_ino, ino)
        if name == "TRAILER!!!":
            last_trailer = off
    if last_trailer is None:
        raise ValueError("no TRAILER!!! entry found in cpio archive")

    out = bytearray(data[:last_trailer])
    ino = max_ino + 1
    for path, mode, blob in entries:
        out += header(path, blob, mode, ino)
        out += b"\0" * pad4(len(out))
        out += blob
        out += b"\0" * pad4(len(out))
        ino += 1
    out += header("TRAILER!!!", b"", 0, 0)
    out += b"\0" * pad4(len(out))
    out += b"\0" * ((512 - len(out) % 512) % 512)  # cpio pads to 512 blocks
    return bytes(out)


# --------------------------------------------------------------- squeezing --

def sniff(blob):
    if blob[:2] == b"\x1f\x8b":
        return "gzip"
    if blob[:6] == b"\xfd7zXZ\x00":
        return "xz"
    if blob[:4] == b"\x28\xb5\x2f\xfd":
        return "zstd"
    if blob[:6] == MAGIC:
        return "none"
    if blob[:3] == b"BZh":
        return "bzip2"
    if blob[:4] == b"\x04\x22\x4d\x18":
        return "lz4"
    if blob[:3] == b"\x89LZ":
        return "lzo"
    return "unknown"


def _cli(cmd, blob):
    if shutil.which(cmd[0]) is None:
        raise SystemExit("error: %s is needed for this initrd but is not "
                         "installed" % cmd[0])
    return subprocess.run(cmd, input=blob, stdout=subprocess.PIPE,
                          check=True).stdout


def decompress(blob, kind):
    if kind == "none":
        return blob
    if kind == "gzip":
        import gzip
        return gzip.decompress(blob)
    if kind == "xz":
        import lzma
        return lzma.decompress(blob)
    if kind == "zstd":
        try:
            from compression import zstd  # python >= 3.14
            return zstd.decompress(blob)
        except ImportError:
            return _cli(["zstd", "-d", "-c"], blob)
    raise SystemExit("error: unsupported initrd compression: %s" % kind)


def compress(blob, kind):
    if kind == "none":
        return blob
    if kind == "gzip":
        import gzip
        return gzip.compress(blob, compresslevel=9, mtime=0)
    if kind == "xz":
        import lzma
        # The kernel's xz decompressor only guarantees CRC32.
        return lzma.compress(blob, format=lzma.FORMAT_XZ, preset=9,
                             check=lzma.CHECK_CRC32)
    if kind == "zstd":
        try:
            from compression import zstd  # python >= 3.14
            return zstd.compress(blob, level=19)
        except ImportError:
            return _cli(["zstd", "-19", "-T0", "-c"], blob)
    raise SystemExit("error: unsupported initrd compression: %s" % kind)


def split_prefix(blob):
    """Split an initrd into (uncompressed leading archives, remainder).

    Some initrds start with a plain cpio archive (CPU microcode, and such)
    followed by the compressed main archive.  Only the remainder gets patched.
    """
    if blob[:6] != MAGIC:
        return b"", blob
    off = 0
    end = len(blob)
    while off < end and blob[off:off + 6] == MAGIC:
        _, size, nsize = _fields(blob, off)
        name = blob[off + HDR: off + HDR + nsize - 1]
        off += HDR + nsize
        off += pad4(off)
        off += size
        off += pad4(off)
        if name == b"TRAILER!!!":
            while off < end and blob[off] == 0:
                off += 1
            if off < end and blob[off:off + 6] != MAGIC:
                return blob[:off], blob[off:]  # compressed part follows
    return b"", blob


# ------------------------------------------------------------------ xorriso --

def xorriso(args, what):
    proc = subprocess.run(["xorriso"] + args, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        raise SystemExit("error: xorriso failed while %s" % what)
    return proc.stdout


def iso_find(iso, pattern):
    out = xorriso(["-indev", iso, "-find", "/", "-name", pattern, "-type", "f"],
                  "listing %s" % iso)
    paths = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("'") and line.endswith("'"):
            paths.append(line[1:-1])
    return sorted(paths)


def iso_extract(iso, iso_path, dest):
    xorriso(["-osirrox", "on:auto_chmod_on", "-indev", iso,
             "-extract", iso_path, dest], "extracting %s" % iso_path)
    os.chmod(dest, 0o644)
    return dest


def has_el_torito(iso):
    out = xorriso(["-indev", iso, "-report_el_torito", "plain"],
                  "reading boot info of %s" % iso)
    return "El Torito images" in out


def boot_report(iso):
    out = xorriso(["-indev", iso, "-report_el_torito", "plain",
                   "-report_system_area", "plain"],
                  "reading boot info of %s" % iso)
    keep = ("Boot record", "El Torito cat path", "El Torito img path",
            "System area summary", "MBR partition ")
    return [l.strip() for l in out.splitlines() if l.startswith(keep)]


# ---------------------------------------------------------------- patching --

def patch_initrd(blob):
    """Return (new blob, note).  Note is None when it was already patched."""
    prefix, body = split_prefix(blob)
    kind = sniff(body)
    if kind in ("unknown", "bzip2", "lz4", "lzo"):
        raise SystemExit("error: unsupported initrd format (%s)" % kind)
    cpio = decompress(body, kind)
    if contains(cpio, HOOK_PATH):
        return blob, None
    cpio = insert(cpio, [(HOOK_PATH, 0o100755, HOOK)])
    return prefix + compress(cpio, kind), kind


def rmtree(path):
    """rmtree, but files restored from an ISO come out read-only."""
    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            try:
                os.chmod(os.path.join(root, name), 0o700)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check(iso):
    paths = iso_find(iso, "initrd*")
    if not paths:
        raise SystemExit("error: no initrd found in %s" % iso)
    tmp = tempfile.mkdtemp(prefix="isocheck-")
    try:
        rc = 0
        for i, p in enumerate(paths):
            local = iso_extract(iso, p, os.path.join(tmp, "i%d" % i))
            with open(local, "rb") as fh:
                _, body = split_prefix(fh.read())
            cpio = decompress(body, sniff(body))
            ok = contains(cpio, HOOK_PATH)
            print("%-28s %s" % (p, "patched" if ok else "NOT patched"))
            rc |= 0 if ok else 1
        return rc
    finally:
        rmtree(tmp)


def main():
    ap = argparse.ArgumentParser(
        description="Pre-patch a Trisquel/Debian installer ISO so debootstrap "
                    "verifies packages with SHA256 instead of SHA512.")
    ap.add_argument("iso", help="input ISO")
    ap.add_argument("-o", "--output", help="output ISO "
                    "(default: <input>-sha256.iso)")
    ap.add_argument("-f", "--force", action="store_true",
                    help="overwrite the output if it exists")
    ap.add_argument("--check", action="store_true",
                    help="only report whether the ISO is already patched")
    args = ap.parse_args()

    if shutil.which("xorriso") is None:
        raise SystemExit("error: xorriso is not installed "
                         "(brew install xorriso / apt install xorriso)")
    if not os.path.isfile(args.iso):
        raise SystemExit("error: no such file: %s" % args.iso)

    if args.check:
        sys.exit(check(args.iso))

    out = args.output
    if out is None:
        stem, ext = os.path.splitext(args.iso)
        out = stem + "-sha256" + (ext or ".iso")
    if os.path.exists(out) and not args.force:
        raise SystemExit("error: %s exists (use --force to overwrite)" % out)

    started = time.time()
    tmp = tempfile.mkdtemp(prefix="isopatch-")
    try:
        paths = iso_find(args.iso, "initrd*")
        if not paths:
            raise SystemExit("error: no initrd found in %s -- is this an "
                             "installer ISO?" % args.iso)
        print("initrds found: %s" % ", ".join(paths))

        # Several ISO paths often share one initrd; patch each distinct one once.
        by_digest = {}
        for i, p in enumerate(paths):
            local = iso_extract(args.iso, p, os.path.join(tmp, "in%d" % i))
            by_digest.setdefault(sha256(local), []).append((p, local))

        mapping = []
        for n, (digest, group) in enumerate(sorted(by_digest.items())):
            names = ", ".join(p for p, _ in group)
            _, local = group[0]
            with open(local, "rb") as fh:
                blob = fh.read()
            print("patching %s (%.1f MiB)..." % (names, len(blob) / 2**20))
            new, kind = patch_initrd(blob)
            if kind is None:
                print("  already patched, leaving it alone")
                continue
            new_local = os.path.join(tmp, "out%d" % n)
            with open(new_local, "wb") as fh:
                fh.write(new)
            print("  added /%s, recompressed (%s), %d -> %d bytes"
                  % (HOOK_PATH, kind, len(blob), len(new)))
            for p, _ in group:
                mapping.append((new_local, p))

        if not mapping:
            raise SystemExit("nothing to do: %s is already patched" % args.iso)

        print("building %s..." % out)
        cmd = ["-indev", args.iso, "-outdev", out, "-hardlinks", "on"]
        if has_el_torito(args.iso):
            cmd += ["-boot_image", "any", "replay"]
        else:
            print("  note: no El Torito boot record found, not replaying one")
        for local, iso_path in mapping:
            cmd += ["-map", local, iso_path]
        xorriso(cmd + ["-commit"], "writing %s" % out)

        print("verifying...")
        for i, (local, iso_path) in enumerate(mapping):
            got = iso_extract(out, iso_path, os.path.join(tmp, "chk%d" % i))
            if sha256(got) != sha256(local):
                raise SystemExit("error: %s in the new ISO does not match the "
                                 "patched initrd" % iso_path)
            print("  %s ok" % iso_path)
        before, after = boot_report(args.iso), boot_report(out)
        if before != after:
            print("  warning: boot layout differs from the original:")
            for line in after:
                if line not in before:
                    print("    %s" % line)
        else:
            print("  boot layout matches the original")
    finally:
        rmtree(tmp)

    print("\ndone in %d s: %s" % (time.time() - started, out))
    print("sha256: %s" % sha256(out))
    print("\nDuring the install, tty4 (ctrl-alt-f4) will show\n"
          "  debootstrap-sha256: patched /usr/share/debootstrap/functions ...\n"
          "once anna has fetched debootstrap-udeb.")


if __name__ == "__main__":
    main()
