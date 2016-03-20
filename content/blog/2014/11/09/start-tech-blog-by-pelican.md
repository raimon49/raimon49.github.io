Title: 技術ブログを静的ページジェネレータPelicanで始めることにした
Date: 2014-11-09 18:44:37
Category: Python
Tags: GitHub, Pelican, Python
Slug: start-tech-blog-by-pelican
Authors: raimon
Summary: 技術ブログを静的ページジェネレータPelicanで始めることにしたのでメモ

技術ブログを静的ページジェネレータPelicanで始めることにしたのでセットアップ手順のメモとかを残す。

## 2015-04-19追記

最新のセットアップ手順は、このブログ自身の[リポジトリトップに置いてあるREADME.md](https://github.com/raimon49/raimon49.github.io/blob/source/README.md)に簡潔にまとめてある。

## 動機

もともとウェブ日記ツール[tDiary](http://www.tdiary.org/)を使ってプログラミング系の記事も書いていたのだけど、

* シンタックスハイライトがしんどい
    * [google-code-prettify](https://code.google.com/p/google-code-prettify/)で色付けしているのだが、やはりJavaScriptではしんどい
    * プログラミング言語のサポートも貧弱なので、やはりこの分野ではデファクトスタンダードな[pygments](http://pygments.org/)が使いたい
* プログラミングネタはMarkdownで書きたい
    * tDiaryにもMarkdownで書く設定があるが、違う道具も使ってみたかった
    * ファイル名 `*.md` だと使い慣れてるVimでサクサクと書けるので是非やりたい

といった理由により、GitHub Pagesにホスティングして別ブログを始めたいと考えた。

## GitHub Pagesの準備

あらかじめGitHub側に `{username}.github.io.git` という名前のリポジトリを作っておく。

手元に持って来て、ここを作業ディレクトリにする。GitHub Pagesとして公開するページとPelican作業用ディレクトリとで内容が一致できないので、 `source` というブランチで公開ページの元となるMarkdownファイルを管理して行く事にした。これが正しいやり方なのか良く分からない。

```bash
$ git clone git@github.com:raimon49/raimon49.github.io.git
$ cd raimon49.github.io
$ git checkout -b source
```

## Pelican環境のセットアップ

以下のページを参考にPelican 3.5.0の環境をセットアップした。

* [Pelican 3.5.0](http://docs.getpelican.com/en/3.5.0/)
* [Pelican + Markdown + GitHub Pagesで管理するブログの作り方 - blog@sotm.jp](http://blog.sotm.jp/2014/01/04/Pelican-Markdown-GithubPages-install-guide/ "Pelican + Markdown + GitHub Pagesで管理するブログの作り方 - blog@sotm.jp")

まずPython 2.7系でPelican用のvirtualenv環境を作る。

```bash
$ pyenv virtualenv 2.7.8 venv-2.7.8-pelican
$ pyenv local venv-2.7.8-pelican
```

依存するパッケージのインストール。

`Makefile` と一緒に `fabfile.py` も作ってくれるらしいので、Fabricも入れてみることにした。

```bash
$ pip install pelican markdown fabric
$ pip list
blinker (1.3)
docutils (0.12)
ecdsa (0.11)
Fabric (1.10.0)
feedgenerator (1.7)
Jinja2 (2.7.3)
Markdown (2.5.1)
MarkupSafe (0.23)
paramiko (1.15.1)
pelican (3.5.0)
pip (1.5.6)
pycrypto (2.6.1)
Pygments (1.6)
python-dateutil (2.2)
pytz (2014.9)
setuptools (3.6)
six (1.8.0)
Unidecode (0.04.16)
wsgiref (0.1.2)
```

`pelican-quickstart` というコマンドで質問に答えてテンプレートを生成する。

ほとんどデフォルトの回答にした。

```bash
$ pelican-quickstart
Welcome to pelican-quickstart v3.5.0.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.


> Where do you want to create your new web site? [.] .
> What will be the title of this web site? Steel Dragon 14106
> Who will be the author of this web site? raimon
> What will be the default language of this web site? [en] ja
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) y
> What is your URL prefix? (see above example; no trailing slash) http://raimon49.github.io
> Do you want to enable article pagination? (Y/n) y
> How many articles per page do you want? [10] 10
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) y
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) y
> Do you want to upload your website using FTP? (y/N) n
> Do you want to upload your website using SSH? (y/N) n
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
Done. Your new project is available at /home/raimon49/works/git/raimon49.github.io
```

生成された `pelicanconf.py` というファイルを自分用に編集する。

変更・追加したのは以下の辺り。

```python
# Atom/RSS Feedの生成に必要
SITEURL = 'http://raimon49.github.io'
# SITEURLが指定されているとローカルサーバでもリンクに使われてしまうので
# ローカルサーバのプレビュー時は相対リンクするように指定
RELATIVE_URLS = True

# SITEURL/YYYY/MM/DD/Markdown fileというルールでURLを発行
ARTICLE_PATHS = ['blog']
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

# ブログ記事の日付フォーマットを指定
TIMEZONE = 'Asia/Tokyo'
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'ja': '%Y-%m-%d(%a)',
}

# ブログのデザインテーマを指定（後述）
THEME = './vendor/pelican-sober'

# ブログのRSSフィードを全文配信
FEED_ALL_RSS = 'feeds/all.rss.xml'

# Social widget
SOCIAL = (('GitHub', 'https://github.com/raimon49'),
          ('Twitter', 'https://twitter.com/raimon49'),
          ('Last.fm', 'http://www.lastfm.jp/user/raimon_49'),
          ('Website', 'http://sangoukan.xrea.jp/'),)

```

ブログのデザインテーマは `pelican-themes` というコマンドラインツールを使って管理できるみたいだけど、まぁ気に入ったものをGitHubから持って来て使えば途中で変更することも無いかなと考えて、submoduleとして追加して参照することにした。

```bash
$ git submodule add git://github.com/fle/pelican-sober.git vendor/pelican-sober
```

## ブログ記事の投稿とページ生成

後は `content/blog-title.md` みたいな感じで好きなテキストエディタで記事を書けば良いようだ。

記事に埋め込むメタデータについては[Writing content](http://docs.getpelican.com/en/3.5.0/content.html)の章を参考にする。

HTMLの生成とローカルサーバでの確認は `Makefile` または `fabfile.py` を利用すると簡単。

```bash
$ make html
$ make serve

$ fab build
$ fab serve

# 2つをまとめてやってくれる
$ fab reserve
```

ローカルでの確認が終わったら[Tips - Publishing to GitHub](http://docs.getpelican.com/en/3.5.0/tips.html)を参考にGitHub Pagesに記事をpushする。

```bash
$ fab rebuild
[localhost] local: rm -rf output
[localhost] local: mkdir output
[localhost] local: pelican -s pelicanconf.py
Done: Processed 1 article(s), 0 draft(s) and 0 page(s) in 0.15 seconds.

# 現在のoutputディレクトリの内容をgh-pagesというローカルブランチに反映する
$ pip install ghp-import
$ ghp-import output

# コミットされた内容をリモートpushする
$ git checkout gh-pages
$ git push -f origin gh-pages:master
```

`ghp-import -b master` みたいにブランチ名を指定した方が楽かもしれない。

`source` ブランチと `master` ブランチは全く別の歴史を持って行くので混ぜるな危険な感じになってしまった。記事生成元データは別リポジトリとして管理する方がベターなのかな。

よって更新手順としては以下のようなフローとなる

```bash
# sourceブランチで記事を編集
$ git checkout source
$ vim content/blog/2014/11/09/start-tech-blog-by-pelican.md
$ git commit -a
$ git push origin source

# GitHub Pagesに反映
$ fab rebuild
$ ghp-import
$ git checkout gh-pages
$ git push gh-pages:master
```

ローカルブランチを切り替えるのは面倒なので、この辺はコミットフックを使って自動化するのが良いかも知れない。

はてなスターとか設置したいんだけど今日は疲れたのでこれまで。
