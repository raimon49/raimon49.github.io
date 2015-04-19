Title: OS XでAndroid Studioインストール後の起動が進まなかった時の対処
Date: 2015-04-19 11:19:19
Modified:
Category: Android
Tags: Android, Android Studio, Mac
Slug: android-studio-does-not-launching
Authors: raimon
Summary: Android Studioインストール後の起動が進まなかった時、Proxy設定の変更で解消した。

Android Studioをインストールして起動したが、最初の画面で「The following SDK components were not installed: extra-android-m2repository, tools, addon-google\_apis-google-21, android-21, sys-img-x86-addon-google\_apis-google-21, source-21, extra-google-m2repository」のようなメッセージが表示され、何度「Retry」ボタンを押して試みても成功しなかった。

## 環境

* OS X Yosemite 10.10.3
* JDK 8 u45
* Android Studio 1.1.0

## Proxy設定の変更で解消

メニューバー「Android Studio」-「Preferences」-「HTTP Proxy」より、「Auto-detect proxy settings」を選択、設定を反映。

![Android Studio Proxy設定画面](/images/android-stdio-proxy-setting.png)

一度Android Studioを終了し、ホームディレクトリの `~/.android` を削除する。

```sh
$ rm -rf ~/.android
```

上記を行ってからAndroid Studioを再び起動すると、処理が進んで失敗しなくなった。

## 参考情報

* [Android Studio doesn't start, fails saying components not installed - Stack Overflow](http://stackoverflow.com/questions/27376465/android-studio-doesnt-start-fails-saying-components-not-installed)
