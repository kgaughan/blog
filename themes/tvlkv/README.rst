Tvlkv
=====

The Tvlkv theme was originally based on `William Ting`__'s Svbtle__ theme.
Since I originally forked that, I've essentially ripped out everything from
the original theme, so it deserved a new name. As a nod to the original theme,
I've decided to name it Tvlkv.

.. __: https://github.com/wting/
.. __: https://github.com/wting/pelican-svbtle

For a demo of the theme, visit: https://i.canthack.it/

Aims
----

The theme started as a radical simplification of the original theme's CSS and
HTML templates. I'm still far from done. I've mostly stripped down the CSS,
but I've done less work on the templates.

Still in need of work are:

* The page and article templates needs simplification.
* I've barely touched the archives, author, categories, category, tag, and
  tags templates, aside from some cursory fixes.
* I need to add back in comment support, though I don't want to tie it to
  Disqus. I don't have anything against Disqus, I'd just like to give anybody
  who uses the theme a choice.
* I would like to make the theme responsive, but I haven't decided on what
  the narrow variation is going to look like as yet.
* It'd be nice if it automagically used Font Awesome icons for Github, Twitter,
  &c.

Settings
--------

These are the Pelican global variables currently supported by the theme:

* ``GOOGLE_ANALYTICS``
* ``GAUGES_ANALYTICS``
* ``DISQUS_SITENAME``
* ``LINKS = (('name1', 'url1'), ('name2', 'url2'))``
* ``DEFAULT_DATE_FORMAT = '%b %d, %Y'``: suggested date format
* ``FEED_DOMAIN = SITEURL``
* ``AUTHOR_BIO``, providing a short bio that appears on the side bar.

When developing locally, set the following variable::

    SITEURL = 'http://localhost:8000'

Author
------

Keith Gaughan.

Originally based on the Svbtle theme by William Ting.

License
-------

Released under MIT License, full details in `LICENSE` file.
