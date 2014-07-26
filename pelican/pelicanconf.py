#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'lostman/ごる'
SITENAME = 'blog.gorugle.org'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

# Social widget
SOCIAL = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}.html'

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'misc'

DEFAULT_DATE_FORMAT = '%Y/%m/%d %a'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['better_figures_and_images']

# for better_figures_and_images
RESPONSIVE_IMAGES = True
STATIC_IMAGES_PATH = '.'

THEME = 'themes/pelican-bootstrap3'

USE_OPEN_GRAPH = False
