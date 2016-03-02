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

LINKS = (
    ('Github', 'https://github.com/kgaughan/'),
    ('Twitter', 'https://twitter.com/talideon/'),
    ('Main site', 'https://stereochro.me/'),
)

THEME = os.path.join(os.curdir, 'themes', 'svbtle')

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
