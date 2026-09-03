# Trisquel (macOS)

*Read this in another language: [Nederlands](README.md) · **English***

## Which iso should I download?

To install Trisquel in a virtual machine with VirtualBox on macOS, you first need to know what kind of Mac you are using. You either have an older Intel Mac, or a more recent model with Apple Silicon. You can check this quickly by running this command in the macOS terminal:

```
uname -m
```

If the output is:

```
arm64
```

then you have a Mac with an Apple Silicon chip. That processor uses a different architecture than most common PCs (`x86_64`). Because of this you also need to download an adapted version of Trisquel. In theory macOS can emulate `x86_64` systems, but that is slow and unstable. So make sure you download the right installation file right away using this link:

[Download Trisquel 12.0 ARM64 Netinst ISO](https://cdimage.trisquel.info/trisquel-images/trisquel-netinst_12.0_arm64.iso)

Still working on an Intel Mac (`x86_64`)? Then you simply use the standard iso from the general Windows instructions. In the rest of this guide we focus entirely on `arm64`, since virtually every modern Mac runs on it.

## Installing VirtualBox

Download VirtualBox from the [VirtualBox download page](https://www.virtualbox.org/wiki/Downloads). On that page, choose `macOS / Apple Silicon hosts`.

## Setting up a new virtual machine

Once VirtualBox is on your system, you create a new VM in almost exactly the same way as on Windows.

Give the virtual machine a clear name (such as `Trisquel Linux`) and select the file you just downloaded under `ISO Image`. VirtualBox does not recognise the ARM64 iso automatically and reports that the operating system could not be detected. That is expected. So set it manually: choose `Linux` for `OS`, `Ubuntu` for `OS Distribution` and `Ubuntu (ARM 64-bit)` for `OS Version`. After all, Trisquel uses Ubuntu as its foundation.

![New virtual machine: name, iso and operating system](01-nieuwe-vm-naam-en-besturingssysteem.png)

In the next step you assign the desired computing power. With 2048 MB RAM, 2 CPU cores and a 38 GB virtual disk you have more than enough. Be sure to tick the `Use EFI` option: without EFI an ARM64 environment simply refuses to boot.

![Configuring the virtual hardware](02-virtuele-hardware-instellen.png)

Review the summary and finish with `Finish`.

![Summary of the new virtual machine](03-samenvatting-nieuwe-vm.png)

Open the settings of your new machine right away, go to the `Display` tab and set the video memory to 64 MB (not required, but everything will run more smoothly).

![Settings: video memory set to 64 MB](04-instellingen-display-videogeheugen.png)

Your VM is now ready in the VirtualBox Manager with the status `Powered Off`. Select the machine and click `Start` to begin the installation procedure.

![The virtual machine is ready in the VirtualBox Manager](05-virtualbox-manager-vm-powered-off.png)

## The installation

The setup of the `arm64` version differs noticeably from the regular `x86_64` disk image. For ARM devices there is no uniform boot standard, which is why the developers opted for a compact network installation (`netinst`). This type of installer only downloads the required components at the moment the process asks for them. The initial download stays small, but a reliable internet connection is therefore strictly necessary. On top of that, the installation wizard does not use a mouse-driven GUI, but a text menu.

### Booting

At startup the GRUB boot menu appears. Don't be alarmed if the window opens tiny: you can simply drag it larger with the mouse, and the display should scale along.

![The GRUB menu at startup](06-grub-menu-install.png)

Use the arrow keys to move to `Install` and press `Enter` to begin.

![Install selected in GRUB](07-grub-install-geselecteerd.png)

> **Tip:** In this interface you switch fields with the `Tab` key. You tick or untick options with the space bar, make choices with the arrow keys and confirm with `Enter`. The mouse pointer does nothing for now.

### Language, location and keyboard

First choose the language for the installation process. This setting immediately determines the system language of your Linux installation. Select `English` here.

![Selecting the language: English](09-taal-selecteren-english.png)

Next, specify your location so the time zone is set correctly. Since we chose English, the list mainly shows English-speaking countries. Choose `other` at the bottom.

![Selecting the location: other](10-locatie-selecteren-other.png)

Then select the continent `Europe`.

![Selecting the continent: Europe](11-continent-selecteren-europe.png)

Scroll down and choose `Belgium`.

![Selecting the country: Belgium](12-land-selecteren-belgium.png)

There is no official default combination for English within the Belgian locale settings. The installer therefore proposes falling back to `United States - en_US.UTF-8`. Confirm that selection.

![Setting the locale: en_US.UTF-8](13-locale-instellen-en-us-utf8.png)

For the keyboard, always choose the layout of your physical keyboard, not blindly what you see in the example screenshots. The images show `Belgian` because that Mac has a Belgian AZERTY keyboard. If you work with a QWERTY model (on many Apple laptops that is `English (US)`), select that layout instead. A mistake here causes wrong characters later on, which leads to unpleasant surprises especially when entering your password.

![Keyboard country: Belgian](14-toetsenbord-land-belgian.png)

For the variant, simply choose the standard layout (such as `Belgian`) and avoid the other sub-variants.

![Keyboard layout: Belgian](15-toetsenbord-layout-belgian.png)

### Network

Trisquel now configures network access. For the `hostname` you can safely keep the default value `trisquel`, or use something else.

![Hostname: trisquel](16-hostname-trisquel.png)

Leave the domain name field empty. Continue right away with `Continue`.

![Leaving the domain name empty](17-domeinnaam-leeg-laten.png)

### Mirror and proxy

Because we are working with a network installer, the system needs to know which server the installation files are fetched from. Preferably choose a server that is geographically close, such as `Germany`.

![Mirror country: Germany](18-mirror-land-germany.png)

Then select a specific server.

![Selecting a mirror](19-mirror-selecteren.png)

You can simply leave the HTTP proxy field empty. Neither at home nor on a standard school network do you need this.

![Leaving the HTTP proxy empty](20-http-proxy-leeg-laten.png)

The installer now pulls in the missing components from the server. This takes some time and requires a stable connection.

![Extra components are being downloaded](21-extra-componenten-laden-15procent.png)

![Extra components are being downloaded](22-extra-componenten-laden-36procent.png)

### User and password

Now create your own user account. You use this account for daily tasks instead of the root user. First fill in your full name.

![Full name of the new user](23-volledige-naam-nieuwe-gebruiker.png)

Just type your own name here. Based on that, the system immediately suggests a sensible username.

![Full name filled in](24-volledige-naam-andie-ingevuld.png)

Then enter a decent password. Use your student number for this (e.g. s123456).

![Choosing a password](25-wachtwoord-kiezen.png)

Pay very close attention to your keyboard layout here. If you chose the wrong layout a few steps back, characters and digits will not match what you see on your keys. Use the space bar to tick the `Show Password in Clear` option so that your password appears on screen as plain text. Check whether the letters match what you type. If you notice differences, use `Go Back` to return to the keyboard step and correct it.

![Password filled in](26-wachtwoord-ingevuld.png)

Confirm your chosen password by typing it once more.

![Confirming the password](27-wachtwoord-bevestigen.png)

Because your student number is shorter than 8 characters, you get a warning that you are using a weak password. That is correct, but you may ignore it for now.

![Using the weak password anyway](28-zwak-wachtwoord-gebruiken.png)

### Partitioning the disk

Time to prepare the virtual hard disk. Choose the option `Guided - use entire disk and set up LVM`. The installer then arranges the layout by itself and immediately adds Logical Volume Management, which makes resizing your volumes easier afterwards.

![Partitioning method: guided with LVM](29-partitioneermethode-guided-lvm.png)

There is only one virtual storage medium in the list, for example `SCSI1 (0,0,0) (sda) - 40.8 GB VBOX HARDDISK`. So you cannot overwrite or erase any physical partitions of your own Mac.

![Selecting the disk: sda](30-schijf-selecteren-sda.png)

Then select `All files in one partition (recommended for new users)`.

![Partitioning scheme: all files in one partition](31-partitieschema-alles-in-een-partitie.png)

Give permission to modify the partition table by choosing `Yes`.

![Writing the changes and configuring LVM](32-wijzigingen-schrijven-en-lvm-configureren.png)

Accept the proposed size for the volume group (about 38.7 GB) and continue with `Continue`.

![Size of the volume group](33-grootte-volume-group-38gb.png)

The system now shows a final overview with a root volume, swap partition and boot partition. This is the last step where you can still abort without consequences. Select `Yes` to set up the disk definitively.

![Writing the changes to disk for good](34-wijzigingen-naar-schijf-schrijven.png)

### Installing the system

The base operating system is now written to the virtual disk.

![The base system is being installed](35-basissysteem-installeren.png)

Next the installer configures the package manager `apt`, so the system can fetch future software.

![apt is being configured](36-apt-configureren.png)

The first set of files is downloaded and installed.

![Software is downloaded and installed](37-software-selecteren-en-installeren.png)

After this the system asks which software packages you want to include right away. So far the machine only has a minimal Linux installation, without a graphical interface. Use the space bar to tick only `Trisquel desktop environment` and leave the other options empty. Press `Tab` to navigate to `Continue` and press `Enter`. Take a short break here: downloading the full desktop environment takes a while.

![Software selection: Trisquel desktop environment](38-softwareselectie-trisquel-desktop-environment.png)

To finish, the wizard installs the GRUB bootloader, so your virtual machine boots on its own.

![The GRUB bootloader is being installed](39-grub-bootloader-installeren.png)

As soon as the message `Installation complete` appears, finish with `Continue` to restart the system.

![Installation complete](40-installatie-voltooid-herstarten.png)

## Booting for the first time

Trisquel now boots into its own graphical boot screen.

![The Trisquel boot screen](41-trisquel-opstartscherm.png)

After that you end up at the login screen. Click your account name, type your password and press `Log In`.

![Login screen](42-inlogscherm-andie.png)

Does the system refuse your password? Then your keyboard layout is almost certainly set incorrectly. At the top right of the login screen you can force a different keyboard layout using the language button (often labelled `en`). If needed, type your password in the username field first to visually check which characters actually appear on screen.

## Installing the Guest Additions

The graphical interface works, but for now the window is stuck at a low resolution and clipboard integration is still missing. You fix this by installing the *Guest Additions*: a bundle of drivers that run inside the guest system.

First detach the installation file, otherwise the virtual machine may start the installation wizard again. In the VirtualBox window, go to `Devices` > `Optical Drives` > `Remove Disk From Virtual Drive`.

![Removing the iso from the virtual drive](43-devices-schijf-verwijderen-uit-virtueel-station.png)

In this same menu you recognise active disks by the check mark next to them.

![The Optical Drives submenu shows the current disk](48-devices-optical-drives-submenu.png)

To be able to compile these drivers you need development tools and up-to-date kernel headers. Start a terminal window via `Applications` > `Accessories` > `MATE Terminal`.

![Opening a terminal via the menu](46-mate-terminal-openen-via-menu.png)

Run the following instructions:

```
sudo apt update
sudo apt upgrade
sudo apt install gcc make tree # Optional
sudo apt install build-essential dkms linux-headers-$(uname -r)
```

![Installing the required packages](45-terminal-build-essential-dkms-linux-headers.png)

If these packages are already installed, `apt` simply reports that everything is up to date and you don't have to do anything else.

Now virtually attach the disk image with the Guest Additions via `Devices` > `Insert Guest Additions CD image...`.

![Inserting the Guest Additions cd](49-guest-additions-cd-image-invoegen.png)

Note: this action only puts the virtual cd in the tray. Trisquel does not start anything automatically and does not mount the disk by itself. If you look in the `/media/cdrom` folder right away, there is nothing in it yet:

```
cd /media/cdrom
ls
```

![/media/cdrom is still empty](50-terminal-media-cdrom-is-leeg.png)

So mount the virtual disk manually yourself. Use the path `/media/cdrom` for this (the folder `/mnt/cdrom` does not exist by default):

```
cd ..
sudo mount /dev/cdrom /media/cdrom
```

The message `source write-protected, mounted read-only` makes perfect sense, because an optical disk is always read-only. On your desktop you will now also see a cd icon appear.

![Mounting the cd on /media/cdrom](51-cdrom-mounten-op-media-cdrom.png)

List the folder contents again to see the files on the disk:

```
cd /media/cdrom
ls
```

In the listing you will see `VBoxLinuxAdditions-arm64.run`. That is the file we are looking for. The version without `arm64` in the file name is meant for classic `x86_64` systems.

![The contents of the Guest Additions cd](52-inhoud-guest-additions-cd.png)

Run the script. Don't forget the `./` at the beginning, because without that addition Linux only searches the system folders and the script will not be found.

![The command without ./ does not work](53-guest-additions-commando-typen.png)

```
sudo ./VBoxLinuxAdditions-arm64.run
```

![Starting the installation of the Guest Additions](54-guest-additions-installatie-starten.png)

The script extracts the files and automatically builds the required modules for your active kernel. That takes a minute of patience. Notices such as `System running in EFI mode, skipping` and the message that you should log in again are purely informational and do not indicate problems.

![The Guest Additions have been installed](55-guest-additions-installatie-voltooid.png)

Restart your virtual machine afterwards to load the new drivers.

![Shutting down or restarting the virtual machine](56-systeem-afsluiten-dialoog.png)

## Shared clipboard and drag-and-drop

Thanks to the Guest Additions you can easily copy and paste between macOS and Trisquel, although you first have to enable that integration. Shut down your virtual machine completely so that it is `Powered Off`.

![The virtual machine is powered off](57-virtualbox-manager-vm-powered-off.png)

In VirtualBox, navigate to `Settings` > `General` > `Features` and set both `Shared Clipboard` and `Drag-and-Drop` to `Bidirectional`. Save with `OK` and start Trisquel again.

![Shared clipboard and drag-and-drop set to Bidirectional](58-instellingen-gedeeld-klembord-en-drag-and-drop.png)

From now on the Trisquel window adapts automatically when you drag its edges, and you can move text or files back and forth between macOS and your virtual machine without any trouble.
