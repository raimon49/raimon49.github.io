Title: svn:ignoreの無視ファイル設定を.gitignoreに移行する
Date: 2015-01-27 23:13:00
Modified:
Category: Git
Tags: Git, Subversion
Slug: migrate-ignore-from-svn-to-git
Authors: raimon
Summary: Subversionリポジトリからの変換・移行ツールsvn2gitでの移行時に無視ファイル設定も移行したい。

SubversionからGitに完全移行したい際には[svn2git](https://github.com/nirvdrum/svn2git)というRubyGemsで配布されているツールを使う事が多い。

この時、Subversionリポジトリで設定していたバージョン管理外としたいファイルの無視リストである「svn:ignore」属性は、変換されたGitリポジトリに引き継がれない。

公式issueを見ても対応予定が無さそうだったので、無視リストの移行方法を調査・検討した。

## git-svnのサブコマンドshow-ignoreを使う

システム任せに移行する方法の一つとして、git-svnリポジトリ形式に変換すると使える[create-ignoreやshow-ignore](http://git-scm.com/book/ja/v1/Git%E3%81%A8%E3%81%9D%E3%81%AE%E4%BB%96%E3%81%AE%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%81%AE%E9%80%A3%E6%90%BA-Git-%E3%81%A8-Subversion)がある。

先述のsvn2gitでは完全なGitリポジトリ形式に変換されてしまっているため、これとは別途で次のように用意する。

```bash
# Subversion側のHEADコミットだけあれば良い
$ git svn clone -r HEAD -s /path/to/svn/repo my-git-svn
$ cd my-git-svn

# 「svn:ignore」をまとめて標準出力し確認
$ git svn show-ignore

# .gitignoreとして使用
$ git svn show-ignore > .gitignore
```

Subversion側のリビジョンが育っている場合、このコマンドはかなり待たされる。

## svn pgetコマンドの結果を加工する

checkoutしたSubversionリポジトリの「svn:ignore」属性を再帰的に取得し、加工する方法もある。

```bash
# Subversion側のHEADコミットだけあれば良い
$ svn co -r HEAD /path/to/svn/repo/trunk repo/trunk
$ cd repo/trunk

# 「svn:ignore」属性を再帰的に取得
$ svn pget svn:ignore -R

# 取得結果を加工して.gitignoreの雛形として出力し確認
$ svn pget svn:ignore -R | grep -v "^$" | sed "s/\(\(.*\) - \)\(.*\)/\2\/\3/g" | sort

# .gitignoreとして使用
$ svn pget svn:ignore -R | grep -v "^$" | sed "s/\(\(.*\) - \)\(.*\)/\2\/\3/g" | sort > .gitignore
```

## その他のSubversionで使っていた属性

Subversionのディレクトリ単位で付与できる属性は「svn:ignore」以外にも色々あるが、引き継いで持って行きたいものは「svn:externals」くらいだろう。以下のようにするとリスト出力できる。

```bash
$ svn plist -v -R
```

「svn:externals」属性で外部参照していたリポジトリも自分達の管理下にあるソースツリーであれば、同様にsvn2gitで変換してgit-submoduleまたはgit-subtreeで代替させるのが良いと思われる。3rd party管理下の場合は、丸ごと食わせるか、自分達でGitリポジトリを用意するか、いずれにしろ諦めて二重管理が発生することになる。

以下の属性は、Gitへ完全移行できたなら不要と考えて良い。

* svn:executable
* svn:mime-type
* svn:eol-style
* svn:keywords

特にキーワード展開はCVS時代からの呪いのように使いたがる人が居るが、git-blameの情報で十分なので、無理に努力してノイズになるような情報を別途で埋め込む必要は無い。
