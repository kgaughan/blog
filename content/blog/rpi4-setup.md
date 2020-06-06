Title: Configuring a Raspberry Pi 4 as a desktop replacement
Date: 2020-06-06 21:00
Status: published
Category: Tech

I gave in to getting a Raspberry Pi 4 last month, and I've tried using it as a
desktop replacement over the past week or so. It hasn't been going so badly!
After some initial issues finding a working SD card, I found the one I'd
originally gotten for my Switch and put [Raspbian](https://www.raspbian.org/)
on it. I went with the _Lite_ version as I planned on keeping what I installed
on it to a minimum.

[Keep in mind that all of this is a highly compressed version of what I did,
and I'm probably leaving out some stuff. However, if I need to rebuild the
machine at some point, this should be enough to get me 99% of the way.]

After boot, I ran `raspi-config` to get the basics working and performed an
upgrade on the OS to get it up to date:

```console
# apt update
# apt dist-upgrade
# reboot
```

Then I got everything installed:

```console
# apt install --no-install-recommends xorg lightdm xdg-utils compton
# apt install --no-install-recommends fish font-inconsolata sqlite3 vim git zip
# apt install debfoster xsel i3 firefox-esr tmux feh fonts-noto fonts-dejavu
# apt install --no-install-recommends python3-venv python3-pip pipx
# apt install xfonts-terminus xfonts-terminus-oblique
# apt install --no-install-recommends keepassxc atril
# apt install avahi-utils cifs-utils smbclient
# apt install --no-install-recommends neomutt ssmtp w3m
# apt install --no-install-recommends ansible
# apt install --no-install-recommends rsync mkdocs
# apt install --no-install-recommends pelican python3-typogrify python3-html5lib
```

I generated some SSH keys:

```console
$ ssh-keygen -t ed25519
```

I got that key copied into Github, checked out my dotfiles repo, and installed
everything:

```console
$ git clone git@github.com:kgaughan/dotfiles.git .dotfiles
$ make -C .dotfiles reinstall
```

I needed to fiddle with `~/.Xdefaults` a bit to get it working as I wanted.

Here's my `~/.xsession` script:

```sh
#!/bin/sh

command -v mpd >/dev/null && export MPD_HOST=$HOME/.cache/mpd.sock
test -e ~/.fehbg && ~/.fehbg

exec /usr/bin/x-window-manager
```

I downloaded a wallpaper and configured it with `feh`:

```console
$ feh --bg-center ~/Pictures/Wallpapers/rainbow-smoke-high-definition_0.jpg
```

It was at this point that I realised I was still using the default _pi_ user,
and I didn't want that, so I created a new user:

```console
# adduser --add_extra_groups keith
# adduser keith sudo
# adduser keith adm
# adduser keith input
# adduser keith games
# adduser keith netdev
# adduser keith gpio
# adduser keith i2c
# adduser keith spi
```

I also want to be able to SSH into this machine:

```console
# systemctl enable --now ssh
```

Here is the output of `localectl`:

```console
$ localectl 
   System Locale: LANG=en_IE.UTF-8
       VC Keymap: ie
      X11 Layout: ie
       X11 Model: pc105
     X11 Variant: UnicodeExpert
     X11 Options: lv3:ralt_switch
```

I needed to do some additioanl fiddling around in `raspi-config` for that.

In `/etc/lightdm/lightdm.conf`, I updated `greeter-hide-users` to `false` to
avoid needing to type in my username.

I investigated the GNOME Epiphany browser as an alternative to Firefox, but I
wasn't too impressed with it. I did mean I installed `compton` however. Here's
my `~/.config/compton.conf` file:

```text
shadow = true;
no-dnd-shadow = true;
no-dock-shadow = true;
# If this is true, it causes some weird outlining
clear-shadow = false;

shadow-ignore-shaped = true;
glx-no-stencil = true;

shadow-opacity = 0.25;
shadow-radius = 5;
shadow-offset-x = -7;
shadow-offset-y = -7;

backend = "glx";
```

My `~/.config/i3/config` file is similar to what I set up on the
[Dell Mini 12]({filename}/notes-dell-mini-12.md) when I tried getting it
working again. I added/modified:

```text
exec --no-startup-id compton -b
set $mod Mod4
font pango:DejaVu Sans 8
bindsym $mod+Return exec exec i3-sensible-terminal
```

The 'double exec' is so that the shell process i3 spins up when launching the
terminal doesn't stick around.

Once I was happy with everything, I obliterated the `pi` user:

```console
# deluser --remove-all-files pi
```

As I want to mount the SMB share from my NAS, I added this to `/etc/fstab`:

```text
//192.168.1.160/nas /media/keith cifs username=keith,credentials=/home/keith/.smbcred,uid=1001,gid=1001 0 0
```

I created `~/.smbcred` with the permissions `600` to store the password:
```text
password=500p3r53kr3t
```
And got it mounted:

```console
# mkdir -p /media/keith
# chown keith:keith /media/keith
# mount -a
```

## Opinion

It's been going surprisingly well! Aside from the occasional freeze, which is
likely due to the SD card. I didn't have to get any extra equipment for it as I already had a mouse, keyboard, and mini-HDMI cable ready to use with it.

It's been nice having a relatively distraction free environment to work from.

One minor annoyance is that Raspbian is still 32-bit, while the SOC is 64-bit.
I doesn't matter so much because mine is the 4GB model, but it's unfortunate
as it caused me some confusion when attempting so set up
[gdrive](https://github.com/gdrive-org/gdrive) to I could pull down files from
my Google Drive account.
