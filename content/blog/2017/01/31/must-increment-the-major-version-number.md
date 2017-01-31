Title: SemVerを採用したソフトウェアの更新でビルドが壊される時、メジャーバージョン番号を上げなければならない
Date: 2017-01-31 20:23:10
Category: Node
Tags: CI, Node
Slug: must-increment-the-major-version-number
Authors: raimon
Summary: SemVerを採用したソフトウェアに利用者の期待するバージョン更新と異なる更新が行われると、ビルドが破壊されたり混乱を招く。

ソフトウェアが[セマンティックバージョニング（以下SemVer）](http://semver.org/lang/ja/)を採用している時、公開APIの互換性を保たれない変更がされるのであれば、メジャーバージョン番号を上げなければならない。

## jshint-stylishのケース

[jshint-stylish](https://www.npmjs.com/package/jshint-stylish)というJavaScriptライブラリでは実際にメジャーバージョン番号が `1.y.z` から `2.y.z` にインクリメントされた。

この時の変更は、第三者からのP-Rを受け入れて、ライブラリが提供するコードの大半が `stylish.js` から `index.js` に移されたものだった（[バージョン間の差分](https://github.com/sindresorhus/jshint-stylish/compare/v1.0.2...2.0.0)）。

変更の結果、jshint-stylishを利用しているユーザーは、次のように利用コードを変更する必要があった。変更しないでバージョンアップした場合は **ビルドが破壊される** からである。

```sh
# jshint-stylish 1.0.2を利用するコード
$ jshint --reporter=node_modules/jshint-stylish/stylish.js file.js

# jshint-stylish 2.0.0を利用するコード
$ jshint --reporter=node_modules/jshint-stylish file.js
```

[npmに登録される多くのライブラリではSemVerが採用されており](https://docs.npmjs.com/getting-started/semantic-versioning)、利用者は `^1.0.0` のように宣言しておくことで `1.y.z` のメジャーバージョンをまたがない最新バージョンを安全に使い続けられる。jshint-stylishのように破壊的な変更がメジャーバージョン番号の更新で通知されれば、ライブラリ利用者は慎重にバージョンアップを検討することが可能になる。

## SemVerを守られないと混乱する

よくある勘違いの一つに、次のような理由からメジャーバージョン番号を上げてしまうケースがある。

* 革新的な新機能が追加された
* APIを保ったままコードを大幅にリファクタリングした

確かに商用ソフトウェアでこのようなメジャーバージョンアップが行われることはあるが、**こういった商用ソフトウェアは最初からSemVerを採用していない**点に注意が必要である。利用者がSemVerを期待している時に、商用ソフトウェアの真似をしてはならない。利用者が混乱するからである。
