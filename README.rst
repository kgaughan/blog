This is the Pelican_ source for my `Can't Hack` blog. I can't see there being
anything terribly interesting here except maybe to poke around some unpublished
draft posts that might be checked in.

On a bare bones FreeBSD box, you will need to install a few prerequisites::

    $ sudo pkg install rsync gmake py37-pip

On Ubuntu and Debian, avoid the packaged version of Pelican and do this::

    4 sudo apt install rsync python3-pip

Then you can install Pelican itself::

    $ pip3 install --user pelican Markdown typogrify html5lib

On MacOS, using pipx is preferable::

    $ brew install pipx
    $ pipx install pelican
    $ pipx inject pelican Markdown typogrify html5lib

You should also ensure that the pelican-plugins repo is checked out in the
same directory as the repo::

    $ git clone https://github.com/getpelican/pelican-plugins.git

Finally, ensure that reST smart quotes are switched on in ``~/.docutils``::

    [restructuredtext parser]
    smart_quotes=yes

The makefile should be portable, so it'll work with both GNU make and BSD make.

.. _Pelican: https://github.com/getpelican/pelican
.. _Can't Hack: https://i.canthack.it/
