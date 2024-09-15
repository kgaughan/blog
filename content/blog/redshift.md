Title: Setting up redshift
Date: 2024-09-15 17:00
Slug: redshift
Category: Health, Tools
Status: published

I revived my old Lenovo Miix 310 yesterday. It's not a great machine by any stretch, but it at least fills a niche similar to the one netbooks used to play for me: it's small, low-power, and can be thrown in a bag. The top row of the detachable keyboard is awkwardly shifted over (making tying numbers and some punctuation awkward), and the touchpad is weirdly sensitive. However, I did get it to work just fine, [albeit with some tweaking]({filename}getting-ubuntu-up-and-running-on-a-lenovo-miix-310.md).

For some reason I'd been under the impression that the machine had become mostly unusable after an upgrade gone wrong, but I suspect I was just mixing that up with a different laptop. I picked it up to see if I could wipe it and reinstall something like Manjaro on it, but it booted up just fine! I got it upgraded from Xubuntu Focal (20.04) through to Xubuntu Noble (24.04), stripped the installed packages down as far as I sensibly could, including replacing xubuntu-desktop with xubuntu-desktop-minimal. So far, it's been working fine.

One thing I wanted to set up was dimming at nighttime to help save my eyes and to help with sleep, but Xubuntu doesn't install anything for that, so I had to do some digging, and recalled [redshift](http://jonls.dk/redshift/). It has a GTK frontend that can function as an indicator, but it crashed for me. I ran it manually, and there were some issues with the GeoClue2 service, which appears to be installed but isn't functioning as expected for me. I figured the next best thing would be to spin it up as a systemd user service.

I dropped the following configuration file at `~/.config/redshift.conf`:

```ini
[redshift]
temp-day=5700
temp-night=3600
gamma=0.8
adjustment-method=randr
location-provider=manual

[manual]
lat=53.35
lon=-6.26
```

I make no secret of the fact that I live in Dublin, so giving away its approximate position on the globe isn't too big a deal! The main things I had to set there were `adjustment-method=randr` as XFCE on this machine doesn't support Wayland as yet, and `location-provider=manual` to prevent it from querying GeoClue2.

Next up was configuring the user service. I dropped this file as `~/.config/systemd/user/redshift.service`, after ensuring the directory existed:

```ini
[Unit]
Description=redshift
After=graphical-session.target

[Service]
Type=notify
Environment=DISPLAY=:0
ExecStart=/usr/bin/redshift
Restart=always

[Install]
WantedBy=default.target
```

Of note is `Type=notify`: this should ensure that the service only starts when X itself is ready.

After that, it was a matter of running:

```
systemctl --user daemon-reload
systemctl --user enable --now redshift
```

And everything just worked. It's survived at least one reboot, so I think it should work away by itself from now on.

I stumbled across an alternative to it called [xsct](https://github.com/faf0/sct). It lacks some of the smarts to toggle things based on when dawn and dusk are and isn't a daemon, but it probably wouldn't be too big a deal to write a wrapper service that can do just that and trigger `xsct` to run as appropriate.
