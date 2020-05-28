Title: Getting Ubuntu up and running on a Lenovo Miix 310
Date: 2018-03-03 16:42:03
Category: Tech
Status: published

Back in January, I picked up a
[Lenovo Miix 310](https://www3.lenovo.com/ie/en/laptops/ideapad/miix-series/Ideapad-Miix-310/p/88EMMX30692)
a while back to play with Windows. It was an interesting experience, but I
really can't see myself shifting my development over to Windows any time soon,
so I figured I'd throw Xubuntu on it and see if it'd be good as something I
could use when travelling.

My first attempt was with 16.04 LTS. That didn't go too well. The biggest issue
was with screen distortion: the graphics looked interlaced. HDMI out worked,
however, but I couldn't get much further with it.

I figured I'd try 17.10, which might have slightly better luck, and it did!
While during boot, the same weird interlacing thing happened, I was able to get
to the point where I had a login screen, albeit one that was rotated, along
with the mouse pointer. To fix that, I made the following update to
`/etc/default/grub`, running `sudo update-grub` afterwards:

```sh
GRUB_CMDLINE_LINUX="fbcon=rotate:1"
```

I then edited `/etc/lightdm/lightdm.conf`:

```ini
[SeatDefault]
display-setup-script=/etc/lightdm/display-setup.sh
```

And created `/etc/lightdm/display-setup.sh`, which I made executable:

```sh
#!/bin/sh

# Fix screen rotation on login.
xrandr --output DSI-1 --rotate right
# Fix mouse.
xinput set-prop "FTSC1000:00 2808:1015" --type=float "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1
```

Then I did my usual setup:

```sh
apt install git tig ansible most vim-gnome tmux meld
apt install debfoster zsh keepassx make openssh-server fonts-inconsolata
ssh-keygen -t ed25519 -f ~/.ssh/id_primary
chsh -s $(which zsh)
mkdir projects
cd projects
git checkout git@github.com:kgaughan/dotfiles/
cd dotfiles
make install
```

This would work in fits and start. Sometimes, I'd be able to boot it up without
any issues, while other times I'd be presented with a black screen. At that
point, I gave up, and the tablet was left sitting on a cupboard in my living
room for a while. I suspected it was an issue with not being able to control
the backlight, but didn't know for sure, or how to solve it.

Recently, however, I came across
[this post on the Lenovo forums](https://forums.lenovo.com/t5/Linux-Discussion/ubuntu-for-Miix-310-10ICR-Tablet/m-p/3996259#M10556)
that gave me the missing part of the puzzle. I edited
`/etc/initramfs-tools/modules`, adding `pwm_lpss_platform`, and ran
`sudo update-initramfs -k all -u`.

A reboot later, and everything's been working almost flawlessly! There are
still a few issues, such as the SD card reader not working (which I believe
won't be an issue in 18.04), and the Bluetooth support being broken, but I can
live without those. The other small issue is that sometimes the device will
hang for seemingly no reason.
