Title: manコマンドで表示されるドキュメントの色付けをカスタマイズ
Date: 2017-03-31 17:35:00
Category: zsh
Tags: zsh
Slug: man-with-colored-pager
Authors: raimon
Summary: manコマンドで表示されるドキュメントの色付けを見易く設定する方法について。

## PAGERで開いた時の標準色付けだと見づらい

環境変数 `$PAGER` を設定している状態で `man` コマンドでドキュメントを表示すると色付けしてくれるが、標準では見づらい。

```sh
export PAGER=lv
export LV="-Ou8 -c"
```

例えば上記のように `lv` を指定していると、次のように色付けして出力される。

<img src="/images/less_noncolor.png" alt="標準の色付け出力" width="1054px" height="464px" style="width: 1054px; max-width: 100%; height: auto;">

## それぞれのPAGERで色付けをカスタマイズ

`lv` や `less` ではカラーコードを指定して色付けをカスタマイズが可能である。自分は次のような色付け設定に落ち着いている。

<img src="/images/less_with_color.png" alt="カスタマイズした色付け出力" width="1053px" height="456px" style="width: 1053px; max-width: 100%; height: auto;">

`lv` では環境変数 `$LV` でカラーコードを指定する。

```sh
export LV="-Ou8 -c -Sh1;36 -Su1;4;32 -Ss7;37;1;33"
```

環境によっては `lv` がインストールされていない場合もある。そのため `less` も互換性を持つ配色にしておくと困らない。 `$LESS_TERMCAP_` から始まる環境変数にエスケープシーケンスを出力するように設定しておく。

```sh
man() {
    env \
        LESS_TERMCAP_mb=$(printf "\e[1;36m") \
        LESS_TERMCAP_md=$(printf "\e[1;36m") \
        LESS_TERMCAP_me=$(printf "\e[0m") \
        LESS_TERMCAP_se=$(printf "\e[0m") \
        LESS_TERMCAP_so=$(printf "\e[1;44;33m") \
        LESS_TERMCAP_ue=$(printf "\e[0m") \
        LESS_TERMCAP_us=$(printf "\e[1;32m") \
        man "$@"
}
```

自分好みのカラーコードを設定するには、[bash:tip\_colors\_and\_formatting](http://misc.flogisoft.com/bash/tip_colors_and_formatting)のようなページを参考にするとよい。
