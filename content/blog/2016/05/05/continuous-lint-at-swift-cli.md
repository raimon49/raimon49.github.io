Title: Swift CLI環境におけるTravis CIを利用した継続的Lint
Date: 2016-05-05 13:02:17
Category: Xcode
Tags: CI, Swift, Xcode
Slug: continuous-lint-at-swift-cli
Authors: raimon
Summary: Swift CLIで動作させているコードの継続的LintをTravis CIで行う

Xcodeに付属する `swift` コマンドを使い、[『詳解 Swift 改訂版』](http://www.sbcr.jp/products/4797386257.html)のサンプルコードを写経したり、書き換えて動作を確認したりするGitリポジトリを作った。

せっかくGitHubにホスティングしているので、学習しながら継続的に[SwiftLint](https://github.com/realm/SwiftLint)で好ましくない書き方を自動検知できると良いのではないかと考えた。

## 成果物

* [raimon49/swift-definitive-guide-2nd-edition-study](https://github.com/raimon49/swift-definitive-guide-2nd-edition-study)

最低限で必要になるのは次のファイルである。

```sh
.
|-- .swiftlint.yml
|-- .travis.yml
`-- install_swiftlint.sh
```

## インストールスクリプトの準備

Travis CIのビルド環境へSwiftLintを導入する最速の手段は、[リリース済みpkgファイル](https://github.com/realm/SwiftLint/releases)を取得し、OS Xの `installer` コマンドでインストールする方法である。

よって、次のようなインストールスクリプト `install_swiftlint.sh` を準備する。スクリプトファイルには実行権限を付与するようにし、スクリプト中の変数 `SWIFTLINT_PKG_URL` は都度でSwiftLintの最新リリースに変えると良い。

pkgファイルが取得できなかった時は代替手段としてソースコードをcloneしてコンパイルさせるが、時間がかかる。

```sh
#!/bin/bash

# Installs the SwiftLint package.
# Tries to get the precompiled .pkg file from Github, but if that
# fails just recompiles from source.

set -e

SWIFTLINT_PKG_PATH="/tmp/SwiftLint.pkg"
SWIFTLINT_PKG_URL="https://github.com/realm/SwiftLint/releases/download/0.10.0/SwiftLint.pkg"

wget --output-document=$SWIFTLINT_PKG_PATH $SWIFTLINT_PKG_URL

if [ -f $SWIFTLINT_PKG_PATH ]; then
  echo "SwiftLint package exists! Installing it..."
  sudo installer -pkg $SWIFTLINT_PKG_PATH -target /
else
  echo "SwiftLint package doesn't exist. Compiling from source..." &&
  git clone https://github.com/realm/SwiftLint.git /tmp/SwiftLint &&
  cd /tmp/SwiftLint &&
  git submodule update --init --recursive &&
  sudo make install
fi
```

もしpkgファイル経由比でおよそ3倍のインストールに時間を許容できるなら、インストールスクリプトでは単にHomebrew経由で導入する方法もある。メリットとしては、ソースコード取得からのコンパイルと同様に、常に最新のリリース版が利用できる。

```sh
# 最新リリースのビルド済みバイナリからインストール
$ brew update && brew install swiftlint

# 最新のソースコードからコンパイルしてインストール
$ brew update && brew install --HEAD swiftlint
```

## SwiftLintとTravis CIの設定を追加

『詳解 Swift 改訂版』に登場するサンプルコードでは、変数名に1文字の名前やユニコード文字列が多用されており、SwiftLintでエラーとなってしまうため、回避する設定を `.swiftlint.yml` として追加した。

```yml
disabled_rules:
  - variable_name
```

ここまで準備した内容で `git push` される度にSwiftLintでチェックが走るよう、Travis CI側のWeb UIでリポジトリ連携を設定し `.travis.yml` を次のような内容で追加する。

```yml
language: objective-c
osx_image: xcode7.3

install:
  - ./install_swiftlint.sh

script:
  - swiftlint
```

[Travis CIでSwiftLintの結果が継続的に確認できるようになった](https://travis-ci.org/raimon49/swift-definitive-guide-2nd-edition-study)ら、好ましくないコードスタイルを都度修正し、常にチェック結果がグリーンを保つようにする。

## 参考情報

* [Setting up SwiftLint on Travis CI - Alex Plescan](https://alexplescan.com/posts/2016/03/03/setting-up-swiftlint-on-travis-ci/)
