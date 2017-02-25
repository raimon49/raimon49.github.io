Title: Ubuntu 16.04 LTSにシステムワイドでNeovimとPythonパッケージneovimをインストール
Date: 2017-02-25 22:42:00
Category: Vim
Tags: Python, Ubuntu, Vim
Slug: install-neovim-in-ubuntu1604
Authors: raimon
Summary: Ubuntu 16.04 LTSにaptパッケージ版のNeovimとPyPIから配信されているPythonクライアントをインストールし、Neovim用のプラグインであるdeopleteが使えるようにする

Ubuntu ServerにNeovimをインストールし、[deoplete](https://github.com/Shougo/deoplete.nvim)が動作するようPythonクライアントもシステムワイドで使えるようにした。

## 環境

```sh
$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.2 LTS"
```

## PPAリポジトリからNeovimの開発版をインストール

Ubuntu向けのビルドバイナリパッケージでは `stable` か `unstable` かをユーザーが選択して導入できる。ここでは開発中の最新版である `unstable` をインストールした。

また、後述するPythonクライアントを導入するために、Python 3関連のaptパッケージも一緒に入れておく。

```sh
$ sudo apt-get install software-properties-common python3-dev python3-pip
$ sudo add-apt-repository ppa:neovim-ppa/unstable
$ sudo apt-get update
$ sudo apt-get install neovim

$ nvim --version
NVIM 0.2.0-dev
```

## Pythonクライアントをシステムワイドにインストール

NeovimのPythonクライアントはPythonパッケージマネージャのpipでシステムワイドにインストールする。

```sh
$ sudo pip3 install -U pip
$ sudo pip3 install neovim

$ pip3 show neovim
Name: neovim
Version: 0.1.12
Summary: Python client to neovim
```

Neovimを起動してコマンドラインモードで確認すると `1` が返るようになっていれば目的は達している。

```vim
:echo has('python3')
```
