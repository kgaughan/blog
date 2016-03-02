This is the Pelican_ source for my `Can't Hack` blog. I can't see there being
anything terribly interesting here except maybe to poke around some unpublished
draft posts that might be checked in.

On a bare bones FreeBSD box, you will need to install a few prerequisites::

    $ sudo pkg install rsync gmake py27-pip

Then you can install Pelican itself::

    $ pip install --user pelican

And to ensure the theme is pulled in::

    $ git submodule update --init

I may make the Makefile portable so it works on both GNU make and BSD make
without modification.

.. _Pelican: https://github.com/getpelican/pelican
.. _Can't Hack: https://i.canthack.it/
