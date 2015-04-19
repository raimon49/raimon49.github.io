raimon49.github.io
==================

My Tech Blog

http://raimon49.github.io/

Setup
-----

Dependencies

* Python 2.7.x (with [pyenv](https://github.com/yyuu/pyenv))
* [Pelican 3.5.0](http://docs.getpelican.com/en/latest/index.html)

```bash
# clone this repository
$ git clone --recursive git@github.com:raimon49/raimon49.github.io.git
$ cd raimon49.github.io
$ git branch master origin/master

# install Python and dependency packages
$ pyenv install 2.7.9
$ pyenv virtualenv 2.7.9 venv-2.7.9-pelican
$ pyenv local venv-2.7.9-pelican
$ pip install -r requirements.txt
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
