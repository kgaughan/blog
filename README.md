This is the [Pelican][] source for [my blog][]. I can't see there being
anything terribly interesting here except maybe to poke around some unpublished
draft posts that might be checked in.

On a bare bones FreeBSD box, you will need to install a few
prerequisites:

```console
$ sudo pkg install rsync gmake py39-pipx
```

Then you can install Pelican itself:

```console
$ pipx install pelican
$ pipx inject pelican Markdown typogrify html5lib
$ pipx inject pelican pelican-more-categories pelican-sitemap pelican-series
```

The makefile should be portable, so it'll work with both GNU make and
BSD make.

[Pelican]: https://github.com/getpelican/pelican
[my blog]: https://keith.gaughan.ie/
[pipx]: https://pipxproject.github.io/pipx/
[pelican-plugins repo]: https://github.com/getpelican/pelican-plugins
