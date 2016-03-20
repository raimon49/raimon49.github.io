Title: Swiftで書かれたiOSアプリを実機デバッグ実行時に「image not found」エラーとなる場合の対処
Date: 2016-03-20 13:53:00
Category: iOS
Tags: Swift, Xcode, iOS
Slug: error-at-swift-app-with-ios-device
Authors: raimon
Summary: Swiftで書かれたiOSアプリの実機デバッグ実行がエラーとなる場合のXcode設定について

## エラー内容

Swiftで書かれたコードを含むiOSアプリを、検証用のiOS端末に流し込んで実機デバッグしようとすると、以下のようなエラーが出てクラッシュしてしまう事がある。

Objective-Cで書かれた既存XcodeプロジェクトにSwiftコードを追加した際にも遭遇する。

```sh
dyld: Library not loaded: @rpath/libswiftCore.dylib
Referenced from: /private/var/mobile/Containers/Bundle/Application/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/App-Name.app/App-Name
Reason: image not found
```

## 解決方法

確認するポイントとしては2点ある。

1点目は「Build Settings」-「Build Options」-「Embedded Content Contains Swift Code」を「Yes」に設定する。

![Xcode設定画面](/images/contains-swift-code.png)

2点目は「Build Settings」-「Linking」-「Runpath Search Path」に `@executable_path/Frameworks` を追加する。

![Xcode設定画面](/images/runpath-search-paths.png)

これらの設定を行ってからXcodeで再度デバッグ実行すると、iOS端末に流し込んでアプリを起動後にクラッシュが発生することは無くなった。

## 参考情報

* [ios - dyld: Library not loaded: @rpath/libswiftCore.dylib / Image not found - Stack Overflow](http://stackoverflow.com/questions/26104975/dyld-library-not-loaded-rpath-libswiftcore-dylib-image-not-found)
