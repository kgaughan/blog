#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

import os
import os.path


AUTHOR = u'Keith Gaughan'
SITENAME = u"Can't Hack"
TAGLINE = "...but trying to"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Dublin'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

DEFAULT_METADATA = {
    'status': 'draft',
}

LINKS = (
    ('Main site', 'https://stereochro.me/'),
)

SOCIAL = (
    ('Github', 'https://github.com/kgaughan/'),
    ('Twitter', 'https://twitter.com/talideon/'),
)

PLUGIN_PATHS = [os.path.abspath('../pelican-plugins')]
PLUGINS = [
    # See: https://github.com/getpelican/pelican-plugins/tree/master/code_include
    'code_include',
    # https://github.com/getpelican/pelican-plugins/tree/master/headerid
    'headerid',
    # See: https://github.com/getpelican/pelican-plugins/tree/master/sitemap
    'sitemap',
]

STATIC_PATHS = (
    'images',
    'extra/robots.txt',
)
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}

THEME = os.path.join(os.curdir, 'themes', 'svbtle')

SITEMAP = {
    'format': 'xml',
}

DEFAULT_PAGINATION = 20

# Pages to disable.
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
