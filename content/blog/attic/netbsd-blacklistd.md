Title: Switching from sshguard to blacklistd
Date: 2020-06-09 22:30
Status: draft
Category: Tech

Last time, [I worked on getting ipfilter and sshguard working]({filename}../netbsd-sshguard.md), but thought I should give [blacklistd](https://netbsd.gw.com/cgi-bin/man-cgi?blacklistd) a go at some point. Well, why not now? It's part of the base system, and ought to be a bit more efficient than sshguard as it doesn't need to do any log parsing.

I tried running it, and didn't expect it to start right out of the box. I wasn't disappointed:

```console
# service blacklistd onestart
/etc/rc.d/blacklistd: WARNING: /etc/blacklistd.conf is not readable.
```

The man page didn't indicated where I might find an example, but a quick `find` revealed on at `/usr/share/examples/blacklist/blacklistd.conf`, which should help. For now, I'm going to assume that it's a good starting point, and if I need to, I'll configure it later.

```console
# cp /usr/share/examples/blacklist/blacklistd.conf /etc/
# service blacklistd onestart
Starting blacklistd.
# service blacklistd onestatus
blacklistd is running as pid 1422.
```

Good so far! So I'll make sure it starts on boot:

```console
# echo "blacklistd=YES" >> /etc/rc.conf
# service blacklistd restart
Stopping blacklistd.
Starting blacklistd.
```

Just to get a rough idea of how much resources each is using:

```console
# ps aux | grep 'blacklist\|sshguard'
root    1520  0.0  0.4  7024  1760 ?     Ss   10:42PM 0:00.01 /sbin/blacklistd
root    1066  0.0  0.5 11424  2288 pts/0 Il    8:53PM 0:00.09 /usr/pkg/sbin/sshguard -b /var/db/sshguard-blacklist.db -l /var/log/authlog -l /var/log/maillog -i /var/run/sshguard.pid
```

blacklistd is indeed a bit more lightweight than sshguard, but not tremendously so, and both daemons are hardly doing anything currently, so it's not entirely fair to compare them like this.

I tried logging in and out to see if I could get anything to happen. Unfortunately...

```console
# blacklistctl dump -a
        address/ma:port id      nfail   last access
```

That should show at least one entry, so I obviously missed something. What documentation I could find implied I need to add `UseBlacklist yes` to `/etc/ssh/sshd_config`:

```console
# echo "UseBlacklist yes" >> /etc/ssh/sshd_config
# service sshd reload
Reloading sshd config files.
```

But disaster struck when I attempted to log back in:

```console
$ ssh rpi.local
ssh: connect to host rpi.local port 22: Connection refused
```

That's not good. Thankfully, I had an SSH session still open on another machine. It turned out that the master sshd process had died when I reloaded the configuration. Running `service sshd restart` revealed that the source of the error was the `UseBlacklist yes` line I added, which isn't actually supported by NetBSD's version of sshd.

So, how to test the thing? Thankfully, I found [this article](https://gioarc.me/2017/05/29/blacklistd-a-new-approach-to-blocking-attackers/), which suggested a simple way: make blacklisting super aggressive with this config file:

```text
# sample blacklistd.conf
# adr/mask:port type    proto   owner           name    nfail   disable
[local]
ssh             stream  *       *               *       1       1m
# adr/mask:port type    proto   owner           name    nfail   disable
[remote]
```

And connect in like so:

```console
ssh -o "PubkeyAuthentication no" rpi.local
```

And... nothing. It's like the ssh daemon isn't hitting blacklistd at all. But I discovered something else interesting. Take a look at some of the code from `/libexec/blacklistd-helper`:

```sh
case "$pf" in
ipf)
    /sbin/ipfstat -io | /sbin/ipf -I -f - >/dev/null 2>&1
    echo block in quick $proto from $addr/$mask to \
        any port=$6 head port$6 | \
        /sbin/ipf -I -f - -s >/dev/null 2>&1 && echo OK
    ;;
```

Yet...

```console
$ which ipfstat
/usr/sbin/ipfstat
```

That's not going to work: for NetBSD, ipfilter support is broken anyway, which means I'm forced to switch to `npf`.

I spent a while going down various rabbitholes in the NetBSD version of OpenSSH, and then it hit me: the test in the article was wrong: if I used a bad username, it ought to trigger blacklistd properly. And it did:

```console
# blacklistctl dump -ar
        address/ma:port id      nfail   remaining time
   192.168.1.10/32:22           1/3     4m23s
```

I finally knew what was going wrong. I decided to patch `/libexec/blacklistd-helper` as that's the path of least resistance.
