This is the [Pelican][] source for [my blog][]. I can't see there being
anything terribly interesting here except maybe to poke around some unpublished
draft posts that might be checked in.

On a bare bones FreeBSD box, you will need to install a few
prerequisites:

```console
$ sudo pkg install rsync gmake py37-pip
```

Then you can install Pelican itself:

```console
$ pip3 install --user pelican Markdown typogrify html5lib
```

On MacOS, using [pipx][] is preferable:

```console
$ brew install pipx
$ pipx install pelican
$ pipx inject pelican Markdown typogrify html5lib
```

On Ubuntu and Debian:

```console
$ sudo apt install rsync pelican
$ sudo apt install python3-markdown python3-typogrify python3-html5lib
```

You should also ensure that the [pelican-plugins repo][] is checked out in
the same directory as the repo:

```console
$ git clone --recursive https://github.com/getpelican/pelican-plugins.git
```

The makefile should be portable, so it'll work with both GNU make and
BSD make.

[Pelican]: https://github.com/getpelican/pelican
[my blog]: https://keith.gaughan.ie/
[pipx]: https://pipxproject.github.io/pipx/
[pelican-plugins repo]: https://github.com/getpelican/pelican-plugins
