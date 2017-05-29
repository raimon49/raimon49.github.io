Title: python-prompt-toolkitを使ってお手軽自動補完
Date: 2017-05-29 23:42:44
Category: Python
Tags: Python
Slug: auto-suggest-by-python-prompt-toolkit
Authors: raimon
Summary: python-prompt-toolkitを使ってお手軽に高機能な対話型CUIを実現する

## python-prompt-toolkitで手軽に高機能な入力待ち画面

[python-prompt-toolkit](https://pypi.python.org/pypi/prompt_toolkit)はPure Pythonで実装されたシンプルかつ強力なプロンプト作成ツールで、例えば次のようなREPL風のPythonコード入力待ち画面をお手軽に実現できる。

<img src="/images/python-suggest.png" alt="入力補完付きのプロンプト" width="575px" height="102px" style="width: 575px; max-width: 100%; height: auto;">

このプロンプトを実現するコード全体は本当にシンプルである。入力補完で表示している要素は、単にPythonの予約語をリストとして渡しているだけだ。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from pygments.lexers import PythonLexer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit import prompt
from prompt_toolkit.layout.lexers import PygmentsLexer

reserved_words_completer = WordCompleter([
    'and',       'del',       'from',      'not',       'while',
    'as',        'elif',      'global',    'or',        'with',
    'assert',    'else',      'if',        'pass',      'yield',
    'break',     'except',    'import',    'print',
    'class',     'exec',      'in',        'raise',
    'continue',  'finally',   'is',        'return',
    'def',       'for',       'lambda',    'try',
])


def main():
    code = prompt('Enter Python code: ',
                  completer=reserved_words_completer,
                  lexer=PygmentsLexer(PythonLexer))
    print('Raw code: %s' % code)


if __name__ == '__main__':
    main()
```

## 依存ライブラリも少ない

インストール時に一緒に入る依存ライブラリも少なく、バージョン1.0.14現在、sixとwcwidthの2つのみである。今回は入力中Pythonコードの構文ハイライトも実現したかったため、一緒にPygmentsもインストールしているが必須ではない。

```console
$ pip install prompt_toolkit Pygments
```

## 使い方は色々考えられる

サポートされるPython本体のバージョンも2.6から最新の3.5までと広く、大抵のUNIX系OS環境にバンドルされているPythonそのままで動作が期待できる。

例えばリモート実行ツールのFabricと組み合わせてターゲットホストや条件を選択させるCUIフロントエンドを作ったり、機械学習系の実行を繰り返す際の条件入力の補助にも使えると考えられる。

作者のJonathan Slenders氏は、python-prompt-toolkitを応用して[pyvim](https://pypi.python.org/pypi/pyvim)や[pymux](https://pypi.python.org/pypi/pymux)といった尖ったPure Pythonプロダクトを多く作っているようだ。
