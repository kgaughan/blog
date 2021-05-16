Title: Doing
Date: 2021-05-16 19:47
Category: Tools
Status: published

I haven't posted anything here in a very long time. I figure I'd might as well share a small tool I knocked together.

Here it is:

```sh
#!/bin/sh

set -eu

usage () {
	echo "usage: ${0##*/} [-h] [MESSAGE]"
}

# Ensure data directory exists
: "${DOING_ROOT:=${XDG_DATA_HOME:-$HOME/.local/share}/doing}"
mkdir -p "$DOING_ROOT"

while getopts h opt; do
	case "$opt" in
	h)
		usage
		exit
		;;
	esac
done

shift $((OPTIND - 1))

# Append the remaining text to the end of today's file
if test -n "$*"; then
	echo "$(date "+%Y-%m-%d %H:%M:%S")\t$*" >> "$DOING_ROOT/$(date +%Y-%m-%d)"
fi
```

It's called `doing`, and it's intended to be a way of capturing what I'm doing at any given moment. The format is simple: one entry per line, with each entry being a set of tab-separated fields. The first field is a date, and the second is a message.

I don't know what else I'll end up using it for. I figure it'll be good for noting down random things during the day, and I can figure out later what to do with them later.
