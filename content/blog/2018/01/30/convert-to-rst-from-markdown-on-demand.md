Title: PythonパッケージをPyPIにアップロードする際にMarkdownをreSTに変換
Date: 2018-01-30 17:52:24
Category: Python
Tags: GitHub, Markdown, Python
Slug: convert-to-rst-from-markdown-on-demand
Authors: raimon
Summary: PyPIサーバーではreSTフォーマットでなければHTML描画されないため、Markdownフォーマットの文書をオンデマンドでreSTに変換してアップロードする方法

## MarkdownフォーマットではHTML描画されない問題

Pythonパッケージの開発もGitHubが使われるケースが増えている。それに伴って、パッケージのドキュメントもMarkdownフォーマットが採用されるケースも散見される。

ただし、MarkdownフォーマットでPyPIサーバーにアップロードすると、Web UIではHTML描画されないため、ユーザーフレンドリーではない。

<img src="/images/markdown_at_pypi.png" alt="Markdownがプレーンテキストで表示されている例" width="195px" height="276px" style="width: 198px; max-width: 100%; height: auto;">

そこで、Pythonパッケージの新しいバージョンをPyPIサーバーにアップロードする際に、オンデマンドでreStructuredText（以降「reST」）フォーマットにオンデマンドで変換してやると、いい感じにWeb UIでもHTML描画される。

<img src="/images/rst_at_pypi.png" alt="Markdownがプレーンテキストで表示されている例" width="184px" height="236px" style="width: 198px; max-width: 100%; height: auto;">

## 環境準備

フォーマットのオンデマンド変換には、ドキュメントコンバーターである[Pandoc](https://pandoc.org/)と、そのPythonラッパーである[pypandoc](https://pypi.python.org/pypi/pypandoc/)を利用する。この変換Tipsは、pypandoc自身でも新バージョンのリリース時に採用されている手法である。

Pandocの準備は、[Installing pandoc](https://pandoc.org/installing.html)の項を参考に、ビルド済みバイナリでインストールする。macOSであればHomebrew、Linuxであればディストリビューションごとのパッケージ管理ツール経由でインストールできる。

pypandocはPyPIサーバから `pip install` でインストールする。

```bash
$ pip install pypandoc
```

## 変換処理の適用

パッケージのドキュメントが `README.md` というファイル名で管理されていると仮定すると、`setup.py` に適用する変換処理は次のようになる。

```python
import os
from setuptools import setup


def read_file(filename):
    basepath = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(basepath, filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''


LONG_DESC = ''
try:
    import pypandoc
    LONG_DESC = pypandoc.convert('README.md', 'rst', format='markdown_github')
except (IOError, ImportError):
    LONG_DESC = read_file('README.md')


setup(
    name='your-package-name',
    long_description=LONG_DESC,
    # (省略)
)
```

これで毎回 `setup.py` でパッケージを作成した際に `long_description` として渡されるドキュメントはreSTフォーマットに変換済みとなった。

ただしPandocの変換も完全ではないため、壊れたreSTフォーマットになってしまう時がある。

壊れた状態でPyPIにアップロードしてもHTML描画されないため、気になる時は `dist/` ディレクトリの成果物をチェックしておくと良い。 `rst2html.py` は[docutils](https://pypi.python.org/pypi/docutils)パッケージに付属している。

```bash
$ python setup.py --long-description | rst2html.py > /dev/null
```

上記のコマンドでエラーが出力されなければ、PyPIへ成果物アップロード後、整形されたHTMLで描画される。

もちろん、最初から `README.rst` としてreSTフォーマットでドキュメント管理していれば、こういうTipsは不要だが、GitHubで新しいリポジトリを作成した時のデフォルトはMarkdownフォーマットであり、Markdownの方が慣れている開発者も多いため、オンデマンド変換も悪くないやり方と思われる。

## 参考情報

* [Use Markdown README's in Python modules (Example)](https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules)
* [Python Package Index (PyPI)](https://docs.python.jp/3/distutils/packageindex.html)
