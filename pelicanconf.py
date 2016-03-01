#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

import os
import os.path


AUTHOR = u'Keith Gaughan'
SITENAME = u"Can't Hack"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Dublin'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

# Blogroll
LINKS = (
#    ('You can modify those links in your config file', '#'),
)

THEME = os.path.join(os.curdir, 'themes', 'svbtle')

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
