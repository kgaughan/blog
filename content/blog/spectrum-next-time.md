Title: A time server for the ZX Spectrum Next
Date: 2020-06-22 20:39:00
Category: Projects, Spectrum Next, NetBSD, Retrocomputing
Status: published

I recently received my Spectrum Next. I'd been waiting three years for it, and they started sending them out just as the lockdown started. Thankfully, even though I wasn't able to update the address, they were able to receive it at the office, and drop it over, which relieved me no end.

The model I got was the one with the RPi Zero Accelerator board, WiFi, and the real-time clock. It's been fun to play with so far. I had a C64 as a kid, but I had a bit of a soft spot for the Spectrum, even if it wasn't quite as capable as the C64 for the most part, and the Spectrum Next looked like a really fun project.

This isn't about any of that though. As mentioned, my model has the real-time clock add-on. Natively, NextZXOS supports a protocol called the [Network neXt Time Protocol](https://github.com/Threetwosevensixseven/nxtp). Something like the Spectrum Next doesn't require anything better than second-level accuracy, and something like NTP, or even [SNTP](https://tools.ietf.org/html/rfc4330) are much too complicated for a device as small as the Next, so NXTP keeps it as simple as possible: you the server for the current date and time in a given timezone and it responds with date and time. No integrity beyond a very simple checksum, totally cleartext, but it's good enough.

Unfortunately, the default server implementation is written with .NET Core, and I wanted to be able to install this on a Raspberry Pi sitting in my flat running NetBSD 9, so I knocked together [my own server and client implementation](https://github.com/kgaughan/nxtp) in Go. When built, it weighs in at just over 2MB. Were I to write it in C, I could probably make it significantly smaller, but there's not much point in that, and it'd just complicate the build for anybody who wants to use it.

Hopefully, it should be of use of other Spectrum Next owners.

## Running it under NetBSD

What's left is to run it as a daemon on the Pi, which is easier said than done with servers written in Go, as [this is apparently very finicky](https://github.com/golang/go/issues/227). The alternative is to have something else daemonise it. On FreeBSD, the [_daemon_](https://www.freebsd.org/cgi/man.cgi?query=daemon&apropos=0&sektion=0&manpath=FreeBSD+12.1-RELEASE+and+Ports&arch=default&format=html) command would do the trick, but NetBSD lacks it. However, [_daemond_](https://pkgsrc.se/sysutils/daemond) fits the bill:

```console
$ sudo pkgin install daemond
```

Unlike FreeBSD's _daemon_ command, _daemond_ provides no way to save the PID of the child process it spawns, so we'll have to use _pgrep_ to figure it out, which is less than ideal. Here's the rc script I wrote:

```sh
#!/bin/sh
#
# PROVIDE: nxtp
# REQUIRE: DAEMON

if [ -f /etc/rc.subr ]; then
	. /etc/rc.subr
fi

name=nxtp
rcvar=$name
command="/usr/local/bin/${name}"
pidfile="/var/run/${name}.pid"
nxtp_flags="-endpoint :12300"
start_cmd=nxtp_start

nxtp_start () {
	echo "Starting ${name}."
	/usr/pkg/bin/daemond ${command} ${nxtp_flags}
	/usr/bin/pgrep ${name} > ${pidfile}
}

if [ -f /etc/rc.subr -a -f /etc/rc.conf -a -f /etc/rc.d/DAEMON ]; then
	load_rc_config $name
	run_rc_command "$1"
else
	case ${1:-start} in
	start)
		if [ -x ${command} ]; then
			nxtp_start
		fi
		;;
	stop)
		if [ -f ${pidfile} ]; then
			pid=$(/usr/bin/head -1 ${pidfile})
			echo "Stopping ${name}."
			kill -TERM ${pid}
		else
			echo "${name} not running?"
		fi
		;;
	restart)
		$0 stop
		sleep 1
		$0 start
		;;
	status)
		if [ -f ${pidfile} ]; then
			pid=$(/usr/bin/head -1 ${pidfile})
			echo "${name} is running as pid ${pid}."
		else
			echo "${name} is not running."
		fi
		;;
	esac
fi
```

This went into `/etc/rd.d`, and _nxtp_ went into `/usr/local/bin`. The final bit is to add `nxtp=YES` to `/etc/rc.conf` and run `sudo service nxtp start`.
