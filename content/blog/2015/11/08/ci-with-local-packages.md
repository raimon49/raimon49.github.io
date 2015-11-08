Title: Ruby/Pythonで依存パッケージをローカルインストールして開発環境構築やCIビルドを高速化する
Date: 2015-11-08 15:45:17
Modified:
Category: Git
Tags: CI, Git, GitHub, Ruby, Python
Slug: ci-with-local-packages
Authors: raimon
Summary: RubyGemsやPython PackageをGitリポジトリで管理しておくことで、ローカルインストールして開発環境構築やCIビルドが高速化できる。

一般的にRuby/Pythonで書かれたアプリケーションの依存パッケージはBundler/pipでインストールされるが、[rubygems.org](https://rubygems.org/)や[Python Package Index](https://pypi.python.org/pypi)からの取得・展開に時間がかかり、またこれらの中央サーバがまれにダウンしていると何もできなくなってしまうケースがある。

回避策の一つとして、依存パッケージをGitリポジトリに飲んでしまい、パッケージリポジトリとは通信せずローカルインストールで済ませる、いわゆるvendoring（ベンダリング）と呼ばれる方法がある。

## サンプルリポジトリ

それぞれのサンプルとなるGitリポジトリをGitHubに作成した。

* [ruby-local-gems-sample](https://github.com/raimon49/ruby-local-gems-sample)
* [python-local-wheels-sample](https://github.com/raimon49/python-local-wheels-sample)

## Ruby + Bundlerの場合

Ruby + Bundlerの場合 `Gemfile` に依存パッケージを宣言し、`bundle package` コマンドでローカルに保存できる。

インストールの場所は慣例的に `vendor` 以下が使われる。

```sh
# 依存パッケージの宣言
$ cat Gemfile
source "https://rubygems.org"

gem "minitest"
gem "minitest-reporters"

# 依存パッケージのインストール
$ bundle install --path vendor/bundle

# 依存パッケージをローカルに保存
$ bundle package --all
```

保存された `*.gem` ファイルは[vendor/cache](https://github.com/raimon49/ruby-local-gems-sample/tree/master/vendor/cache)以下に管理される。

GitHubのCreate New repository画面でRuby用の `.gitignore` ファイルを自動生成している時は、このキャッシュファイルがバージョン管理下に置かれるよう設定を1行追加すると良い。

```diff
diff --git a/.gitignore b/.gitignore
index 28f4849..9c7d638 100644
--- a/.gitignore
+++ b/.gitignore
@@ -23,6 +23,7 @@ build/
 ## Environment normalisation:
 /.bundle/
 /vendor/bundle
+!/vendor/cache/*.gem
 /lib/bundler/man/

```

上記の設定を追加することで、ローカル `*.gem` ファイルをバージョン管理の対象として追加できるようになる。

```sh
$ git add vendor/cache
$ git commit -m  'Packaging Gems'
```

依存パッケージが全てGitリポジトリに含まれるようになったため、開発メンバーやCI環境ではこのファイルを使って `--local` オプションを指定することでローカルインストールが可能になった。

```sh
$ git clone git://github.com/raimon49/ruby-local-gems-sample.git
$ cd ruby-local-gems-sample
$ bundle install --path vendor/bundle --local
```

例としてTravis CIでローカルインストールを使う設定を載せておく。

```yaml
install:
  bundle install --path vendor/bundle --local
```

ローカルインストールを使って[CIビルドを走らせる](https://travis-ci.org/raimon49/ruby-local-gems-sample)と、`bundle install` は1秒かからず完了していることが分かる。

## Python + pipの場合

Pythonの場合はpipと[wheel](https://pypi.python.org/pypi/wheel)パッケージの組み合わせによって `pip wheel` コマンドが使えるようになり、ローカルに保存できる。

インストールの場所は慣例的に `wheelhouse` 以下が使われる。

```sh
# 依存パッケージをインストール
$ pip install [Package A] [Package B]...

# 依存パッケージの書き出し
$ pip freeze > requirements.txt

# 依存パッケージをローカルに保存
$ pip install wheel
$ pip wheel -r requirements.txt
$ git add wheelhouse
$ git commit -m 'Packaging wheels'
```

依存パッケージが全てGitリポジトリに含まれるようになったため、開発メンバーやCI環境ではこのファイルを使って `--no-index -f wheelhouse` オプションを指定することでローカルインストールが可能になった。

```sh
$ git clone git://github.com/raimon49/python-local-wheels-sample.git
$ cd python-local-wheels-sample
$ python-local-wheels-samplp install -r requirements.txt --no-index -f wheelhouse
```

例としてTravis CIでローカルインストールを使う設定を載せておく。

```yaml
install:
  - pip install -r requirements.txt --no-index -f wheelhouse
```

ローカルインストールを使って[CIビルドを走らせる](https://travis-ci.org/raimon49/python-local-wheels-sample)と、`pip install` は1秒かからず完了していることが分かる。

## まとめ

RubyやPythonで書かれたアプリケーションの依存パッケージをvendoringで管理する方法で、開発環境構築やCIビルドを高速に行うことができる。

高速化の他にも、開発サーバやプロダクションサーバからのHTTP/HTTPS通信先が絞られているケースや、デプロイを公式パッケージリポジトリのダウン影響を受けず安定化させる効果も期待できる。

一方で、依存パッケージを丸ごとGitリポジトリに飲むのは、リポジトリサイズの肥大化という面で、ある意味で富豪的なアプローチであると言える。チーム・組織のサイズによって、例えばパッケージリポジトリのミラーを立ち上げるといった別の方法が適している事も十分に考えられる。

この記事では例としてTravis CIでのビルドにローカルインストールを利用しているが、Travis CIを使っていてCIビルドの時間を短縮化したいだけなら[Caching Dependencies and Directories機能](http://docs.travis-ci.com/user/caching/)を使っておくのも良い（CircleCIにもYAMLでの書式は違うが同様の機能がある）。
