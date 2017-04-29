Title: VimでPipfileを構文ハイライトされた状態で編集
Date: 2017-04-29 20:39:28
Category: Vim
Tags: Python, Vim
Slug: support-syntax-for-pipfile
Authors: raimon
Summary: Pythonの新しい依存パッケージ管理ファイルフォーマットであるPipfileを構文ハイライトされた状態で編集する方法

Pythonの `requirements.txt` に変わる新しい依存パッケージ管理用に開発が進められている[Pipfile](https://github.com/pypa/pipfile)をVimで編集する際の設定方法についてまとめる。

## TOMLとJSONに適したVimの構文ハイライト用プラグインを導入

まず `Pipfile` はTOMLベース、バージョンロックを書き出して記録する `Pipfile.lock` はJSONベースであるため、それぞれ適したVimの構文ハイライト用プラグインを導入しておく。

JSONに関しては、元々Vimでサポートされているが、よりベターな実装があるため、そちらを利用するのがおすすめである。

* [vim-toml](https://github.com/cespare/vim-toml)
* [vim-json](https://github.com/elzr/vim-json)

## それぞれのファイル読込時に構文ハイライトを適用させる

あとは、それぞれのファイル読込時に、ファイル名で判定して構文ハイライトを適用してやれば綺麗に編集できるようになる。

```vim
au BufNewFile,BufRead Pipfile setf toml
au BufNewFile,BufRead Pipfile.lock setf json
```

例として `Pipfile` と `Pipfile.lock` それぞれのファイル編集時に構文ハイライトが適用された編集画面のキャプチャを紹介しておく。なお現行の依存パッケージ管理ファイルフォーマットである `requirements.txt` 編集時は[requirements.txt.vim](https://github.com/raimon49/requirements.txt.vim)を導入すると同様の事が可能になる。


<img src="/images/edit_pipfile.png" alt="構文ハイライトが適用された編集画面" width="605px" height="506px" style="width: 605px; max-width: 100%; height: auto;">
