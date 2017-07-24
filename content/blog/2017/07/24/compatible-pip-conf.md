Title: pip.confファイルをUnix系OS/macOSどちらでも同じ場所に置く
Date: 2017-07-24 20:13:12
Category: Python
Tags: Python
Slug: compatible-pip-conf
Authors: raimon
Summary: pipのユーザー毎に設置する設定ファイルを一つの場所で管理する

## pip 9.xからpip listコマンドに警告が出る

pip 9.x以降に更新すると `pip list` コマンドで警告が出るようになる。

これを抑止するには、システムワイドまたはユーザー毎に `pip.conf` ファイルを置いてlist formatを指定することで解決する。

* [pip 9 系にしたら pip list で警告出るようになったので止めたい](http://dev.classmethod.jp/server-side/language/pip-9-pip-list-deprecate-message/)

しかし、ユーザー毎の設定は、Unix系OSとmacOSとで、それぞれファイルを置く場所が異なるため、管理が煩雑になり面倒である。

* Unix系OS: `$HOME/.config/pip/pip.conf`
* macOS: `$HOME/Library/Application Support/pip/pip.conf`

## 環境変数で一つの場所を指定し管理する

[pip User Guide](https://pip.pypa.io/en/stable/user_guide/)に書かれているが、環境変数 `PIP_CONFIG_FILE` で設定ファイルの場所を指定しておけば、どのOSでも同じ場所の設定ファイルを見に行くようになる。

例えば、メインシェルの設定ファイルで次のように環境変数で場所を定義すれば良い。

```bash
export PIP_CONFIG_FILE="${HOME}/.pip.conf"
```

これで、自分で定義した場所に設定ファイルを置いておけば、Unix/Linux OSの時もmacOSの時も `pip list` コマンドで同じ設定が効くようになる。

```bash
$ cat ${HOME}/.pip.conf
format = columns

$ pip list
Package         Version
--------------- -------
apipkg          1.4
asn1crypto      0.22.0
bcrypt          3.1.3
blinker         1.4
```

