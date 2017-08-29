Title: swiftenvを利用してLinux環境でSwiftモジュール開発の準備
Date: 2017-08-29 21:49:37
Category: Linux
Tags: Swift, Ubuntu
Slug: start-develop-swift-in-linux-with-swfitenv
Authors: raimon
Summary: Linux環境でSwiftモジュール開発を始めるための準備としてswiftenvを導入した時の覚え書き

## Linux環境におけるSwift

Linux環境でSwiftモジュールやSwiftコマンドラインツールを開発したい場合、2017-08現在、次の64bit OS環境が必要である。

* Ubuntu 14.04
* Ubuntu 16.04
* Ubuntu 16.10

その上で、さらに[Swift.org: Download Swift](https://swift.org/download/)に書かれている通り、実行バイナリを自分で設置してPATHを通すと利用可能になる。

Swift本体は開発が活発で、有効なバージョンが多く存在するため、Linux環境でSwiftモジュールやSwiftコマンドラインツールを開発したければ[swiftenv](https://github.com/kylef/swiftenv)を導入しておくと良い。

## swiftenvの導入

導入にあたっては、まずswiftenvをGitリポジトリから手元のHOME以下に設置する。

```sh
$ git clone https://github.com/kylef/swiftenv.git ~/.swiftenv
```

また、シェル起動時に `swiftenv` コマンドにPATHが通るよう `.bash_profile` や `.zshenv` といったシェル設定ファイルに設定を追記する。

```sh
export SWIFTENV_ROOT="$HOME/.swiftenv"
export PATH="${SWIFTENV_ROOT}/bin:${PATH}"
eval "$(swiftenv init -)"
```

## Swift本体のインストールと利用

swiftenvを導入したら `install` サブコマンドで利用したいバージョンのSwift本体をインストールする。

```sh
# Swift 3.1.1をインストール
$ swiftenv install 3.1.1

# インストールされているバージョンと現在有効になっているバージョンの確認
$ swiftenv versions
* 3.1.1 (set by /home/raimon49/.swiftenv/version)
```

これでLinux環境でもSwiftが利用できるようになった。

例えばSwift Package Managerで新しくモジュール開発を始めるコマンドを実行すると、macOSのXcodeに付属しているSwiftで実行した時と同様に、マニフェストファイルやユニットテストの雛形ファイルが生成される。

```sh
$ mkdir MySwiftModule
$ cd MySwiftModule

# Swift Package Manager用の雛形ファイルを生成
$ swift package init
Creating library package: MySwiftModule
Creating Package.swift
Creating .gitignore
Creating Sources/
Creating Sources/MySwiftModule.swift
Creating Tests/
Creating Tests/LinuxMain.swift
Creating Tests/MySwiftModuleTests/
Creating Tests/MySwiftModuleTests/MySwiftModuleTests.swift
```
