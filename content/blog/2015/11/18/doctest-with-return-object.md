Title: Pythonでオブジェクトを返す関数/メソッドをdoctestする
Date: 2015-11-18 21:19:59
Category: Python
Tags: Python
Slug: doctest-with-return-object
Authors: raimon
Summary: オブジェクトを返す関数やメソッドをdoctestする方法。

## doctestの使い方

Pythonにはdoctestと呼ばれる仕組みが標準で備わっている。

docstringと呼ばれるドキュメンテーション文字列フォーマットの中に、関数やメソッドの使い方を示す式と期待される戻り値を書いておくと、それを実行してテストできる。

例えば `calc.py` として次のように関数が定義されているとする。

```python
def add(x, y):
    """
    引数xとyを加算した結果を返す
        >>> add(2, 3)
        5
    """
    return x + y
```

テストランナー系のライブラリに頼らず素直にdoctestを実行すると、次のような結果が得られる。

```sh
$ python -m doctest -v calc.py
Trying:
    add(2, 3)
Expecting:
    5
ok
1 items had no tests:
    calc
1 items passed all tests:
   1 tests in calc.add
1 tests in 2 items.
1 passed and 0 failed.
Test passed.
```

## 辞書オブジェクトやインスタンスオブジェクトを返す関数をdoctestしたい

辞書オブジェクトやインスタンスオブジェクトを返す関数をdoctestしたい時はどうするのが良いか。

例えばユニットテストは高速に実行したいため、外部リソースを取得する部分をモック化する事が良くある。このモック化のために、以下のようなヘルパー関数を作っておくとする。

```python
from mock import patch, Mock, MagicMock, PropertyMock


def mocked_response(status_code=200):
    code = PropertyMock()
    code.return_value = status_code

    response = MagicMock()
    response.read.return_value = 'mocked body'
    type(response).code = code

    return response


@patch('urllib2.urlopen')
def test_use_some_resouce(urlopen):
    urlopen.return_value = mocked_response(status_code=200)

    target = TargetClass()
    assert target.request() == 'mocked body'
```

これで関数 `test_use_some_resouce` は、モック化されたレスポンスオブジェクトを使って高速にテストできるようになった。

ヘルパー関数 `mocked_response` 自身もdoctestを使ってテストしたいが、この関数はスカラ値ではなくモック化された `code` プロパティと `read` メソッドを持つオブジェクトを返す。

## doctestの式で比較しTrue/Falseを実行結果として書く

オブジェクトを返す関数のdoctest方法は、ずばり[doctestモジュール 25.2.3.6. 注意](http://docs.python.jp/2/library/doctest.html)に書かれている。

`>>>` で実行される式の行には辞書オブジェクトやインスタンスオブジェクトの持つプロパティとの比較を書き、期待する出力の行には `True/False` を書いておけば良い。

```python
def mocked_response(status_code=200):
    """
    Return mocked response instance

        >>> mocked_response(status_code=404).code == 404
        True
        >>> mocked_response(status_code=404).read() == 'mocked body'
        True
    """
```

doctestを実行すると、期待通りにテストができている。

```sh
$ python -m doctest -v tests/test_target_class.py
Trying:
    mocked_response(status_code=404).code == 404
Expecting:
    True
ok
Trying:
    mocked_response(status_code=404).read() == 'mocked body'
Expecting:
    True
ok
```

今回はわざわざ `python -m doctest` で実行したが、`nosetests` や `py.test` のようなテストランナーを使えば、宣言されているdoctestも簡単に見付けてテストしてくれる。

```sh
# noseでdoctest
$ nosetests --with-doctest -v

# pytestでdoctest
$ py.test --doctest-modules -v
```
