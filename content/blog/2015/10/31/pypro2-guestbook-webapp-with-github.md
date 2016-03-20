Title: 『Pythonプロフェッショナルプログラミング 第2版』のWebアプリケーション課題をGitHubで作りTest PyPIで公開する
Date: 2015-10-31 08:52:35
Category: Python
Tags: CI, Git, GitHub, Python
Slug: pypro2-guestbook-webapp-with-github
Authors: raimon
Summary: 『Pythonプロフェッショナルプログラミング 第2版』のWebアプリケーション課題にアレンジを加えてBitbucketではなくGitHubに穂スティングした時の記録。

[秀和システムより出版されている『Pythonプロフェッショナルプログラミング 第2版』](http://www.shuwasystem.co.jp/products/7980html/4315.html)を読んでPythonパッケージングの仕組みなどについて勉強している。

* 2章「Webアプリケーションを作る」
* 3章「Pythonプロジェクトの構成とパッケージ作成」

で課題として登場するFlaskを使ったWebアプリケーションをPythonパッケージとして作成する方法について、書籍のサポートページなどからサンプルページを探してみたものの、見付からなかったので1から作ってみることにした。何点か書籍の内容に対してアレンジを加えたので、併せて紹介したい。

## 成果物

コード全体はGitHub、PythonパッケージはTest PyPI Serverというパッケージリポジトリで公開している。

* [https://github.com/raimon49/pypro2-guestbook-webapp](https://github.com/raimon49/pypro2-guestbook-webapp)
* [https://testpypi.python.org/pypi/raimon49.guestbook](https://testpypi.python.org/pypi/raimon49.guestbook)

Test PyPIというのは名前の通りPyPI公開前の検査・学習用のサーバで、機能に関しては本番用PyPIと全く同じものが利用できる。

[Test PyPI Server解説ページ](https://wiki.python.org/moin/TestPyPI)に書かれている通り、pipのオプション `-i` でパッケージインデックスとして `https://testpypi.python.org/pypi` を指定することで、Test PyPI上で公開したパッケージからインストールが可能になる。この時、課題guestbookアプリの依存しているFlaskはTest PyPIサーバからは見付けられないため、先にFlaskをインストールしておく必要がある。

```sh
# 先にFlaskをPyPIサーバからインストール
$ pip install Flask

# guestbookアプリをTest PyPIサーバからインストール
$ pip install -i https://testpypi.python.org/pypi raimon49.guestbook
```

## 書籍との違い

次のような点を書籍の内容とは違った方法に変更した。いずれも2015年現在で主流に近い部分と考えられるが、最後のTest PyPIについては書籍中でもオプションの選択肢として提示されており、特別にアレンジした内容ではない。

* Python本体とvirtualenv環境の管理にpyenvを使う
* Mercurial + BitbucketではなくGit + GitHubで構成管理・ホスティング
* コマンドラインオプションでネットワークとポート番号を指定可能に
* Travis CIを利用してPEP8に準拠しているかテスト
* 開発ツールの依存管理にpip-toolsを利用
* Test PyPI Serverでパッケージを公開

## Python本体とvirtualenv環境の管理にpyenvを使う

書籍ではUbuntuサーバの中で最新の2.7系Pythonをビルドする方法が紹介されている。この辺りはマルチバージョンにPythonを切り替えら得られる[pyenv](https://github.com/yyuu/pyenv)を使った方が管理が楽であると考え、pyenv経由でPython本体をビルド・利用するようにした。

また、virtualenv環境もpyenvコマンドを通して透過的に管理・利用できるため、READMEの内容もpyenvを中心とした手順に変えている。

* [https://github.com/raimon49/pypro2-guestbook-webapp/blob/master/README.rst](https://github.com/raimon49/pypro2-guestbook-webapp/blob/master/README.rst)

## Mercurial + BitbucketではなくGit + GitHubで構成管理・ホスティング

構成管理にMercurialはやや特殊だと感じたため、Gitを採用するよう変更した。

リポジトリのホスティングサービスは書籍の通りにBitbucketを使うことも考えられる（BitbucketではGitリポジトリのホスティングもサポートしている）が、ホスティング先もGitHubを使うことに変更した。

書籍との主な違いは構成管理上の無視設定を記述するファイルが `.hgignore` から `.gitignore` に変わる程度で、大きな違いは無い。

* [https://github.com/raimon49/pypro2-guestbook-webapp/blob/master/.gitignore](https://github.com/raimon49/pypro2-guestbook-webapp/blob/master/.gitignore)

他にもGitHubを使うメリットとして、[Add A License](http://www.addalicense.com/)といった便利な連係サービスから[ライセンスファイルの自動生成](https://github.com/raimon49/pypro2-guestbook-webapp/commit/101ee9fbaccd262b551f5ef2a9aedcd6e43eaa1f)ができる。

## コマンドラインオプションでネットワークとポート番号を指定可能に

書籍で紹介されているVirtualBoxと自宅PCでのVirtualBox環境との間で、ネットワーク設定がやや異なっていたので、いっそコマンドラインオプションで指定可能にしようと考えた。

Python 2.7には標準ライブラリとして強力な[argparseモジュール](http://docs.python.jp/2/library/argparse.html)が付属しているので、これを使ってやれば簡単に実現できる。

```python
import argparse
from flask import Flask, request, render_template, redirect, escape, Markup

NETWORK = '127.0.0.1'
PORT = 8000

application = Flask(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description='A guestbook web application.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='guestbook 1.0.0')
    parser.add_argument('-n', '--network',
                        default=NETWORK)
    parser.add_argument('-p', '--port',
                        type=int,
                        default=PORT)

    return parser.parse_args()


def main(debug=False):
    args = parse_args()
    application.run(args.network,
                    args.port,
                    debug=debug)

if __name__ == '__main__':
    main(debug=True)
```

上記の実装によりコマンドラインオプションが指定されていたらそちらを使うようになったため、最終成果物の `guestbook` コマンドでは、自由にネットワークとポート番号を変更してFlaskアプリケーションを起動できる。

```sh
# ネットワークとポート番号を変更して起動
$ guestbook -n 192.168.56.100 -p 5000
```

## Travis CIを利用してPEP8に準拠しているかテスト

書籍では主なCIツールとしてJenkinsの使い方が紹介されている。GitHubではCI as a ServiceとしてTravis CIと組み合わせる方法がメジャーであるため、こちらを利用してPEP8に準拠したPythonコードが書けているかチェックするようにした。

チェックツールには[pytest-pep8](https://pypi.python.org/pypi/pytest-pep8)を使い、非準拠コードの修正には[autopep8](https://pypi.python.org/pypi/autopep8/)を使った。

```sh
# ツールのインストール
$ pip install pytest-pep8 autopep8

# コードのチェック
$ py.test -v --pep8 guestbook

# 非準拠コードの修正
$ autopep8 -i guestbook/__init__.py
$ git commit -am 'Fix PEP8: E302 expected 2 blank lines'
```

これらのチェック用ツールへの依存関係は後述のpip-toolsで `dev-requirements.txt` というファイルにまとめ、Travis CIの設定ファイルでインストールされるように指定する。

```yaml
language: python
python:
  - "2.7"
install:
  - pip install -r dev-requirements.txt
script:
  py.test -v --pep8 guestbook
```

Travis CI側のWeb UIで今回のGitリポジトリと連携させるよう選択すると[pushの度に自動でチェックが走る](https://travis-ci.org/raimon49/pypro2-guestbook-webapp)ようになる。

## 開発ツールの依存管理にpip-toolsを利用

書籍でもpipを使う際の注意点として挙げられているが、guestbookアプリケーションの開発に利用するFlaskのバージョンが上がって `pip install -U Flask` でアップグレードし、もしFlaskの依存する他のPythonパッケージが変わった場合、不要になったパッケージの削除には追随できない。

この辺りを楽に管理するために[pip-tools](https://github.com/nvie/pip-tools)を使う。

```sh
$ pip install pip-tools
```

まずguestbookアプリケーション本体の動作に必要となる依存パッケージを `requirements.in` ファイルに記述する。

```
Flask
```

次にguestbookアプリケーションの開発作業でのみ必要となる依存パッケージを `dev-requirements.in` ファイルに記述する。このファイルでは `requirements.in` の内容も取り込むようにする。

```
-r requirements.in

autopep8
docutils
wheel
pip-tools
pytest-pep8
```

それぞれのファイルをpip-toolsに付属する `pip-compile` でコンパイルすると、最新の依存バージョンが書き出される。

```sh
# requirements.txtファイルの書き出し
$ pip-compile requirements.in

# dev-requirements.txtファイルの書き出し
$ pip-compile dev-requirements.in

# 依存バージョンに更新があった場合の手元virtualenv環境への反映
$ pip-sync dev-requirements.txt
```

## Test PyPI Serverでパッケージを公開

Test PyPIへのパッケージ登録・公開方法は[How to submit a package to PyPI](http://peterdowns.com/posts/first-time-with-pypi.html)のページに詳しい。

1. [本系PyPIアカウント登録](http://pypi.python.org/pypi?%3Aaction=register_form)と[Test PyPIアカウント登録](http://testpypi.python.org/pypi?%3Aaction=register_form)を済ませる
    * 両者は機能としては同じだがアカウントDBが完全に別物であるため、両方に登録する
    * 入力したEメールアドレスにリンク付きのメールが届いて、それを踏んで規約同意すると登録完了
    * 同じEメールアドレスとパスワードを使っておくのがオススメだそう
2. ホームディレクトリに `.pypirc` ファイルを作成し `pypi` と `pypitest` の設定を記述する
    * `password:` は空欄でも登録時にプロンプトで入力できるため問題は無い
3. Test PyPIにパッケージを登録・公開する
    * パッケージ名が `guestbook` だと他と被る可能性が高いため `{アカウント名}.guestbook` のような名前を使うと良い

`.pypirc` では `pypitest` という名前でTest PyPI Serverが登録しておく。

```
[distutils]
index-servers=
    pypi
    pypitest

[pypitest]
repository = https://testpypi.python.org/pypi
username = raimon49
password =

[pypi]
repository = https://pypi.python.org/pypi
username = raimon49
password =
```

この状態だと `-r pypi` オプションで、登録と公開する先をTest PyPIに指定できる。

```sh
# registerの時にパスワードを尋ねられてuploadでもそれが認証に使われる
$ python setup.py register -r pypitest sdist bdist_wheel upload -r pypitest
```

## まとめ

Pythonパッケージの作成方法について、『Pythonプロフェッショナルプログラミング 第2版』の内容を少しアレンジしてまとめた。本書はビープラウド社のノウハウが中心であるため、構成管理にMercurialを採用しているのかなと感じた。自分もMercurialは一時期プライベートで使っていたが、世間の流れが完全にGitへ傾いてしまったため、今回学んだ内容もGitで管理したかった。

まとまった量のREADMEドキュメントをreStructuredTextフォーマットで書いたのは今回が初めてで、Markdownとの違いも見えて良い経験になった。
