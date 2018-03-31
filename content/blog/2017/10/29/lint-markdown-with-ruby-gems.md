Title: Markdown lint toolでMarkdownファイルの構文のLintをチェック
Date: 2017-10-29 21:04:20
Category: Ruby
Tags: CI, Git, Markdown, Ruby
Slug: lint-markdown-with-ruby-gems
Authors: raimon
Summary: Markdown lint toolの利用方法を設定カスタマイズ方法、CIサービスとの連携方法について。

継続的にMarkdownファイルの構文チェックを実施させたい時はRubyの[Markdown lint tool](https://github.com/markdownlint/markdownlint)（以降「Markdownlint」）を利用する。

Lint設定の変更方法や、CIサービスとの連携方法についてまとめる。

## インストール

MarkdownlintはRubyGemsで公開・配布されているため `gem` または `bundle` コマンドを用いてインストールする。

例えば `bundle` であれば、次のように `Gemfile` にRubyGemsでの公開名「mdl」を記述する。

```ruby
source 'https://rubygems.org'

gem 'mdl'
```

Bundlerでローカル環境にインストールする。

```sh
$ bundle install --path vendor/bundle
```

インストール後、Bundlerを通して `mdl` コマンドがローカル環境で実行可能になる。

```sh
$ bundle exec mdl --help
Usage: mdl [options] [FILE.md|DIR ...]
    -c, --config FILE                The configuration file to use
    -g, --git-recurse                Only process files known to git when given a directory
    -i, --[no-]ignore-front-matter   Ignore YAML front matter
    -l, --list-rules                 Don't process any files, just list enabled rules
    -r, --rules RULE1,RULE2          Only process these rules
    -u, --rulesets RULESET1,RULESET2 Specify additional ruleset files to load
    -a, --[no-]show-aliases          Show rule alias instead of rule ID when viewing rules
    -w, --[no-]warnings              Show kramdown warnings
    -d, --skip-default-ruleset       Don't load the default markdownlint ruleset
    -s, --style STYLE                Load the given style
    -t, --tags TAG1,TAG2             Only process rules with these tags
    -v, --[no-]verbose               Increase verbosity
    -h, --help                       Show this message
    -V, --version                    Show version
```

## リンティングの実行

リンティングの実行は、 `mdl` コマンドの引数として、Markdownファイルや文書の存在するディレクトリ名を渡すだけである。

```sh
$ bundle exec mdl docs
```

この時、Markdownlintのチェック設定として、[ツール側の推奨するルール](https://github.com/markdownlint/markdownlint/blob/master/docs/RULES.md)が適用される。

例えば、推奨ルールではリストのインデントにおいて2 spacesを推奨しているため、4 spacesやハードタブを採用しているMarkdown文書では、次のようなエラーが検出される。

```sh
MD007 Unordered list indentation
```

## Lintルールの無視設定やカスタマイズ

自分達のプロジェクトで採用するルールと合わなくて無視したい場合は `mdlrc` というファイルを作成し、無視したいルール名を `~` （チルダ）で明示する。

```sh
rules "~MD007"
```

そしてリンティング実行時に上記の設定ファイルを `-c` オプションに指定すれば良い。複数のルール名を記述したい場合はカンマ区切りで並べれば全てのルールについて有効/無効を指定できる。

```sh
$ bundle exec mdl -c mdlrc docs
```

デフォルトの推奨ルールを全て継承した上で、特定のルールだけ設定を変えたい場合は `style.rb` のようなファイルを作成する。例えばリストのインデントを4 spacesだったら正としてチェックさせたい時は、次の内容となる。

```ruby
all
rule 'MD007', :indent => 4
```

リンティング実行時には、このスタイルファイルを `-s` オプションに指定する。スタイルファイルの詳細は[Creating styles](https://github.com/markdownlint/markdownlint/blob/master/docs/creating_styles.md)を参照のこと。

## CIサービスで自動実行させる

ローカル環境でだけMarkdownファイルをチェックできるだけでも助かるのだが、やはりCIサービスと連携して自動実行させたい。

Travis CIであれば、CI設定ファイル `.travis.yml` は次のような内容になるだろう。無視設定やスタイル設定は `script:` のコマンド行で各々のプロジェクトに合わせて指定させると良い。ここでは例として、先に挙げた4 spaces indentのスタイル設定ルールを採用して自動チェックさせる。

```yaml
language: ruby
rvm:
  - 2.4
script:
  bundle exec mdl -s style.rb docs
```

サンプルとして、このCI設定ファイルを使ってTravis CIと連携し、[Pull Requestを投げたら自動でルール違反が検出され、修正後にCIジョブをPassしてマージされるまでの流れ](https://github.com/raimon49/use-markdownlint-sample/pull/1)を記録に残した。

## まとめ

* MarkdownのLintにはRubyGemsで公開・配布されているMarkdown lint toolが活用できる
* デフォルトルールで無視したい設定は `mdlrc` で、カスタマイズしたいスタイル設定は `style.rb` で指定できる
* CIサービスと連携することで、ブランチやPull Requestの内容を自動チェックできる

## 他の実装

* Python実装として[pymarkdownlint](https://github.com/jorisroovers/pymarkdownlint)が存在するが、Ruby版の移植途中で作者が止めてしまったらしく、何年もメンテナンスされていない。
* Node（JavaScript）実装として[markdownlint](https://github.com/DavidAnson/markdownlint)が存在する。こちらはRuby版の移植として2017年10月現在もメンテナンスされている。
    * やや古い内容にあるが[2015年に本ブログでも取り上げている](/2015/05/01/lint-markdown-at-commit.html)ので参考にされたい。
