Title: Travis CIのビルドコンテナ内で最新のpipを使う
Date: 2015-10-11 20:31:05
Category: Python
Tags: CI, Python
Slug: use-latest-pip-in-travis
Authors: raimon
Summary: Travis CIでビルドを走らせる際に古いバージョンのpipがインストールされていて回避したい時の方法。

[pip-tools](https://github.com/nvie/pip-tools)が大きくバージョンアップし、 `pip-compile` および `pip-sync` コマンドを組み合わせた依存管理が行えるようになった。

## CIフローとして依存パッケージの更新を知りたい

pip-toolsの細かな使い方は、最後に参考情報をまとめることにして、pip-toolsを利用すると、現在リポジトリ内で宣言している依存パッケージが古くなっているかどうか、次のように調べられる。

```sh
$ pip-compile --dry-run requirements.in | diff -u requirements.txt -
```

pip-toolsでの管理に移行しておらずトラディショナルな `pip freeze -l` した内容で依存パッケージを宣言している場合は、次のように比較が可能である。

```sh
$ pip-compile --dry-run --no-header --no-annotate requirements.in | diff -u requirements.txt -
```

いずれの比較方法にせよ[Travis CI](http://travis-ci.org/)のようなCI as a Serviceでのビルドログに上記コマンドの結果を記録しておくと、古くなったパッケージが検知できて便利である。

## Travis CIのpipが古い

ところが2015-10-11現在、Travis CIのPythonプラットフォームでビルドを実行するコンテナ内では `pip-compile` に必要な要件 `pip==6.1 or higher` を満たしておらず、pipのバージョンが古いためにビルドが必ず失敗してしまう。

これを解決するには、`before_script` のフックでpipを最新にアップグレードしてしまえば良い。

```yaml
language: python
python:
  - "2.7"
install:
  - pip install -r requirements.txt
before_script:
  - pip install -U pip
  - pip-compile --dry-run requirements.in | diff -u requirements.txt -
script:
  (テストスクリプトの実行)
```

やや強引な方法だが、Travis CI側のpipデフォルトバージョンが上がるまでのワークアラウンドなので、不要になったら消せば問題ないと思われる。

## 参考情報

pip-toolsに関しては、次のページを参考にした。この管理方法が主流になって行くか現時点では分からないが、CIと組み合わせ易い点は便利である。

* [Python - pip-toolsでrequirements.txtのパッケージバージョン番号を管理しよう - Qiita](http://qiita.com/ryu22e/items/ad3f8f3df30886d23661)
* [Managed environments with pip-tools ? koed](https://koed00.github.io/managed-environments-with-piptools/)
