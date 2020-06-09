Title: Awkwardly flailing around to get sshguard working on NetBSD
Date: 2020-06-09 22:05
Status: published
Category: Tech

When [I previously configured NetBSD 9]({filename}rpi-netbsd9.md), I'd forgotten that I should configure [sshguard](https://www.sshguard.net/) and a firewall on the Raspberry Pi. It's time to fix that.

I figured that I'd install the package:

```console
# pkgin install sshguard
calculating dependencies...done.

1 package to install:
  sshguard-1.5nb1

0 to refresh, 0 to upgrade, 1 to install
0B to download, 270K to install

proceed ? [Y/n] y
installing sshguard-1.5nb1...
===========================================================================
The following files should be created for sshguard-1.5nb1:

        /etc/rc.d/sshguard (m=0755)
            [/usr/pkg/share/examples/rc.d/sshguard]

===========================================================================
pkg_install warnings: 0, errors: 0
reading local summary...
processing local summary...
marking sshguard-1.5nb1 as non auto-removable
```

That's weirdly inconvenient, but OK.

```console
# install -m755 /usr/pkg/share/examples/rc.d/sshguard /etc/rc.d
# echo "sshguard=YES" >> /etc/rc.conf
# service sshguard start
Starting sshguard.
# service sshguard status
sshguard is not running.
```

Hmm. Maybe it's that I didn't have a firewall running?

```console
# echo "ipfilter=YES" >> /etc/rc.conf
# service ipfilter start
/etc/rc.d/ipfilter: WARNING: /etc/ipf*.conf not readable; ipfilter start aborted.
```

Maybe some bare-bones config is what it needs?

```console
# echo "pass in on any all" > /etc/ipf.conf
# service ipfilter start
Enabling ipfilter.
0:open device: Device not configured
0:SIOCFRENB: Bad file descriptor
open device: Device not configured
User/kernel version check failed
open device: Device not configured
User/kernel version check failed
0:1:ioctl(add/insert rule)
```

At this point, I'm confused. I can't see anything that indicates why this isn't working, so I take a quick look at `/etc/rc.d/ipfilter`, but it reveals nothing. I reboot, and lo-and-behold:

```console
# service ipfilter status
ipf: IP Filter: v5.1.2 (408)
Kernel: IP Filter: v5.1.2
Running: yes
Log Flags: 0 = none set
Default: pass all, Logging: available
Active list: 0
Feature mask: 0x14e
```

I don't know what's different, but at least now it's running.

Let's try sshguard again:

```console
# service sshguard start
Starting sshguard.
# service sshguard status
sshguard is not running.
```

As the version for NetBSD is rather old, I figured I'd look at the [FreeBSD port for sshguard 1.5](https://svnweb.freebsd.org/ports/head/security/sshguard/?pathrev=382064) to see if it could shed some light on why it wasn't working before I went down the path of running it by hand. Unfortunately, it did little to enlighten me as to what was going on. All that's left is to try running it by hand:

```console
# /usr/pkg/sbin/sshguard -b /var/db/sshguard-blacklist.db -l /var/log/authlog -l /var/log/maillog
Could not init firewall. Terminating.
```

(I later found out that I could've seen this had I checked `/var/log/authlog`, but that's not at all an obvious location unless you know sshguard's logging behaviour beforehand.)

Well, that would've been good to know sooner, like when I ran `service sshguard start`. But, _which_ filewall? Time to poke around [options.mk](http://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/security/sshguard/options.mk), which implies that on NetBSD, it uses ipfilter by default, as I'd expected:

```make
PKG_SUGGESTED_OPTIONS.NetBSD=		sshguard-ipfilter
...
.elif !empty(PKG_OPTIONS:Msshguard-ipfilter)
CONFIGURE_ARGS+=	--with-firewall=ipfilter
# Set correct location of IPFilter configuration file under NetBSD.
CONFIGURE_ARGS.NetBSD+=	--with-ipfilterconf=/etc/ipf.conf
```

I brought up the [ipf documentation](https://web.archive.org/web/20180902011955/https://www.sshguard.net/docs/setup/#ipf) on the sshguard website, which states:

<blockquote>
<p>Insert the following lines in <code>ipf.rules</code> where SSHGuard's rules should go:</p>
<pre>
##sshguard-begin##
##sshguard-end##
</pre>
<p>SSHGuard will add or remove rules between these two lines and reload <code>ipf</code> after each change.</p>
</blockquote>

It would've been good if that little snippet of information had been included in the installation instructions. I edited `/etc/ipf.conf` and tried again:

```console
# service sshguard start
Starting sshguard.
# service sshguard status
sshguard is running as pid 1066.
```

Success!

Admittedly something like [blacklistd](https://netbsd.gw.com/cgi-bin/man-cgi?blacklistd) would probably be preferable, but this at least gets something basic up and running.

The whole thing was far more obtuse than it ought to have been. The with some extra lines in the installation message explaining what needed to be done with `/etc/ipf.conf` would've saved so much time.

I'm also mystified why ipfilter didn't start as I'd expected it to. I expected it would be compiled into the kernel and wouldn't need any special massaging. Why it started working all of a sudden is a mystery to me. Maybe I did something to accidentally get it working and I just didn't notice? I found [this message](http://mail-index.netbsd.org/port-arm/2018/07/05/msg004928.html), but the thread it's part of hasn't been terribly enlightening. Still, when I give blacklistd a try, I'll also give npf a try too.
