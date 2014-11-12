Title: Xcode 6に付属しているSwiftのREPLを使う
Date: 2014-11-12 23:45:00
Modified:
Category: Xcode
Tags: Mac, Swift, Xcode
Slug: xcode-swift-repl
Authors: raimon
Summary: Xcode 6にはSwiftのREPLが付属しておりターミナル上で簡単に動作を試せる

Xcode 6にはSwiftのREPLが付属しておりターミナル上で簡単に動作を試せる。

## 起動方法

AppleのSwift Blogに紹介エントリがあって知ったのだが、Xcode 6にはSwiftのREPLが付属しており、次のように `swift` コマンドで起動できる。正確にはOS X Yosemiteの場合は `swift` と打ち、OS X Mavericksでは `xcrun swift` と打つ。

起動すると、番号付きのプロンプトが現れて入力待ちのループに入る。

```bash
# Yosemite
$ swift

# Mavericks
$ xcrun swift

Welcome to Swift version 1.1 (swift-600.0.20.0). Type :help for assistance.
  1> println("Hello, world!!")
Hello, world!!
```

REPLとしては良くできていて、入力の途中で `Tab` キーを押せば豊富な補完候補が表示される。

また、いかにも型付きのプログラミング言語らしく、`var` や `let` といったキーワードで宣言した変数でも、きちんと代入された値の型に応じてメソッドなどが補完される。

`import Foundation` は通るが `import UIKit` はエラーとなってしまった。

## 参考

* [Introduction to the Swift REPL - Swift Blog - Apple Developer](https://developer.apple.com/swift/blog/?id=18 "Introduction to the Swift REPL - Swift Blog - Apple Developer")
