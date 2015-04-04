Title: Gitのsubmoduleをお手軽に削除する
Date: 2015-04-04 21:00:00
Modified:
Category: Git
Tags: Git, Pelican
Slug: git-submodule-deinit
Authors: raimon
Summary: Gitのsubmoduleをお手軽に削除するdeinitコマンドについて

このブログに適用しているPelicanのテーマを乗り換えた。

## submoduleで参照していた外部リポジトリを削除

[最初のエントリにも書いた](/2014/11/09/start-tech-blog-by-pelican.html)通り、[ブログのリポジトリ](https://github.com/raimon49/raimon49.github.io)では外部テーマを以下のように `vendor/theme-name` というパスで外部参照している。

```sh
repo
`-- vendor
    `-- theme-name
```

今回はmolivierさんの[nest](https://github.com/molivier/nest)というテーマに乗り換えたため、これまで使っていたテーマの外部参照は、ブログの記事を生成する際には不要となる。

Gitのsubmoduleを削除するのは、以前は面倒な手順が必要だったが、最近は `git submodule deinit` を使うと簡単らしい。今回もこんな感じで `.git` 以下のメタファイルは編集しなくても削除できた。

```sh
# submodule deinitでクリーンアップ
$ git submodule deinit vendor/pelican-sober
Cleared directory 'vendor/pelican-sober'
Submodule 'vendor/pelican-sober' (git://github.com/fle/pelican-sober.git) unregistered for path 'vendor/pelican-sober'

# ファイルパスを削除
$ git rm vendor/pelican-sober
rm 'vendor/pelican-sober'

$ git status -s
M  .gitmodules
D  vendor/pelican-sober

# コミットして反映
$ git commit -a
```

これを `pull` している側の反映手順でハマッた事があって、その時の対応方法は [Gistに書いた](https://gist.github.com/raimon49/9719585)。

## git-submodule(1)

マニュアル `git-submodule(1)` も引用して貼っておく。

>     deinit
>         Unregister the given submodules, i.e. remove the whole submodule.$name section from .git/config together with their
>         work tree. Further calls to git submodule update, git submodule foreach and git submodule sync will skip any
>         unregistered submodules until they are initialized again, so use this command if you don’t want to have a local
>         checkout of the submodule in your work tree anymore. If you really want to remove a submodule from the repository and
>         commit that use git-rm(1) instead.
>
>         If --force is specified, the submodule’s work tree will be removed even if it contains local modifications.
