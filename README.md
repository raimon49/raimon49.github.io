raimon49.github.io
==================

[![Build Status](https://travis-ci.org/raimon49/raimon49.github.io.svg)](https://travis-ci.org/raimon49/raimon49.github.io)
[![Requirements Status](https://requires.io/github/raimon49/raimon49.github.io/requirements.svg?branch=source)](https://requires.io/github/raimon49/raimon49.github.io/requirements/?branch=source)

My Tech Blog

http://raimon49.github.io/

Setup
-----

Dependencies

* Python 2.7.x (with [pyenv](https://github.com/yyuu/pyenv))
* [Pelican 3.7.x](http://docs.getpelican.com/en/latest/index.html)
    * See my [requirements.in](requirements.in) file

```bash
# Clone this repository
$ git clone --recursive git@github.com:raimon49/raimon49.github.io.git
$ cd raimon49.github.io
$ git branch master origin/master

# Install Python and dependency packages
$ pyenv install 2.7.11
$ pyenv virtualenv 2.7.11 venv-2.7.11-pelican
$ pyenv local venv-2.7.11-pelican
$ pip install -r requirements.txt

# Check outdated dependency packages
$ pip-compile -U -n requirements.in | diff -u requirements.txt -

# Update dependency packages
$ pip-compile -U requirements.in && pip-sync
```

Develop
-------

Set use relative URLs at [pelicanconf.py](pelicanconf.py) (Do **NOT** commit)

```diff
-RELATIVE_URLS = False
+RELATIVE_URLS = True
```

Publish
-------

```bash
# checkout stable configure and rebuild
$ git checkout pelicanconf.py
$ fab rebuild

# go publish
$ ghp-import output -b master
$ git push --all origin
```
