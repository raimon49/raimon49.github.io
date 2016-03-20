Title: Homebrewでインストール済みパッケージが更新後に「already installed, it's just not linked」と言われた時の対応
Date: 2014-11-18 23:05:00
Category: Mac
Tags: Homebrew, Mac, Mercurial
Slug: homebrew-bottle-mercurial
Authors: raimon
Summary: Homebrewでインストール済みパッケージが更新後に「already installed, it's just not linked」と言われた時に解消した方法のメモ。

少しの間触っていなかったMac miniで、パッケージ管理ツールHomebrewで入れているコマンド群を `brew update && brew upgrade` を実行したところ、分散バージョン管理システムMercurialの `hg` コマンドを実行しようとすると「already installed, it's just not linked」怒られるようになってしまった。

## 対応方法

次のように `brew link` を実行したら、 最新の `hg` コマンドが使えるように解決した。

```bash
$ brew link --overwrite mercurial
```

## 原因

多分だけど、HomebrewのMercurialパッケージがbottle化されたことが原因のように考えられる。

bottleというのは、いわゆるaptやyumのようなバイナリ配布形式で、Mercurial 2.xまでは `brew install mercurial` を実行した時はソースコードをダウンロードして来てビルドする挙動だったように記憶している。これがバイナリ配布形式に変わって、 `brew link --overwrite` が必要になったのではないか。現に[Formula/mercurial.rbのコミットログ](https://github.com/Homebrew/homebrew/commits/master/Library/Formula/mercurial.rb)を参照すると、Mercurial 3.0.1前後にbottle云々というものが登場する。

Homebrewも使い始めた頃は大半のパッケージが手元でビルドされていて、単なるMakefileラッパー + 管理システムのような印象のツールだったけど、2014-11現在ではbottleとしてバイナリ配布されるパッケージが増えているのを感じる。サクサクと短い時間でインストールが完了するようになって便利だ。
