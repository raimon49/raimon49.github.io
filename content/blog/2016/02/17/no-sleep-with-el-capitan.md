Title: OS X El CapitanでNoSleep代替としてInsomniaXで蓋を閉じて自動スリープを防止する
Date: 2016-02-17 22:29:00
Modified:
Category: Mac
Tags: Mac
Slug: no-sleep-with-el-capitan
Authors: raimon
Summary: El Capitanで「NoSleep Kernel Extension is not loaded.」で機能しないため代替としてInsomniaXを導入し、MacBookの蓋を閉じた時の自動スリープを防止する

OS XをEl Capitanにアップデートすると、モバイル環境でMacBookの蓋を閉じた時の自動スリープを防止するNoSleep.appが「NoSleep Kernel Extension is not loaded.」というエラーメッセージと共に機能しなくなる。

## 代替としてInsomniaXを導入する

古いNoSleep.appを入れると使えるといった情報も探すと出て来るが、自分の環境では残念ながら機能しなかった。

代替として[InsomniaX](http://semaja2.net/projects/insomniaxinfo/)を導入する事で希望の動作を実現できた。

導入方法としては、2016-02-17現在のLatest Versionである[InsomniaX-2.1.8](http://insomniax.semaja2.net/InsomniaX-2.1.8.tgz)をダウンロードして展開・インストールを行う。

```sh
$ tar zxvf InsomniaX-2.1.8.tgz
$ sudo cp -r InsomniaX.app /Applications
```

インストール完了したらInsomniaX.appを起動し、

* 「Preferences」 - 「Start to Login」にチェック
* 「Disable Lid Sleep」にチェック

<img src="/images/insomniax-setting.png" alt="InsomniaXの設定例" width="198px" height="301px" style="width: 198px; max-width: 100%; height: auto;">

上記のような設定で利用することで、MacBookの蓋を閉じた時の自動スリープを防止したい目的は達成できた。
