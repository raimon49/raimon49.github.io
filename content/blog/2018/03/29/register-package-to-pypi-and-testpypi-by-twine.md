Title: Twineを使ったPyPI/TestPyPIへのパッケージ更新
Date: 2018-03-29 10:53:52
Category: Python
Tags: Python
Slug: register-package-to-pypi-and-testpypi-by-twine
Authors: raimon
Summary: パッケージ公開ユーティリティTwineでPyPI/TestPyPIにPythonパッケージを登録・更新する方法

## setupスクリプトからTwineへの移行

[Migrating to PyPI.org](https://packaging.python.org/guides/migrating-to-pypi-org/)で案内されている通り `python setup.py register` や `python setup.py upload` といったsetupスクリプトを使って登録・更新しようとするとサーバー側から410 Errorが応答されるようになった。

上記の移行ガイドにおいて、Twineでの設定方法が案内されている。

PyPIの練習用サーバーであるTestPyPIでも、Twineで更新できるよう、移行しておくのが良いだろう。


## PyPI/TestPyPIへのTwineからの更新用設定

Twineを導入していなかれば、自身のvenv環境などにインストールする。

```bash
$ pip install twine
```

HOMEディレクトリにはTwineから参照される設定を `~/.pypirc` に書いておくと便利である。

```
[distutils]
index-servers=
    pypi
    pypitest

[pypi]
username: yourusername
password: yourpassword

[pypitest]
repository: https://test.pypi.org/legacy/
username: yourusername
password: yourpassword
```

上記設定ファイルのポイントとしては、

* PyPIの `repository` エントリは不要（Twineで何も指定しなければ通信先にPyPIが指定されたものとなる）。
* `password` エントリは、空にした場合、パスワード入力プロンプトで尋ねられる。共有サーバーなどに生のパスワードを置きたくない時は空にしておくのが良い。

Pythonパッケージ作者にとって、PyPI/TestPyPIへのパッケージ更新は日常的な作業の一つであるため、makeやFabricといったタスクランナーに定型タスクとして登録しておくと忘れなくて良い。以下に `Makefile` での登録例を示す。

```make
.PHONY: deploy
deploy: build
	twine upload dist/*

.PHONY: test-deploy
test-deploy: build
	twine upload -r pypitest dist/*

.PHONY: build
build:
	python setup.py sdist bdist_wheel
```

TestPyPIの時だけTwineの `-r/--repository` オプションを指定している点がポイントである。

これで、日常的なパッケージ更新作業は、

```bash
# TestPyPIへのパッケージ更新
$ make test-deploy

# PyPIへのパッケージ更新
$ make deploy
```

に集約できた。

## まとめ

2018年現在、PyPI/TestPyPIへのパッケージ登録・更新にはTwineを利用する。

Twine移行以前の情報（2015年時点）については、このブログの過去エントリ[Pythonプロフェッショナルプログラミング 第2版』のWebアプリケーション課題をGitHubで作りTest PyPIで公開する](/2015/10/31/pypro2-guestbook-webapp-with-github.html)も参考にされたい。
