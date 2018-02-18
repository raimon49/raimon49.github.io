Title: pip showコマンドで「License: UNKNOWN」と表示されるライブラリのライセンスを調べるには
Date: 2018-02-18 12:52:44
Category: Python
Tags: Python
Slug: check-license-as-unknown-with-pip-show-command
Authors: raimon
Summary: LicenseをClassifiersから取得できるツールpip-licensesの紹介

## 「License: UNKNOWN」問題

pip installでインストールしたPythonライブラリについてpip showコマンドで情報表示すると、「License: UNKNOWN」と出力されるケースがある。例えばPythonでは著名なCLIライブラリである[click](https://pypi.python.org/pypi/click)も該当する。

```bash
$ pip show click
Name: click
Version: 6.7
Summary: A simple wrapper around optparse for powerful command line utilities.
Home-page: http://github.com/mitsuhiko/click
Author: Armin Ronacher
Author-email: armin.ronacher@active-4.com
License: UNKNOWN
```

## なぜUNKNOWNのままなのか

なぜライブラリ作者がUNKNOWNのままライセンスを明示していないのかというと、これは[PEP314](https://www.python.org/dev/peps/pep-0314/)に理由が書かれている。

要約すると、ライブラリを公開しているPythonパッケージ作者は、メタ情報として[Classifiersのリスト](https://pypi.python.org/pypi?:action=list_classifiers)から自分のソフトウェアライセンスに該当するものを選択し、リストに無い時はLicenseフィールドで表現する事が求められる。

よって、Classifiersで自分のライセンスを宣言できている作者は、Licenseフィールドに何も情報を入れていないケースがあるし、結果として「License: UNKNOWN」と表示されても、作者の不注意ではないのである。

## pip-licensesでClassifiers情報を参照する

ということで、利用中のソフトウェアライセンスを調べる用途では、pip showコマンドを使うのは適切ではない。

[pip-licenses](https://pypi.python.org/pypi/pip-licenses)という調査ツールでは、Classifiersからの情報取得がサポートされるため、`--from-classifier` オプションと組み合わせて使う。

```bash
# ツールのインストール
$ pip install pip-licenses

# --from-classifierオプションでライセンスを調査
$ pip-licenses --from-classifier
 Name                Version    License
 click               6.7        BSD License
```

これでclickはライセンス不明のソフトウェアではなく、BSD Licenseで提供される事が分かり、安心して利用できる。
