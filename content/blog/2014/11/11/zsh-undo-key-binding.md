Title: zshでファイル名グロブを展開した後にアンドゥできる事を知った
Date: 2014-11-11 18:45:00
Modified:
Category: zsh
Tags: zsh
Slug: zsh-undo-key-binding
Authors: raimon
Summary: zshでファイル名グロブの記号をTabキー展開した後に記号に戻す方法があった。

zshでファイル名グロブの記号をTabキー展開した後に記号に戻す方法があった。

一度展開してしまうと戻せないものだと思い込んでいたが違った。

## 結論

`Ctrl+x` - `u` でと入力してアンドゥ操作することで直前の記号に戻る。

## 詳細

zshで次のように入力した状態で、 `Tab` キーを押すと、コマンド実行前に記号がマッチするファイルが展開される。

```bash
# Tabキーを押す
$ ls *user.js

# 展開される
$ ls feedburner_tracking_cutter.user.js
feedburner_tracking_cutter.user.js  minimum_scroll.user.js              show_yahoo_news_detail_p.user.js
ldc_rancor_cool.user.js             read_two_ahead_feed_on_ldr.user.js  wikipedia_redirect_keyword.user.js
ldr_auto_expand_all_rating.user.js  show_time_on_ldr.user.js
```

展開された後に、元の記号に戻したい事が多々あって、どうやるのか知らなかったのだけど、アンドゥ操作で戻せるのだった。

アンドゥはEmacsキーバインドを設定している場合、先述した `Ctrl+x` - `u` と入力する。

```bash
# Ctrl+x - xと押す
$ ls feedburner_tracking_cutter.user.js
feedburner_tracking_cutter.user.js  minimum_scroll.user.js              show_yahoo_news_detail_p.user.js
ldc_rancor_cool.user.js             read_two_ahead_feed_on_ldr.user.js  wikipedia_redirect_keyword.user.js
ldr_auto_expand_all_rating.user.js  show_time_on_ldr.user.js

# 元に戻った
$ ls *user.js
```

ちなみに、名前の通りアンドゥなので、連続的に `Ctrl+x` - `u` を押すと、入力した文字がどんどん消えて行く。

```bash
# さらに戻る
$ ls *user.j

# さらに戻る
$ ls *user.
```
