Title: Java 7でオブジェクト同士を比較する時のnullチェックはユーティリティメソッドに任せられる
Date: 2014-12-08 21:55:00
Category: Java
Tags: Java
Slug: java7-objects-equals
Authors: raimon
Summary: Java 7から追加されたjava.util.Objects.equals(arg1, arg2)について。

## 不毛な議論

Javaでしばしば不毛な議論の対象となるのが `null` チェックのお作法で、

```java
if (foo.equals("foo")) {
    // NullPointerExceptionが発生し得る
}
```

変数 `foo` が `null` だった時に例外が発生してしまうから、必ず `null` チェックを併記しようとか、定数を先に書く規約にしようと云う話になりがち。

```java
if (foo != null && foo.equals("foo")) {
    // 先にnullでないことをチェック
}
if ("foo".equals(foo)) {
    // fooがnullでもNullPointerExceptionは発生しない
}
```

しかし個人的にはどちらも好きじゃなかった。

特に後者は大昔のC言語のようで好きになれない。

## Java 7から使えるユーティリティメソッド

ところがJava 7からは[JDK 7: java.util.Objectsに欲しい、頻繁に書かれるユーティリティメソッドは?](http://www.infoq.com/jp/news/2009/09/jdk7-java-utils-object)で解説されているような `java.util.Objects.equals(Object a, Object b)` を使って比較すれば、 `a` と `b` いずれかの引数が `null` だった時も考慮して比較結果を返してくれるようだ。

```java
if (Objects.equal(foo, "foo")) {
    // fooがnullでも"bar"でも比較結果はfalseが返される
}
```

再帰的に比較してくれる `java.util.Objects.deepEquals(Object a, Object b)` なるメソッドや、引数 `o` が `null` だった時にデフォルト文字列を指定できる `java.util.Objects.toString(Object o, String nullDefault)` などなど、多くのJavaプログラマが泣いてきた定型パターンで楽をさせてもらえそうなユーティリティクラスだった。

もちろん、こういうの自前で定義して使ってたよって人も山ほど居るだろうけど、標準APIに用意されているなら「これ使おうよ」で議論が終わるから便利。積極的に使って行きたい。

## 参考情報

* [Objects (Java Platform SE 7 )](https://docs.oracle.com/javase/jp/7/api/java/util/Objects.html "Objects (Java Platform SE 7 )")
