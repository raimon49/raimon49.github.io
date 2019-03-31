#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'raimon'
SITENAME = 'Steel Dragon 14106'
SITEURL = 'http://raimon49.github.io'

PATH = 'content'
ARTICLE_PATHS = ['blog']
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'ja': '%Y-%m-%d(%a)',
}

DISQUS_SITENAME = 'steeldragon14106'

THEME = './vendor/nest'

# Feed generation is usually not desired when developing
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Information about raimon',
          'http://raimon49.github.io/my-portfolio/'),
         ('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('GitHub', 'https://github.com/raimon49'),
          ('Twitter', 'https://twitter.com/raimon49'),
          ('Last.fm', 'https://www.last.fm/user/raimon_49'),
          ('Website', 'http://sangoukan.xrea.jp/'),)

DEFAULT_PAGINATION = 10

# NEST Template
SITESUBTITLE = 'スチールドラゴンアイシテル'
# Minified CSS
NEST_CSS_MINIFY = False
# Add items to top menu before pages
MENUITEMS = [('Categories', '/categories.html')]
# Add header background image from content/images : 'background.jpg'
NEST_HEADER_IMAGES = ''
NEST_HEADER_LOGO = '/images/exchange32.png'
# Footer
NEST_SITEMAP_COLUMN_TITLE = 'Sitemap'
NEST_SITEMAP_MENU = [('Archives', '/archives.html'),
                     ('Tags', '/tags.html'),
                     ('Authors', '/authors.html')]
NEST_SITEMAP_ATOM_LINK = 'Atom Feed'
NEST_SITEMAP_RSS_LINK = 'RSS Feed'
NEST_SOCIAL_COLUMN_TITLE = 'Social'
NEST_LINKS_COLUMN_TITLE = 'Links'
NEST_COPYRIGHT = '&copy; raimon 2014-2019'
# index.html
NEST_INDEX_HEAD_TITLE = 'Homepage'
NEST_INDEX_HEADER_TITLE = 'スチールドラゴンアイシテル'
NEST_INDEX_HEADER_SUBTITLE = '絶叫マシンが好きなエンジニアの技術ブログ'
NEST_INDEX_CONTENT_TITLE = 'Last Posts'
# archives.html
NEST_ARCHIVES_HEAD_TITLE = 'Archives'
NEST_ARCHIVES_HEAD_DESCRIPTION = 'Posts Archives'
NEST_ARCHIVES_HEADER_TITLE = 'Archives'
NEST_ARCHIVES_HEADER_SUBTITLE = 'Archives for all posts'
NEST_ARCHIVES_CONTENT_TITLE = 'Archives'
# article.html
NEST_ARTICLE_HEADER_BY = 'By'
NEST_ARTICLE_HEADER_MODIFIED = 'modified'
NEST_ARTICLE_HEADER_IN = 'in category'
# author.html
NEST_AUTHOR_HEAD_TITLE = 'Posts by'
NEST_AUTHOR_HEAD_DESCRIPTION = 'Posts by'
NEST_AUTHOR_HEADER_SUBTITLE = 'Posts archives'
NEST_AUTHOR_CONTENT_TITLE = 'Posts'
# authors.html
NEST_AUTHORS_HEAD_TITLE = 'Author list'
NEST_AUTHORS_HEAD_DESCRIPTION = 'Author list'
NEST_AUTHORS_HEADER_TITLE = 'Author list'
NEST_AUTHORS_HEADER_SUBTITLE = 'Archives listed by author'
# categories.html
NEST_CATEGORIES_HEAD_TITLE = 'Categories'
NEST_CATEGORIES_HEAD_DESCRIPTION = 'Archives listed by category'
NEST_CATEGORIES_HEADER_TITLE = 'Categories'
NEST_CATEGORIES_HEADER_SUBTITLE = 'Archives listed by category'
# category.html
NEST_CATEGORY_HEAD_TITLE = 'Category Archive'
NEST_CATEGORY_HEAD_DESCRIPTION = 'Category Archive'
NEST_CATEGORY_HEADER_TITLE = 'Category'
NEST_CATEGORY_HEADER_SUBTITLE = 'Category Archive'
# pagination.html
NEST_PAGINATION_PREVIOUS = 'Previous'
NEST_PAGINATION_NEXT = 'Next'
# period_archives.html
NEST_PERIOD_ARCHIVES_HEAD_TITLE = 'Archives for'
NEST_PERIOD_ARCHIVES_HEAD_DESCRIPTION = 'Archives for'
NEST_PERIOD_ARCHIVES_HEADER_TITLE = 'Archives'
NEST_PERIOD_ARCHIVES_HEADER_SUBTITLE = 'Archives for'
NEST_PERIOD_ARCHIVES_CONTENT_TITLE = 'Archives for'
# tag.html
NEST_TAG_HEAD_TITLE = 'Tag archives'
NEST_TAG_HEAD_DESCRIPTION = 'Tag archives'
NEST_TAG_HEADER_TITLE = 'Tag'
NEST_TAG_HEADER_SUBTITLE = 'Tag archives'
# tags.html
NEST_TAGS_HEAD_TITLE = 'Tags'
NEST_TAGS_HEAD_DESCRIPTION = 'Tags List'
NEST_TAGS_HEADER_TITLE = 'Tags'
NEST_TAGS_HEADER_SUBTITLE = 'Tags List'
NEST_TAGS_CONTENT_TITLE = 'Tags List'

RELATIVE_URLS = False
