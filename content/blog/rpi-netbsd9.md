Title: Fun installing NetBSD 9.0 on a Raspberry Pi B+
Slug: rpi-netbsd9
Date: 2020-05-07 22:00
Status: published
Category: NetBSD, Raspberry PI

One of the consequences of being on a lockdown is that you find time to do things you've been putting off for a while. One of mine is setting up a small bastion server on my home network. Having already set up dynamic DNS with [Duck DNS](https://www.duckdns.org/), I found one of my old Raspberry Pis when I was digging through some unopened boxes from when I'd last moved. I spent an inordinate amount of time getting an OS onto it after spending far too long believing that it was a RPi 2 B rather than the original B+ it actually was. Unfortunately the Pibow case it's in obscured that particular bit of information.

Still, I managed to get NetBSD 9.0 up and running on it after going through my cache of micro SD cards to find a healthy one and following the sometimes obtuse "[NetBSD/evbarm on Raspberry Pi](https://wiki.netbsd.org/ports/evbarm/raspberry_pi/)" page, I got it booting. The initial experience was slightly better. I recall when I first used NetBSD on a MiniITX box about a decade ago that I had to do some weird USB-related device wrangling, but everything just worked. Well, almost: the USB WiFi dongle in the RPi was recognised but couldn't scan for networks successfully, so had to drop back to wired access. Not the end of the world, mind.

I set up a user:

```console
# useradd -m -G wheel keith
# passwd keith
```

Ensured multicast DNS would work on the next reboot:

```console
# echo "mdnsd=YES" >> /etc/rc.conf
```

And edited `/etc/ssh/sshd_config` to allow password-based login.

This is when the actual fun began.

I shut down the RPi (with `shutdown -p now`), wired it up, waited a while, and ssh'd in successfully. The nice thing about enabling _mdnsd_ is that I could just type `ssh rpi.local`, and it just worked. I pinged a few IPs to make sure everything worked, and everything looked good, so I figured it was time to make sure the basics were present.

I tried typing [`pkgin`](http://pkgin.net/), with no luck. I recalled that NetBSD still has [`pkg_add`](https://netbsd.gw.com/cgi-bin/man-cgi?pkg_add++NetBSD-current), so switched to root with `su` and ran `pkg_add pkgin`. Here's what happened:

```console
# pkg_add pkgin
pkg_add: no pkg found for 'pkgin', sorry.
pkg_add: 1 package addition failed
# export PKG_PATH="https://ftp.netbsd.org/pub/pkgsrc/packages/NetBSD/earmv6hf/9.0/All/"
# pkg_add -v pkgin
PGPV_BN_cmp failed
1623256064:error:14199077:SSL routines:tls_construct_cke_rsa:bad rsa encrypt:/usr/src/crypto/external/bsd/openssl/dist/ssl/statem/statem_clnt.c:3019:
pkg_add: Can't process https://ftp.netbsd.org:443/pub/pkgsrc/packages/NetBSD/earmv6hf/9.0/All//pkgin*: Authentication error
pkg_add: no pkg found for 'pkgin', sorry.
pkg_add: 1 package addition failed
```

After some flailing around, I gave up on expecting `pkg_add` to be network aware, so resorted to downloading packages and installing them (I'm omitting a lot here):

```console
# ftp https://ftp.netbsd.org/pub/pkgsrc/packages/NetBSD/earmv6hf/9.0/All/pkgin-0.14.0.tgz
# ftp https://ftp.netbsd.org/pub/pkgsrc/packages/NetBSD/earmv6hf/9.0/All/pkg_install-20191008.tgz
# pkg_add pkg_install-20191008.tgz
# pkg_add pkgin-0.14.0.tgz
```

Progress! So, let's download the repo database:

```console
# pkgin update
reading local summary...
processing local summary...
processing remote summary (https://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/evbarm/9.0/All)...
pkg_summary.gz                                                      0%    0     0.0KB/s   --:-- ETA
/!\ Warning /!\ earm doesn't match your current architecture (earmv6hf)
You probably want to modify /usr/pkg/etc/pkgin/repositories.conf.
Still want to proceed ? [y/N] y
pkg_summary.gz                                                    100%  738KB  22.4KB/s   00:33
```

Eh... OK. Did I choose the wrong image? Why is this somehow working?!

I need Python so I can later pave the machine properly with Ansible, so:

```console
# pkgin install python37
calculating dependencies...done.

3 packages to install:
  libuuid-2.32.1 libffi-3.2.1nb4 python37-3.7.5

0 to refresh, 0 to upgrade, 3 to install
25M to download, 89M to install

proceed ? [Y/n] y
libuuid-2.32.1.tgz                                                100%   39KB  39.1KB/s   00:00
libffi-3.2.1nb4.tgz                                               100%   32KB  32.2KB/s   00:00
python37-3.7.5.tgz                                                100%   25MB 941.1KB/s   00:27
installing libuuid-2.32.1...
installing libffi-3.2.1nb4...
installing python37-3.7.5...
pkg_install warnings: 3, errors: 3
pkg_install error log can be found in /var/db/pkgin/pkg_install-err.log

# cat /var/db/pkgin/pkg_install-err.log
---May 07 04:45:17: installing libuuid-2.32.1...
pkg_add: Warning: package `libuuid-2.32.1' was built for a platform:
pkg_add: NetBSD/earm 9.0 (pkg) vs. NetBSD/earmv6hf 9.0 (this host)
pkg_add: 1 package addition failed
---May 07 04:45:17: installing libffi-3.2.1nb4...
pkg_add: Warning: package `libffi-3.2.1nb4' was built for a platform:
pkg_add: NetBSD/earm 9.0 (pkg) vs. NetBSD/earmv6hf 9.0 (this host)
pkg_add: 1 package addition failed
---May 07 04:45:17: installing python37-3.7.5...
pkg_add: Warning: package `python37-3.7.5' was built for a platform:
pkg_add: NetBSD/earm 9.0 (pkg) vs. NetBSD/earmv6hf 9.0 (this host)
pkg_add: 1 package addition failed
```

Well, how about that. What struck me as particularly odd about it was this line:

```text
pkg_add: NetBSD/earm 9.0 (pkg) vs. NetBSD/earmv6hf 9.0 (this host)
```

Just... why?! If `pkgin` can look up the correct ABI, why does `$host` in its configuration translate to _the wrong thing_?!

I edited `/usr/pkg/etc/pkgin/repositories.conf` to replace `$arch` with `earmv6hf`, and tried again. This time, I was successful. And so it became time to tackle that one annoying part of every RPi: the (understandable) lack of a battery-backed clock:

```console
# service ntpd stop
Stopping ntpd.
# ntpd -gq
14 Feb 10:03:17 ntpd[790]: ntpd 4.2.8p11-o Sat Sep 29 17:04:56 EDT 2018 (import): Starting
14 Feb 10:03:17 ntpd[790]: Command line: ntpd -gq
14 Feb 10:03:17 ntpd[790]: proto: precision = 4.000 usec (-18)
14 Feb 10:03:17 ntpd[790]: Listen and drop on 0 v6wildcard [::]:123
14 Feb 10:03:17 ntpd[790]: Listen and drop on 1 v4wildcard 0.0.0.0:123
14 Feb 10:03:17 ntpd[790]: Listen normally on 2 usmsc0 [fe80::2dfe:ee49:d966:6c2c%1]:123
14 Feb 10:03:17 ntpd[790]: Listen normally on 3 usmsc0 192.168.1.75:123
14 Feb 10:03:17 ntpd[790]: Listen normally on 4 lo0 127.0.0.1:123
14 Feb 10:03:17 ntpd[790]: Listen normally on 5 lo0 [::1]:123
14 Feb 10:03:17 ntpd[790]: Listen normally on 6 lo0 [fe80::1%2]:123
14 Feb 10:03:17 ntpd[790]: Listening on routing socket on fd #27 for interface updates

 7 May 04:26:57 ntpd[790]: ntpd: time set +7151010.203254 s
ntpd: time set +7151010.203254s
# service ntpd start
Starting ntpd.
```

It's all working now, until I next reboot at least.

It'd be really good if NetBSD produced a smaller 'headless' image that lacked X11, as that would knock a significant chunk off the image, and if `pkgin` could bootstrap itself like FreeBSD's `pkgng`. Some day, maybe. I'd settle for `pkg_add` in base having properly functioning TLS support though.

Next up: using BIND 9, dhcpd, and bozohttpd to effectively build a [Pi-hole](https://pi-hole.net/), and configure [blacklistd](https://netbsd.gw.com/cgi-bin/man-cgi?blacklistd+8) to protect it from the big wide world.

## Addendum

I ran into some issues with the [`authorized_key`](https://docs.ansible.com/ansible/latest/modules/authorized_key_module.html) Ansible module. The solution was this:

```console
# pkgin install mozilla-rootcerts-openssl
```

It'd be interesting if downloading and installing this _first_ would've fixed `pkg_add`'s issues installing `pkgin` in the first place.
