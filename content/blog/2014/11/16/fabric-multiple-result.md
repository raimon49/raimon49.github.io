Title: Fabricで複数ホストに対して実行した結果を使って何かする
Date: 2014-11-16 18:45:00
Category: Python
Tags: Fabric,Python
Slug: fabric-multiple-result
Authors: raimon
Summary: Fabricで複数ホストに対して実行した結果を使って何かしたい時はexecute()

お手軽デプロイ・システム管理ツールFabricで各タスクを実行した結果を使って何かしたい時には、 `execute(task_name)` でホスト毎の結果が辞書オブジェクトとして変数に格納できる。この時、親となるタスクには重複実行されないよう `@runs_once` を付ける。

例えば、以下のようにタスクを定義する。

```python
from fabric.api import *

env.use_ssh_config = True


@task
@runs_once
def print_is_ubuntu_servers():
    results = execute(detect_is_ubuntu_server)
    print(results)

@task
def detect_is_ubuntu_server():
    unix_name = run("uname -a", quiet=True)
    return _is_ubuntu_server(unix_name)

def _is_ubuntu_server(unix_name):
    return unix_name.find("Ubuntu") != -1
```

これを複数のLinuxディストリビューションを採用している複数ホストに対して実行すると、そのサーバがUbuntuを使っているか、ホスト名をキー値に持つ辞書オブジェクトで取得できる。

```bash
$ fab print_is_ubuntu_servers -H centos.host,ubuntu.host
[centos.host] Executing task 'print_is_ubuntu_servers'
[centos.host] Executing task 'detect_is_ubuntu_server'
[ubuntu.host] Executing task 'detect_is_ubuntu_server'
{'centos.host': False, 'ubuntu.host': True}

Done.
Disconnecting from user@centos.host... done.
Disconnecting from user@ubuntu.host... done.
```

複数ホストの実行結果を `results` で受け取ることで、さらに `confirm()` で実行ユーザーに尋ねて、別タスクでターゲットになったホストに対してだけさらに別タスクを実行、といった応用が利く。
