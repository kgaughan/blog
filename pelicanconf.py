#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

from html.parser import HTMLParser
import os
import os.path
import re
import sys

import markupsafe


COLLAPSE = re.compile(r"\s+", re.MULTILINE)


class TagStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.collected = []

    def get_data(self) -> str:
        return "".join(self.collected)

    def handle_data(self, data: str):
        self.collected.append(data)

    @staticmethod
    def strip_tags(doc: str) -> str:
        stripper = TagStripper()
        stripper.feed(doc)
        return COLLAPSE.sub(" ", stripper.get_data()).strip()


def social(url, svg):
    return (markupsafe.Markup(svg), url)


JINJA_FILTERS = {
    "strip_tags": TagStripper.strip_tags,
}


AUTHOR = "Keith Gaughan"
SITENAME = AUTHOR
TAGLINE = "100% guaranteed AI-free organic content or your money back!"
SITEURL = "."

SLUGIFY_SOURCE = "basename"

PATH = "content"

TIMEZONE = "Europe/Dublin"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

DEFAULT_METADATA = {
    "status": "draft",
}

LINKS = [
    ("Inklings", "https://talideon.com/inklings/"),
]

# All SVGs: Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc.
SOCIAL = [
    social(
        "https://stackoverflow.com/users/8342/keith-gaughan",
        '<svg xmlns="http://www.w3.org/2000/svg" height="1em" width="1em" viewBox="0 0 384 512"><title>Stack Overflow</title><path d="M290.7 311L95 269.7 86.8 309l195.7 41zm51-87L188.2 95.7l-25.5 30.8 153.5 128.3zm-31.2 39.7L129.2 179l-16.7 36.5L293.7 300zM262 32l-32 24 119.3 160.3 32-24zm20.5 328h-200v39.7h200zm39.7 80H42.7V320h-40v160h359.5V320h-40z"/></svg>',
    ),
    social(
        "https://www.linkedin.com/in/keithgaughan",
        '<svg xmlns="http://www.w3.org/2000/svg" height="1em" width="1em" viewBox="0 0 448 512"><title>LinkedIn</title><path d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>',
    ),
    social(
        "https://github.com/kgaughan/",
        '<svg xmlns="http://www.w3.org/2000/svg" height="1em" width="1em" viewBox="0 0 496 512"><title>Github</title><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>',
    ),
]

PLUGIN_PATHS = [os.path.abspath("plugins")]
sys.path += PLUGIN_PATHS

import page_hierarchy
import readtime

PLUGINS = [
    page_hierarchy,
    readtime,
    "more_categories",
    "series",
    "sitemap",
]

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.attr_list": {},
        "markdown.extensions.def_list": {},
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.admonition": {},
    },
    "output_format": "html5",
}

DOCUTILS_SETTINGS = {
    "restructuredtext parser": {"smart_quotes": True},
    "html5 writer": {"table_style": "colwidths-auto"},
}

# fmt: off
STATIC_PATHS = [
    "images",
    "extra/robots.txt",
    "extra/favicon.ico",
]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/favicon.ico": {"path": "favicon.ico"},
}
# fmt: on

THEME = os.path.join(os.curdir, "themes", "air-and-fire")

SITEMAP = {"format": "xml"}

DEFAULT_PAGINATION = 20

# Pages to disable.
ARCHIVES_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
TAGS_SAVE_AS = ""
TAG_SAVE_AS = ""

ARTICLE_PATHS = ["blog"]
PAGE_PATHS = ["pages"]

DEFAULT_DATE_FORMAT = "%d %B %Y"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
CATEGORIES_URL = "categories/"
CATEGORIES_SAVE_AS = "categories/index.html"
CATEGORY_URL = "categories/{slug}/"
CATEGORY_SAVE_AS = "categories/{slug}/index.html"

TYPOGRIFY = True
