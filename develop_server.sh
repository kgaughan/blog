#!/bin/sh
##
# This section should match your Makefile
##
PELICAN=uv run pelican
PELICANOPTS=

BASEDIR=$(pwd)
INPUTDIR=$BASEDIR/content
OUTPUTDIR=$BASEDIR/output
CONFFILE=$BASEDIR/pelicanconf.py

###
# Don't change stuff below here unless you are sure
###

SRV_PID=$BASEDIR/srv.pid
PELICAN_PID=$BASEDIR/pelican.pid

usage () {
	cat <<FIN
Usage: $(basename $0) stop|start|restart

This starts pelican in debug and reload mode and then launches a webserver to
help site development. It doesn't read your pelican options so you edit any
paths in your Makefile you will need to edit it as well.
FIN
	exit 3
}

get_command_by_pid () {
	ps -o pid,comm | tail -n+2 | awk "/\\s*$1 / {print substr(\$0, 7)}"
}

kill_by_pidfile () {
	if test -f "$1"; then
		PID="$(cat $1)"
		PROCESS="$(get_command_by_pid $PID)"
		if test "$PROCESS" = pelican; then
			echo "Killing $2"
			kill "$PID"
		else
			echo "Stale PID, deleting"
		fi
		rm $1
	else
		echo "$2 PIDFile not found"
	fi
}

shut_down () {
	kill_by_pidfile "$SRV_PID" "Pelican server"
	kill_by_pidfile "$PELICAN_PID" "Pelican"
}

start_up () {
	echo "Starting up Pelican and Pelican server"
	$PELICAN --debug --autoreload -r $INPUTDIR -o $OUTPUTDIR -s $CONFFILE $PELICANOPTS &
	echo $! > $PELICAN_PID
	$PELICAN --listen &
	echo $! > $SRV_PID
}

case "$1" in
	stop)
		shut_down
		;;
	start)
		start_up
		;;
	restart)
		shut_down
		start_up
		;;
	*)
		usage
		;;
esac
