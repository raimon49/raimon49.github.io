Title: github-markdown-toc.goでMarkdown文書の目次を自動生成
Date: 2017-11-27 23:17:12
Category: Go
Tags: Go, Markdown
Slug: generate-toc-for-markdown-document
Authors: raimon
Summary: github-markdown-tocのGo実装を使いMarkdown文書の目次を自動生成する方法

`README.md` をはじめとするMarkdown文書に、見出しへのページ内リンク付きを目次を作りたくなる時が多々ある。

そのような用途に、自分は今まで[github-markdown-toc](https://github.com/ekalinin/github-markdown-toc)というツールを利用してきた。ただ、このツールはシェルスクリプトで実装されており、各種UNIXツールに依存している。

調べてみたところ、Goで実装され、各種UNIXツールへの依存が無くバイナリをインストールするだけで利用できる[github-markdown-toc.go](https://github.com/ekalinin/github-markdown-toc.go)が存在することを知った。今回こちらに乗り換えたので、使い方もまとめておく。

## インストール

github-markdown-toc.goのインストールは[GitHubのReleasesページ](https://github.com/ekalinin/github-markdown-toc.go/releases)から、各プラットフォーム向けに配布されるバイナリを取得するだけである。

例えば64bitのLinuxプラットフォームであれば、2017-11現在、最新であるバージョン0.8.0のバイナリは、次のように取得・インストールする。好みでPATHの通った場所に置いても良いだろう。

```sh
# 取得・展開
$ wget https://github.com/ekalinin/github-markdown-toc.go/releases/download/0.8.0/gh-md-toc.linux.amd64.tgz
$ tar xzf gh-md-toc.linux.amd64.tgz

# インストールされたことを確認
$ ./gh-md-toc --version
0.8.0
```

## 目次生成

目次生成には、標準入力からMarkdown文書の中身を渡す方法と、Markdown文書のファイルパスを指定して目次を追記させる2種類がある。

例えば、[このブログを管理しているGitリポジトリのREADME.md](https://github.com/raimon49/raimon49.github.io/blob/source/README.md)の中身を渡して目次生成を実行すると、次のように出力される。

```sh
$ cat ~/raimon49.github.io/README.md | ./gh-md-toc
* [raimon49\.github\.io](#raimon49githubio)
  * [Setup](#setup)
  * [Develop](#develop)
  * [Publish](#publish)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)
```

デフォルトでは全ての見出しレベルが目次生成の対象となる。これを例えば見出しレベル1に制限したい場合は、オプション `--depth` を指定する。

```sh
$ cat ~/raimon49.github.io/README.md | ./gh-md-toc --depth=1
* [raimon49\.github\.io](#raimon49githubio)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)
```

コマンド実行の引数としてファイルパスを指定しても目次生成できる。オプションの効果も、標準入力で渡す使い方の時と同様である。

```sh
$ ./gh-md-toc --depth=1 ~/raimon49.github.io/README.md

Table of Contents
=================

* [raimon49\.github\.io](#raimon49githubio)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)
```
