Title: CodecovでPythonコードリポジトリのコードカバレッジを継続的に計測する
Date: 2016-01-17 13:56:18
Category: Python
Tags: CI, GitHub, Python
Slug: continuous-code-coverage-with-codecov
Authors: raimon
Summary: CodecovとTravis CIを連携することで、CodecovでPythonコードリポジトリのコードカバレッジを継続的に計測できる。

[Codecov](https://codecov.io)というサービスを利用すると、GitHubにホスティングしているGitリポジトリのコードカバレッジを継続的に計測し、次のようにバッジで表示できる。

<img src="/images/codecov-badge-sample.png" alt="GitHub READMEに埋め込んだ例" width="369px" height="42px" style="width: 369px; max-width: 100%; height: auto;">

同種のCode coverage as a Service的なものでは、有名なサービスとして[Coveralls](https://coveralls.io/)がある。

## Travis CI連携済みのPythonプロジェクトでCodecovを利用

今回は技術書のサンプルコードを写経してコードカバレッジが取得できるようになっており、かつTravis CIでテストが自動的に回るように連携済みである[既存のPythonプロジェクト](https://github.com/raimon49/pypro2-unittest-study)に対してCodecovとの連携を組み込んでみた。

```sh
# このカバレッジをCodecovで計測したい
$ py.test --doctest-modules --pep8 -v --cov=bankaccount --cov=myview --cov=utility
----------------------------------------- coverage: platform linux2, python 2.7.9-final-0 ------------------------------------------
Name             Stmts   Miss  Cover
------------------------------------
bankaccount.py      29      2    93%
myview.py           15      2    87%
utility.py           5      0   100%
------------------------------------
TOTAL               49      4    92%
```

## codecovモジュールの組み込み

結論から言うとCodecovサービスと連携してPythonのコードカバレッジを計測するのは非常に簡単で、[codecovモジュール](https://pypi.python.org/pypi/codecov/1.1.4)をプロジェクトに依存に追加し、Travis CIの `after_success` フックで呼ぶようにしておくだけである。

設定のYAML全体は以下の通り。

```yaml
language: python
python:
  - "2.7"
install:
  - pip install -r tests-requirements.txt
script:
  py.test --doctest-modules --pep8 -v --cov=bankaccount --cov=myview --cov=utility
after_success:
  codecov
```

[Codecov連携するためのコミット差分](https://github.com/raimon49/pypro2-unittest-study/commit/f6a4f95cb3925462683f02c0264bf83b90120f92)を見ても、ほんの少しの変更で対応できている事が分かる。

## 少ない省力で十分なレポート

Codecov連携しているとコミット毎にテストが書かれているステートメントと書かれていないステートメントを[シンプルな色分けでレポートしてくれる](https://codecov.io/gh/raimon49/pypro2-unittest-study/src/master/bankaccount.py)。

<img src="/images/cover-repost.png" alt="Codecovでのレポート画面" width="487" height="467" style="width: 487px; max-width: 100%; height: auto;">

もちろん、Jenkinsでも充実したPluginエコシステムを利用して同様のレポートを取得・表示することは可能だが、個人のコード管理でそこまでCIサーバ運用に手間をかけられないのが実情である。

これだけの少ない省力で十分なレポートが得られるのであれば、やはり今後はCodecovのようなカジュアルに使えるコードカバレッジ計測サービスが主流になって行くと思われる。

なお本記事の冒頭に貼った画像で依存パッケージの更新状況を表している真ん中のバッジは[Requires.io](https://requires.io/)というサービスで、同様のサービスとして[Gemnasium](https://gemnasium.com/)が有名だが、Requires.ioの方が `git push` した後に即時反映してくれるなど便利な印象である。PythonプロジェクトであればGemnasiumよりも良い選択肢になる。
