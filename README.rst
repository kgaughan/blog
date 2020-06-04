This is the Pelican_ source for `my blog`_. I can't see there being
anything terribly interesting here except maybe to poke around some unpublished
draft posts that might be checked in.

On a bare bones FreeBSD box, you will need to install a few prerequisites::

    $ sudo pkg install rsync gmake py37-pip

Then you can install Pelican itself::

    $ pip3 install --user pelican Markdown typogrify html5lib

On MacOS, using pipx is preferable::

    $ brew install pipx
    $ pipx install pelican
    $ pipx inject pelican Markdown typogrify html5lib

On Ubuntu::

    $ sudo apt install rsync pelican
    $ sudo apt install python3-markdown python3-typogrify python3-html5lib

You should also ensure that the pelican-plugins repo is checked out in the
same directory as the repo::

    $ git clone https://github.com/getpelican/pelican-plugins.git

Finally, ensure that reST smart quotes are switched on in ``~/.docutils``::

    [restructuredtext parser]
    smart_quotes=yes

The makefile should be portable, so it'll work with both GNU make and BSD make.

.. _Pelican: https://github.com/getpelican/pelican
.. _my blog: https://keith.gaughan.ie/
