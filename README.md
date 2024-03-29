raimon49.github.io
==================

[![Python test](https://github.com/raimon49/raimon49.github.io/workflows/Python%20test/badge.svg)](https://github.com/raimon49/raimon49.github.io/actions?query=workflow%3A%22Python+test%22)

My Tech Blog

https://raimon49.github.io

Setup
-----

Dependencies

* Python 3.9.x (with [asdf-python](https://github.com/danhper/asdf-python))
* [Pelican 4.x](http://docs.getpelican.com/en/latest/index.html)
    * See my [requirements.in](requirements.in) file

```bash
# Clone this repository
$ git clone --recursive git@github.com:raimon49/raimon49.github.io.git
$ cd raimon49.github.io
$ git branch master origin/master

# Install Python and dependency packages
$ asdf install python 3.9.13
$ asdf global python 3.9.13
$ python3 -m venv venv/raimon49.github.io
$ source venv/raimon49.github.io/bin/activate
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
