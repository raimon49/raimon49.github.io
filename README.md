raimon49.github.io
==================

[![Build Status](https://travis-ci.org/raimon49/raimon49.github.io.svg)](https://travis-ci.org/raimon49/raimon49.github.io)
[![Requirements Status](https://requires.io/github/raimon49/raimon49.github.io/requirements.svg?branch=source)](https://requires.io/github/raimon49/raimon49.github.io/requirements/?branch=source)

My Tech Blog

http://raimon49.github.io/

Setup
-----

Dependencies

* Python 3.6.x (with [pyenv](https://github.com/pyenv/pyenv))
* [Pelican 3.7.x](http://docs.getpelican.com/en/latest/index.html)
    * See my [requirements.in](requirements.in) file

```bash
# Clone this repository
$ git clone --recursive git@github.com:raimon49/raimon49.github.io.git
$ cd raimon49.github.io
$ git branch master origin/master

# Install Python and dependency packages
$ pyenv install 3.6.4
$ pyenv virtualenv 3.6.4 venv-3.6.4-raimon49.github.io
$ pyenv local venv-3.6.4-raimon49.github.io
$ pip install -r requirements.txt

# Check outdated dependency packages
$ pip-compile --no-header -U requirements.in
$ git diff --exit-code

# Update dependency packages
$ pip-compile --no-header -U requirements.in && pip-sync
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
$ invoke rebuild

# go publish
$ ghp-import output -b master
$ git push --all origin
```
