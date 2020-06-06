Title: Notes on breathing life back into a Dell Mini 12
Slug: notes-dell-mini-12
Category: Tech
Date: 2020-05-23 21:09
Status: published
Series: Dell Mini 12

(These are some rough, unedited notes from when I was rebuilding the machine today.)

I have a Dell Mini 12, and while I'm pretty sure it's never going to be of much practical use, I'd like to restore it to a state where it might be useful as a stripped down machine running just X, a window manager, and a few other tools, as a distraction-free dev environment. This machine doesn't have to be fast or even particularly usable for anyone else. It just needs to _work_.

My tasks are:

 * Get X running on startup.
 * Get wireless working again.
 * Get Awesome (or whatever window manager I choose to use) in a usable state.

I uninstalled most of the packages that were installed on this machine. It was originally configured to run Lubuntu. Kept installed are:

 * bcmwl-kernel-source (to have some hope of keeping wireless working)
 * debfoster
 * dillo (it's the one graphical browser I know won't cripple this machine)
 * firmware-b43-installer (again, for wireless)
 * fish
 * fonts-dejavu
 * fonts-inconsolata
 * fonts-sil-gentium
 * git
 * gksu
 * hwdata
 * jpegoptim
 * linux-generic
 * optipng
 * resolvconf (not sure if this is _really_ necessary)
 * sqlite3
 * ssh
 * tmux
 * ubuntu-minimal (doesn't this sound like something ubuntu-standard should have as a dependency?)
 * ubuntu-standard
 * vim
 * w3m
 * whois
 * wpasupplicant (wireless)
 * xorg
 * xserver-xorg-input-evdev (do I really need this?)
 * xserver-xorg-input-synaptics (to keep the touchpad working)
 * zip

I installed:

 * awesome

Eventually, I'll install:

 * SLiM (as I need a display manager for desktop login eventually)

I have no problem with stating that I don't really know what I'm doing. The last time I got this kind of thing working was well over a decade ago, and that box ran FreeBSD. I've pretty much forgotten all of that in the meantime, so this will be a learning experience.

# First reboot

I should've expected this, but was still disappointed to discover that the only network interface up and running on reboot was `lo0`, so no wireless. I'd _hoped_ to see `wlan0`, but no luck. I could start X though, and got a desktop. I had to run `startx` from a TTY for that, as there's no display manager installed. I got the `wlan0` interface up with `sudo ifconfig wlan0 up`, but that didn't really gain me a lot as it's not connected to anything, and that isn't ultimately sustainable. Running `wpa_cli -i wlan0` gave me the error `Could not connect to wpa_supplicant: wlan0`. I could see that the unit was running, but after some fumbling around, I discovered some documentation that told me it was looking for a configuration file at `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf` and couldn't find it. Here's what I added:

```properties
# set location of the control socket
ctrl_interface=/run/wpa_supplicant
update_config=1
```

Then I ran `sudo systemctl restart wpa_supplicant`, but got the same error. And of course I did, because the `wpa_supplicant` unit configures it to be managed by NetworkManager.

So, back to the drawing-board: disable the DBus/NetworkManager unit and manually manage `wlan0`:

```console
# systemctl disable --now wpa_supplicant
# systemctl enable --now wpa_supplicant@wlan0
```

Success!

```console
# wpa_cli
wpa_cli v2.6
Copyright (c) 2004-2016, Jouni Malinen <j@w1.fi> and contributors

This software may be distributed under the terms of the BSD license.
See README for more details.


Selected interface 'wlan0'

Interactive mode

> scan
OK
<3>CTRL-EVENT-SCAN-STARTED
<3>CTRL-EVENT-SCAN-RESULTS
<3>WPS-AP-AVAILABLE
<3>CTRL-EVENT-NETWORK-NOT-FOUND
> scan_results
bssid / frequency / signal level / flags / ssid
de:ad:be:ef:f0:0d       2437    -53     [WPA-PSK-TKIP][WPA2-PSK-CCMP][WPS][ESS] MyWLAN
...
de:ad:be:ef:f0:0d       2412    -68     [WPA-PSK-TKIP][WPA2-PSK-CCMP][WPS][ESS] NeighboursWLAN
de:ad:be:ef:f0:0d       2437    -73     [WPA2-PSK-CCMP][ESS]    Nest
de:ad:be:ef:f0:0d       2437    -88     [ESS]   Victoria's castle.k
```

(Some details redacted to hide the identities of my neighbours.)

We're getting somewhere!

```console
> add_network
0
> set_network 0 ssid "MyWLAN"
OK
> set_network 0 psk "secret"
OK
> enable_network 0
OK
<3>CTRL-EVENT-SCAN-STARTED
<3>CTRL-EVENT-SCAN-RESULTS
<3>WPS-AP-AVAILABLE
<3>Trying to associate with de:ad:be:ef:f0:0d (SSID='MyWLAN' freq=2437 MHz)
<3>Associated with de:ad:be:ef:f0:0d
<3>CTRL-EVENT-SUBNET-STATUS-UPDATE status=0
<4>RSC 0000000000000074 is likely bogus, using 0
<3>WPA: Key negotiation completed with de:ad:be:ef:f0:0d [PTK=CCMP GTK=TKIP]
<3>CTRL-EVENT-CONNECTED - Connection to de:ad:be:ef:f0:0d completed [id=0 id_str=]
> save config
OK
```

That confirmed that everything worked, however there's no DHCP client running, so no way for it to get an IP address, but that's easily fixed:

```console
$ ip addr dev wlan0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:24:d2:0d:e0:5b brd ff:ff:ff:ff:ff:ff
    inet6 fe80::224:d2ff:fe0d:e05b/64 scope link
       valid_lft forever preferred_lft forever
# dhclient
$ ip addr show dev wlan0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:24:d2:0d:e0:5b brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.84/24 brd 192.168.1.255 scope global wlan0
       valid_lft forever preferred_lft forever
    inet6 fe80::224:d2ff:fe0d:e05b/64 scope link
       valid_lft forever preferred_lft forever
```

And now we have wireless again... until I reboot.

Apparently, `systemd-networkd` is meant to handle this, so I may need to adjust how I'm getting everything configured.

It would be a bit much to describe the machine as 'usable', but it's close enough.

At this point, I rebooted to see if SLiM would start after I installed it.

# Second reboot

The good news is that SLiM ran on boot by whatever arcane mechanism Debian and Ubuntu use to start X, and `wlan0` was mostly configured. However, Awesome was incredibly slow to start, so I decided to ditch it for i3. Dillo turned out to not exactly be the most reliable bit of software, with it sometimes not bothering to fetch the URLs I'd type into its address bar. And I had to run `sudo dhclient` again to get an address.

Quitting awesome threw me back to SLiM, and when I logged in, I has an i3 session.

I installed mplayer and avahi-daemon too. Multicast DNS is just that useful.

I figured I should try and get `systemd-networkd` doing its job as a DHCP client, so I took a read of the `systemd.network` manpage. One of the examples told me what I needed to do:

```ini
# /etc/systemd/network/80-dhcp.network
[Match]
Name=eth* wlan*

[Network]
DHCP=yes
```

The defaults for the `[DHCP]` section looked sane, so I didn't bother adding anything. Then I ran:

```console
# systemctl enable --now systemd-networkd
```

# Third reboot

I performed another reboot to make sure that the DHCP configuration I added actually worked; it did.

This time around I want to make sure that audio still works in spite of PulseAudio no longer being installe, and the various ALSA packages that automatically installed no longer being so.

As I have mplayer installed, I used it to play a track already sitting on the machine:

```console
$ mplayer Music/65daysofstatic\ -\ Crash\ Tactics.mp3
MPlayer 1.3.0 (Debian), built with gcc-7 (C) 2000-2016 MPlayer Team

Playing Music/65daysofstatic - Crash Tactics.mp3.
libavformat version 57.83.100 (external)
Audio only file format detected.
Load subtitles in Music/
==========================================================================
Opening audio decoder: [mpg123] MPEG 1.0/2.0/2.5 layers I, II, III
AUDIO: 44100 Hz, 2 ch, s16le, 160.0 kbit/11.34% (ratio: 20000->176400)
Selected audio codec: [mpg123] afm: mpg123 (MPEG 1.0/2.0/2.5 layers I, II, III)
==========================================================================
AO: [pulse] Init failed: Connection refused
Failed to initialize audio driver 'pulse'
AO: [alsa] 48000Hz 2ch s16le (2 bytes per sample)
Video: no video
Starting playback...
```

I expected this, so installed `alsa-utils`, and yet there was no sound, even after tweaking the levels with `alsamixer`. Then I noticed the 'MM' under the master volume control and realised that the audio was muted. Once I'd unmuted the audio, it started working.

mplayer is a bit impractical as a music player, so I decided to install `mpd` and `mpc`. As this isn't a server, I want it to run as a user daemon:

```console
# apt install mpc mpd
# systemctl disable --now mpd
$ mkdir -p ~/Music/.playlists ~/.config/mpd
$ cat > ~/.config/mpd/mpd.conf
music_directory "~/Music"
playlist_directory "~/Music/.playlists"
log_file "~/.cache/mpd.log"
db_file "~/.cache/mpd.db"
bind_to_address "~/.cache/mpd.sock"
^D
$ systemctl --user enable --now mpd
$ export MPD_HOST=$HOME/.cache/mpd.sock
$ mpc add ~/Music/65daysofstatic\ -\ Crash\ Tactics.mp3
$ mpc play
```

# Other bits

I installed `rxvt`, gave it a sensible configuration in [.Xdefaults](https://github.com/kgaughan/dotfiles/blob/master/common/.Xdefaults), and ran:

```console
$ xrdb ~/.Xdefaults
# update-alternatives --config x-terminal-emulator
```

I also installed:

 * hsetroot
 * moreutils
 * valac

I ran this to attempt to give the machine booting with plymouth rather than the text console:

```console
# dpkg-reconfigure plymouth-theme-ubuntu-text
```

But for whatever reason, possibly down to some grub configuration, it didn't work. It could be because `GRUB_CMDLINE_LINUX_DEFAULT` contains `console=tty8` for some reason.

I tweaked `/etc/slim.conf`, making the following modifications:

```text
default_user   keith
focus_password yes
current_theme  debian-joy
```

SLiM is never going to win awards for its appearance, though I did find [this repo](https://github.com/adi1090x/slim_themes), which has some reasonable themes. Apparently, SLiM hasn't been maintained for a long time, and lacks [logind](https://www.freedesktop.org/software/systemd/man/systemd-logind.service.html) support, so LXDM might be a reasonable alternative. None of this bothers me much though.

Here's the contents of `~/.config/mpd/mpd.conf`:

```text
music_directory "~/Music"
playlist_directory "~/Music/.playlists"
log_file "~/.cache/mpd.log"
db_file "~/.cache/mpd.db"
bind_to_address "~/.cache/mpd.sock"
```

Here's `~/.xsession`:

```sh
#!/bin/sh
export MPD_HOST=$HOME/.cache/mpd.sock
test -e ~/.config/wallpaper && hsetroot -center ~/.config/wallpaper
test -e ~/.Xdefaults && xrdb ~/.Xdefaults
exec /usr/bin/x-window-manager
```

Apparently, `feh` can be used to set the root window, so that looks like it could be an option.

I haven't tweaked `~/.config/i3/config` beyond this:

```text
font pango:DejaVu Sans 8
```

I have still to work out why Awesome was so slow. i3 is simpler to configure and gives me what I want, so I can't see myself switching away.
