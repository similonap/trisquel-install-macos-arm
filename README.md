# Trisquel (macOS)

*Lees dit in een andere taal: **Nederlands** · [English](README.en.md)*

## Welke iso moet ik downloaden?

Om Trisquel in een virtuele machine met VirtualBox te installeren op macOS, moet je eerst weten welk type Mac je gebruikt. Je hebt ofwel een oudere Intel-Mac, ofwel een recenter model met Apple Silicon. Dat controleer je snel door in de macOS-terminal dit commando uit te voeren:

```
uname -m
```

Krijg je als uitvoer:

```
arm64
```

dan heb je een Mac met een Apple Silicon-chip. Die processor heeft een andere architectuur dan de meeste gangbare pc's (`x86_64`). Daardoor moet je ook een aangepaste versie van Trisquel downloaden. macOS kan in theorie wel `x86_64`-systemen emuleren, maar dat werkt traag en instabiel. Zorg dus dat je meteen het juiste installatiebestand binnenhaalt via deze link:

[Download Trisquel 12.0 ARM64 Netinst ISO](https://cdimage.trisquel.info/trisquel-images/trisquel-netinst_12.0_arm64.iso)

Werk je toch nog op een Intel-Mac (`x86_64`)? Dan gebruik je gewoon de standaard iso uit de algemene instructies voor Windows. In de rest van deze handleiding focussen we volledig op `arm64`, aangezien vrijwel elke moderne Mac daarop draait.

## VirtualBox installeren

Download VirtualBox via de [VirtualBox Downloadpagina](https://www.virtualbox.org/wiki/Downloads). Kies op die pagina voor `macOS / Apple Silicon hosts`.

## Een nieuwe virtuele machine opzetten

Zodra VirtualBox op je systeem staat, maak je een nieuwe VM aan op nagenoeg dezelfde manier als onder Windows.

Geef de virtuele machine een duidelijke naam (zoals `Trisquel Linux`) en selecteer bij `ISO Image` het zojuist gedownloade bestand. VirtualBox herkent de ARM64-iso niet automatisch en meldt dat het besturingssysteem niet gedetecteerd kon worden. Dat hoort zo. Stel dit daarom handmatig in: kies `Linux` bij `OS`, `Ubuntu` bij `OS Distribution` en `Ubuntu (ARM 64-bit)` bij `OS Version`. Trisquel gebruikt Ubuntu immers als fundament.

![Nieuwe virtuele machine: naam, iso en besturingssysteem](01-nieuwe-vm-naam-en-besturingssysteem.png)

In de volgende stap wijs je de gewenste rekenkracht toe. Met 2048 MB RAM, 2 CPU-kernen en een virtuele schijf van 38 GB zit je ruim voldoende. Vink de optie `Use EFI` zeker aan: zonder EFI weigert een ARM64-omgeving simpelweg op te starten.

![Virtuele hardware instellen](02-virtuele-hardware-instellen.png)

Kijk het overzicht even na en rond af met `Finish`.

![Samenvatting van de nieuwe virtuele machine](03-samenvatting-nieuwe-vm.png)

Open meteen de instellingen van je nieuwe machine, ga naar het tabblad `Display` en zet het videogeheugen op 64 MB (niet verplicht, maar alles zal vlotter gaan)

![Instellingen: videogeheugen op 64 MB](04-instellingen-display-videogeheugen.png)

Je VM staat nu klaar in de VirtualBox Manager met de status `Powered Off`. Selecteer de machine en klik op `Start` om de installatieprocedure in gang te zetten.

![De virtuele machine staat klaar in de VirtualBox Manager](05-virtualbox-manager-vm-powered-off.png)

## De installatie

De setup van de `arm64`-versie verschilt merkbaar van het reguliere `x86_64`-schijfkopiebestand. Voor ARM-toestellen ontbreekt een uniforme opstartstandaard, waardoor ontwikkelaars gekozen hebben voor een compacte netwerkinstallatie (`netinst`). Dit type installer haalt benodigde onderdelen pas binnen op het moment dat het proces erom vraagt. De initiële download blijft zo compact, maar een betrouwbare internetverbinding is hierdoor strikt noodzakelijk. De installatiewizard werkt bovendien niet met een muisgestuurde GUI, maar met een tekstmenu.

### Opstarten

Bij de start verschijnt het GRUB-bootmenu. Schrik niet als het venster piepklein opent: je mag dit gewoon met de muis groter slepen, de weergave schaalt normaal gezien mee.

![Het GRUB-menu bij het opstarten](06-grub-menu-install.png)

Gebruik de pijltjestoetsen om naar `Install` te bladeren en druk op `Enter` om te beginnen.

![Install geselecteerd in GRUB](07-grub-install-geselecteerd.png)

> **Tip:** In deze interface wissel je van veld met de `Tab`-toets. Opties aan- of uitvinken doe je met de spatiebalk, keuzes maken met de pijltjestoetsen en bevestigen met `Enter`. De muisaanwijzer doet voorlopig nog niets.

### Taal, locatie en toetsenbord

Kies allereerst de taal voor het installatieproces. Deze instelling bepaalt meteen de systeem taal van je linux installatie. Selecteer hier `English`.

![Taal selecteren: English](09-taal-selecteren-english.png)

Geef vervolgens je locatie op om de tijdzone juist te zetten. Aangezien we voor Engels kozen, toont het overzicht hoofdzakelijk Engelstalige landen. Kies onderaan voor `other`.

![Locatie selecteren: other](10-locatie-selecteren-other.png)

Selecteer daarna het werelddeel `Europe`.

![Continent selecteren: Europe](11-continent-selecteren-europe.png)

Scroll naar beneden en kies `Belgium`.

![Land selecteren: Belgium](12-land-selecteren-belgium.png)

Er bestaat geen officiële standaardcombinatie voor het Engels binnen de Belgische landinstellingen. De installer stelt daarom voor om terug te vallen op `United States - en_US.UTF-8`. Bevestig die selectie.

![Locale instellen: en_US.UTF-8](13-locale-instellen-en-us-utf8.png)

Bij het toetsenbord kies je altijd de indeling van je fysieke toetsenbord, niet blindelings wat je op de voorbeeldscreenshots ziet. Op de afbeeldingen staat `Belgian` aangeduid omdat die Mac over een Belgisch AZERTY-toetsenbord beschikt. Werk je met een QWERTY-model (op veel Apple-laptops betreft dat `English (US)`), selecteer dan die layout. Een vergissing hier zorgt straks voor foutieve karakters, wat vooral bij het opgeven van je wachtwoord voor vervelende verrassingen zorgt.

![Toetsenbordland: Belgian](14-toetsenbord-land-belgian.png)

Kies bij de variant gewoon de standaardindeling (zoals `Belgian`) en vermijd de overige subvarianten.

![Toetsenbordlayout: Belgian](15-toetsenbord-layout-belgian.png)

### Netwerk

Trisquel configureert nu de netwerktoegang. Als `hostname` mag je gerust de standaardwaarde `trisquel` behouden of iets anders.

![Hostname: trisquel](16-hostname-trisquel.png)

Het veld voor de domeinnaam laat je leeg. Ga meteen door via `Continue`.

![Domeinnaam leeg laten](17-domeinnaam-leeg-laten.png)

### Mirror en proxy

Omdat we met een netwerkinstaller werken, moet het systeem weten vanaf welke server de installatiebestanden binnengehaald worden. Kies bij voorkeur een server die geografisch dichtbij staat, zoals `Germany`.

![Mirror-land: Germany](18-mirror-land-germany.png)

Selecteer daarna een specifieke server. 

![Een mirror selecteren](19-mirror-selecteren.png)

Het veld voor een HTTP-proxy mag je gewoon leeg laten. Zowel thuis als in een standaard schoolnetwerk heb je dit niet nodig.

![HTTP-proxy leeg laten](20-http-proxy-leeg-laten.png)

De installer trekt nu de ontbrekende onderdelen binnen vanaf de server. Dit neemt wat tijd in beslag en vraagt om een stabiele verbinding.

![Extra componenten worden gedownload](21-extra-componenten-laden-15procent.png)

![Extra componenten worden gedownload](22-extra-componenten-laden-36procent.png)

### Gebruiker en wachtwoord

Maak nu je eigen gebruikersaccount aan. Dit account gebruik je voor dagelijkse handelingen in plaats van de root-gebruiker. Vul eerst je volledige naam in.

![Volledige naam van de nieuwe gebruiker](23-volledige-naam-nieuwe-gebruiker.png)

Typ hier gewoon je eigen naam. Het systeem stelt op basis daarvan meteen een logische gebruikersnaam voor.

![Volledige naam ingevuld](24-volledige-naam-andie-ingevuld.png)

Voer daarna een degelijk wachtwoord in. Kies hiervoor je studentennummer (bv s123456).

![Een wachtwoord kiezen](25-wachtwoord-kiezen.png)

Let hier erg goed op je toetsenbordindeling. Als je een paar stappen terug de foute indeling hebt gekozen, komen tekens en cijfers niet overeen met wat je op je toetsen ziet. Vink met de spatiebalk de optie `Show Password in Clear` aan zodat je wachtwoord in gewone tekst op het scherm verschijnt. Controleer of de letters kloppen met wat je typt. Merk je afwijkingen, ga dan met `Go Back` terug naar de toetsenbordstap om dat recht te zetten.

![Wachtwoord ingevuld](26-wachtwoord-ingevuld.png)

Bevestig je gekozen wachtwoord door het nogmaals in te typen.

![Wachtwoord bevestigen](27-wachtwoord-bevestigen.png)

Omdat je studentennummer korter is dan 8 karakters krijg je een melding dat je een zwak wachtwoord gebruikt. Dat klopt, maar je mag dit voorlopig negeren.

![Zwak wachtwoord toch gebruiken](28-zwak-wachtwoord-gebruiken.png)

### De schijf partitioneren

Tijd om de virtuele harde schijf klaar te maken. Kies de optie `Guided - use entire disk and set up LVM`. Het installatieprogramma regelt de indeling dan vanzelf en voegt meteen Logical Volume Management toe, waardoor je volumes achteraf vlotter herschaalt.

![Partitioneermethode: guided met LVM](29-partitioneermethode-guided-lvm.png)

Er staat maar één virtueel opslagmedium in de lijst, bijvoorbeeld `SCSI1 (0,0,0) (sda) - 40.8 GB VBOX HARDDISK`. Je kunt dus geen fysieke partities van je eigen Mac overschrijven of wissen.

![Schijf selecteren: sda](30-schijf-selecteren-sda.png)

Selecteer vervolgens `All files in one partition (recommended for new users)`.

![Partitieschema: alles in één partitie](31-partitieschema-alles-in-een-partitie.png)

Geef toestemming om de partitietabel aan te passen door `Yes` te kiezen.

![Wijzigingen wegschrijven en LVM configureren](32-wijzigingen-schrijven-en-lvm-configureren.png)

Accepteer de voorgestelde grootte voor de volumegroep (ongeveer 38,7 GB) en ga verder via `Continue`.

![Grootte van de volumegroep](33-grootte-volume-group-38gb.png)

Het systeem toont nu een finaal overzicht met een root-volume, swap-partitie en boot-partitie. Dit is de laatste stap waarin je nog zonder gevolgen kan afbreken. Selecteer `Yes` om de schijf definitief in te richten.

![Wijzigingen definitief naar de schijf schrijven](34-wijzigingen-naar-schijf-schrijven.png)

### Het systeem installeren

Het basisbesturingssysteem wordt nu naar de virtuele schijf geschreven.

![Het basissysteem wordt geïnstalleerd](35-basissysteem-installeren.png)

Vervolgens configureert de installer pakketbeheerder `apt`, zodat het systeem toekomstige software kan ophalen.

![apt wordt geconfigureerd](36-apt-configureren.png)

De eerste reeks bestanden wordt gedownload en geinstalleerd.

![Software wordt gedownload en geïnstalleerd](37-software-selecteren-en-installeren.png)

Hierna vraagt het systeem welke softwarepakketten je direct wilt meenemen. Tot nu toe staat er enkel een minimale Linux-installatie op de machine, zonder grafische interface. Vink met de spatiebalk uitsluitend `Trisquel desktop environment` aan en laat de overige opties leeg. Druk op `Tab` om naar `Continue` te navigeren en druk op `Enter`. Neem hier even pauze: het downloaden van de volledige desktopomgeving duurt even.

![Softwareselectie: Trisquel desktop environment](38-softwareselectie-trisquel-desktop-environment.png)

Als sluitstuk installeert de wizard de GRUB-bootloader, zodat je virtuele machine zelfstandig opstart.

![De GRUB-bootloader wordt geïnstalleerd](39-grub-bootloader-installeren.png)

Zodra de melding `Installation complete` verschijnt, rond je af met `Continue` om het systeem te herstarten.

![Installatie voltooid](40-installatie-voltooid-herstarten.png)

## De eerste keer opstarten

Trisquel start nu door naar zijn eigen grafische bootscherm.

![Het opstartscherm van Trisquel](41-trisquel-opstartscherm.png)

Daarna beland je op het inlogscherm. Klik op je accountnaam, typ je wachtwoord in en druk op `Log In`.

![Inlogscherm](42-inlogscherm-andie.png)

Weigert het systeem je wachtwoord? Dan staat je toetsenbord layout zo goed als zeker verkeerd ingesteld. Rechtsboven op het inlogscherm kun je via de taalknop (vaak aangeduid met `en`) een andere toetsenbordindeling forceren. Typ je wachtwoord desnoods eerst even in het gebruikersnaamveld om visueel te controleren wat er werkelijk aan tekens op het scherm verschijnt.

## Guest Additions installeren

De grafische interface werkt, maar het venster zit voorlopig vast op een lage resolutie en klembordintegratie ontbreekt nog. Dit verhelp je door de *Guest Additions* te installeren: een bundel stuurprogramma's die binnen het gastsysteem draaien.

Koppel eerst het installatiebestand los, anders start de virtuele machine mogelijk opnieuw de installatiewizard op. Ga in het VirtualBox-venster naar `Devices` > `Optical Drives` > `Remove Disk From Virtual Drive`.

![De iso uit het virtuele station verwijderen](43-devices-schijf-verwijderen-uit-virtueel-station.png)

In ditzelfde menu herken je actieve schijven aan het vinkje dat ernaast staat.

![Het submenu Optical Drives toont de huidige schijf](48-devices-optical-drives-submenu.png)

Om deze stuurprogramma's te kunnen compileren heb je ontwikkeltools en actuele kernelheaders nodig. Start een terminalvenster via `Applications` > `Accessories` > `MATE Terminal`.

![Een terminal openen via het menu](46-mate-terminal-openen-via-menu.png)

Voer de volgende instructie uit:

```
sudo apt update
sudo apt upgrade
sudo apt install gcc make tree # Optional
sudo apt install build-essential dkms linux-headers-$(uname -r)
```

![De benodigde pakketten installeren](45-terminal-build-essential-dkms-linux-headers.png)

Als deze pakketten al geïnstalleerd zijn, meldt `apt` simpelweg dat alles up-to-date is en hoef je verder niets te doen.

Koppel nu het schijfbestand met de Guest Additions virtueel aan via `Devices` > `Insert Guest Additions CD image...`.

![De Guest Additions-cd invoegen](49-guest-additions-cd-image-invoegen.png)

Let op: deze handeling steekt de virtuele cd enkel in de lade. Trisquel start niets automatisch en mount de schijf niet vanzelf. Kijk je meteen in de map `/media/cdrom`, dan staat daar nog niets in:

```
cd /media/cdrom
ls
```

![/media/cdrom is nog leeg](50-terminal-media-cdrom-is-leeg.png)

Koppel de virtuele schijf dus zelf handmatig aan. Gebruik hiervoor het pad `/media/cdrom` (de map `/mnt/cdrom` bestaat standaard niet):

```
cd ..
sudo mount /dev/cdrom /media/cdrom
```

De melding `source write-protected, mounted read-only` is volkomen logisch, want een optische schijf is altijd alleen-lezen. Op je bureaublad zie je nu ook een cd-icoontje verschijnen.

![De cd aankoppelen op /media/cdrom](51-cdrom-mounten-op-media-cdrom.png)

Vraag de mapinhoud opnieuw op om de bestanden van de schijf te zien:

```
cd /media/cdrom
ls
```

In het overzicht zie je `VBoxLinuxAdditions-arm64.run` staan. Dat is het bestand dat we zoeken. De versie zonder `arm64` in de bestandsnaam is bedoeld voor klassieke `x86_64`-systemen.

![De inhoud van de Guest Additions-cd](52-inhoud-guest-additions-cd.png)

Start het script. Vergeet de `./` aan het begin niet, want zonder die toevoeging zoekt Linux uitsluitend in de systeemmappen en zal het script niet gevonden worden.

![Het commando zonder ./ werkt niet](53-guest-additions-commando-typen.png)

```
sudo ./VBoxLinuxAdditions-arm64.run
```

![De installatie van de Guest Additions starten](54-guest-additions-installatie-starten.png)

Het script pakt de bestanden uit en bouwt automatisch de vereiste modules voor jouw actieve kernel. Dat vraagt een minuutje geduld. Notificaties zoals `System running in EFI mode, skipping` en de melding dat je best opnieuw inlogt, zijn louter informatief en duiden niet op problemen.

![De Guest Additions zijn geïnstalleerd](55-guest-additions-installatie-voltooid.png)

Start je virtuele machine na afloop opnieuw op om de nieuwe drivers actief te laden.

![De virtuele machine afsluiten of herstarten](56-systeem-afsluiten-dialoog.png)

## Gedeeld klembord en drag-and-drop

Dankzij de Guest Additions kun je vlot kopiëren en plakken tussen macOS en Trisquel, al moet je die integratie eerst nog even inschakelen. Sluit je virtuele machine hiervoor helemaal af zodat hij op `Powered Off` staat.

![De virtuele machine is uitgeschakeld](57-virtualbox-manager-vm-powered-off.png)

Navigeer binnen VirtualBox naar `Settings` > `General` > `Features` en zet zowel `Shared Clipboard` als `Drag-and-Drop` op `Bidirectional`. Sla op met `OK` en start Trisquel opnieuw op.

![Gedeeld klembord en drag-and-drop op Bidirectional](58-instellingen-gedeeld-klembord-en-drag-and-drop.png)

Het venster van Trisquel past zich voortaan automatisch aan zodra je de randen versleept, en tekst of bestanden verplaats je nu probleemloos heen en weer tussen macOS en je virtuele machine.
