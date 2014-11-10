Title: pipのrequirements.txtについて
Date: 2014-11-10 23:43:37
Modified:
Category: Python
Tags: Python
Slug: requirements-text
Authors: raimon
Summary: Pythonのパッケージ管理ツールpipで利用できる `requirements.txt` の仕様について。

Pythonのパッケージ管理ツールpipで利用できる `requirements.txt` の仕様について。

## 保存

virtualenv環境で現在インストールされているパッケージを外部ファイルに書き出すには、以下のように `-l` オプションを指定する。

ファイル名は慣例的に `requirements.txt` が使われる。

```bash
$ pip freeze -l requirements.txt
```

## 復元

この保存した内容を元にvirtualenv環境で復元するには `-r` オプションで指定する。

```bash
$ pip install -r requirements.txt
```

## 参考情報

* [User Guide — pip 1.5.6 documentation](http://pip.readthedocs.org/en/latest/user_guide.html "User Guide — pip 1.5.6 documentation")
