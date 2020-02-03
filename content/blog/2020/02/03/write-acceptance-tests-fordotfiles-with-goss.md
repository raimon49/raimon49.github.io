Title: dotfilesのためのAcceptance Testをgossで宣言的に記述する
Date: 2020-02-03 20:35:25
Category: Git
Tags: CI, Git, Go
Slug: write-acceptance-tests-fordotfiles-with-goss
Authors: raimon
Summary: Gitでdotfilesを管理している時のAcceptance TestをCLIツールgossで宣言的に管理する手順について

## dotfilesで保証したいテスト

ソフトウェアエンジニアで、自身のHOMEディレクトリ以下に設置するファイル群（いわゆるdotfiles）をGitで管理している人はそこそこ居ると思う。

ポピュラーなやり方は、GitHubに代表されるGitリポジトリをホストできるサービスで管理し、手元に `git clone` して持ってきて `setup.sh` や `install.sh` のようなスクリプトを実行し、Git管理下のファイル群をHOMEディレクトリにコピーしたりシンボリックリンクを作成する流れである。

長くGitで管理していると、時々ふっと改善したい意欲が湧き上がってきて、かなりの量を書き直した結果、インストールスクリプトの結果が壊れてしまった経験は無いだろうか。これはなかなかにつらい経験である。壊れないことをテストで保証したいと考えるのは、エンジニアの自然な欲求だ。

いわゆるユニットテストというよりはAcceptance Test（受け入れテスト）に相当するものである。この記事ではCLIツール[goss](https://github.com/aelsabbahy/goss)を使って、YAMLベースで「インストールスクリプトを実行後になっていて欲しい状態」を宣言的に記述し、テストさせる手法を紹介する。

## gossでHOMEディレクトリ以下のファイル構成を宣言的に記述

gossはGoで書かれたCLIツールで、Serverspecに影響を受けたとされている。YAMLベースで宣言的に記述できる点に加えて、Goでコンパイルされているため、Rubyなどの実行環境を必要とせず、バイナリを手元に持ってくればすぐ使える点も便利である。

```sh
# 手元の~/bin以下にgossコマンドをダウンロードして配置
$ curl -fsSL https://goss.rocks/install | GOSS_DST=~/bin sh
```

リファレンス的な内容な[goss manual](https://github.com/aelsabbahy/goss/blob/master/docs/manual.md)に譲るが、dotfilesの受け入れテストを書く上で、専ら使うのは `file` テストである。

例えば、HOME以下に `.bashrc` がシンボリックリンクとして作成されていることを期待するのであれば、次のように記述する。

```yaml
file:
  ~/.bashrc:
    exists: true
    filetype: symlink # cpしているのであれば「symlink」でなく「file」と記述
```

YAMLを `goss.yaml` という名前で保存し、次のようにコマンドラインから実行すると、YAMLでの期待値に対して検査が実行され、結果が出力される。期待通りであればコマンドは成功し、YAMLの記述と違っていれば、終了コードが `1` となりコマンドは失敗する。

```bash
$ ~/bin/goss --gossfile goss.yaml validate --format documentation
File: ~/.bashrc: exists: matches expectation: [true]
File: ~/.bashrc: filetype: matches expectation: ["symlink"]


Total Duration: 0.002s
Count: 2, Failed: 0, Skipped: 0
```

gossファイルは分割にも対応している。例えば、Gitの設定ファイルだけ集約した `git.yaml` をインクルードして検査するなら、 `goss.yaml` は次のように記述する。

```yaml
gossfile:
  git.yaml: {}
```

分割したGitの設定ファイル群に関する受け入れテストでは、新規セットアップしたサーバーなどでやりがちな `git config` やり忘れを防止するために `file` テストの `contains` と組み合わせて、中身も期待するものが配置されているか検査してみよう。例えば、エンジニアBobが自分のコミットログに記述される名前がちゃんと `.gitconfig` に入っているか検査したいなら、こう記述できる。

```yaml
file:
  ~/.gitconfig:
    exists: true
    filetype: symlink
    contains:
      - "name = Bob"
      - "email = bob@example.com"
  ~/.config/git/ignore:
    exists: true
    filetype: symlink
```

検査の実行時は、 `goss.yaml` のみを指定すれば、インクルード先の `git.yaml` で宣言した記述についても一緒に検査される。

```bash
$ goss --gossfile goss.yaml validate --format documentation
File: ~/.gitconfig: exists: matches expectation: [true]
File: ~/.gitconfig: filetype: matches expectation: ["symlink"]
File: ~/.gitconfig: contains: patterns expectation: [name = Bob, email = bob@example.com]
File: ~/.config/git/ignore: exists: matches expectation: [true]
File: ~/.config/git/ignore: filetype: matches expectation: ["symlink"]


Total Duration: 0.006s
Count: 6, Failed: 0, Skipped: 0
```

## CIツールで自動実行させる

ここまで来たら、あとはCIツール、いわゆるCI-as-a-Serviceで自動実行させて、面倒なことは機械に任せよう。dotfilesをガシガシと改善したい欲が高まってリファクタリングした結果、もしインストールスクリプトの結果が壊れてしまっても、CIツールが通知してくれる。

例としてTravis CIでの記述を掲載する。CircleCIやGitHub Actionsなど、Travis以外を使っている人は適宜で読み替えて欲しい。

```yaml
language: sh
addons:
  apt:
    packages:
    - git
script:
- ./setup.sh
- "curl -fsSL https://goss.rocks/install | GOSS_DST=~/bin sh"
- "${HOME}/bin/goss --gossfile goss.yaml validate --format documentation"
```

基本的な流れは同じなので、どのCIツール上で実行させるにしても、次の順になる。

1. テスト実行の先頭ステップやbeforeフックで自身のdotfilesインストールスクリプト（上の例では `setup.sh` を実行）
2. gossコマンドのインストール（or インストールスクリプトに含めてしまってもよい）
3. インストールスクリプト実行後の期待する構成（goss.yaml）を使ったgossコマンドでの検査

## まとめ

* dotfilesのセットアップ後の状態をAcceptance Test（受け入れテスト）で書いておくと、大幅に構造を変えた結果として壊れてしまった時に検知できる。
* CLIツールgossでは、YAMLベースで受け入れテストが手軽に記述できて、dotfilesリポジトリにも導入し易い。
