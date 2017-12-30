Title: PyTodoistからTodoistで管理された自分のタスクにアクセス
Date: 2017-12-30 15:04:29
Category: Python
Tags: Python
Slug: access-my-task-with-pytodoist
Authors: raimon
Summary: Todoist APIで提供されるタスク操作機能に対してPyTodoistを経由してアクセスする方法

GTDタスク管理ツールのTodoistには[開発者向けAPIが用意されている](https://developer.todoist.com/sync/v7/)。

Todoist Sync APIはシンプルなWebAPIであるが、これらのAPI群をラップしたPythonライブラリが幾つか公開されている。

この記事では、3rd partyライブラリのPyTodoistを使い、自分のTodoist管理タスクにアクセスする方法を紹介する。一応オフィシャルな操作ライブラリとして[todoist-python](https://pypi.python.org/pypi/todoist-python)が存在するが、使ってみた印象としてはPyTodoistの方が直感的で分かり易いと思った。

## PyTodoistのインストール

PyTodoistもtodoist-pythonと同様に、[PyPIで公開されている](https://pypi.python.org/pypi/pytodoist)ものを手元の環境にインストールして使う。

```bash
$ pip install pytodoist
```

PyTodoistは2017-12現在の公開バージョンでrequestsモジュールに依存しており、関連パッケージが幾つか一緒にインストールされる。

```bash
$ pip list
Package    Version
---------- ---------
certifi    2017.11.5
chardet    3.0.4
idna       2.6
pip        9.0.1
pytodoist  2.1.0
requests   2.18.4
setuptools 38.2.5
urllib3    1.22
wheel      0.30.0
```

## 自分のタスクにアクセスしてリスト形式で出力する

PyTodoistでは、アカウント認証に複数の方式がサポートされている。

最もシンプルで簡単なのは、TodoistのAPIトークンを利用する方式だろう。自分のアカウント用APIトークンは、「設定」-「連携」-「APIトークン」に表示されている。トークンをPyTodoistに渡してアクセスを行う。

このトークンがあれば、タスクの参照や作成ができてしまうため、扱う上での露出には注意されたい。

試しにAPIトークンで自分のタスクを全て参照し、リスト形式で出力してみる。

Todoistのタスクは、

* プロジェクト
    * タスク
        * サブタスク

という親子構造で管理される。サブタスクの子レベルは `task.indent` という属性値で参照可能で、このPythonスクリプトでも、プロジェクト - タスク - サブタスクの親子関係を、インデント量で表現して出力することにする。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)

from pytodoist import todoist


API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def main():
    def list_asterisk():
        return '* '

    def expand_sub_task(indent):
        return '  ' * indent

    user = todoist.login_with_api_token(API_TOKEN)
    for project in user.get_projects():
        print(list_asterisk() + project.name)
        for task in project.get_tasks():
            print(expand_sub_task(task.indent) +
                  list_asterisk() +
                  task.content)


if __name__ == '__main__':
    main()
```

上記のスクリプトを `todoist.py` という名前で保存し、実行してみると、自分のタスクがリスト出力できる。

```bash
$ ./todoist.py
* Project 1
  * Task A
    * Sub task A
  * Task B
  * Task C
    * Sub task A
* Project 2
  * Task A
  * Task B
    * Sub task A
    * Sub task B
```

もちろん、タスクの完了や削除、新規作成もPythonコードで可能なため、自分用に簡単なCLIツールを実装してみるのも良さそうである。

## 参考情報

* [PyTodoist documentation](http://pytodoist.readthedocs.io/en/latest/pytodoist.html)
* [API Documentation | Todoist Developer](https://developer.todoist.com/sync/v7/)
