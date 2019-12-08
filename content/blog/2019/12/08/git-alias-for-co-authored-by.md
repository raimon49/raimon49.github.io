Title: Co-authored-by署名を手軽に付与するためのGit alias
Date: 2019-12-08 11:04:40
Category: Git
Tags: Git, GitHub
Slug: git-alias-for-co-authored-by
Authors: raimon
Summary: Gitコミット時に付与するCo-authored-by署名のために設定するGit aliasと、その効果について。

GitHubで[コミット時に複数の作者情報を署名する"Co-authored-by"](https://help.github.com/ja/github/committing-changes-to-your-project/creating-a-commit-with-multiple-authors)という機能がある。

リンクしたGitHub Helpで解説されている通り、GitHub Web UIからは、入力補助で比較的簡単に共同作者によるコミットメッセージが作成できる。

開発者としてはコマンドライン上でコミットメッセージ作成する際も、手軽に入力したいところではある。インターネット上でやり方を探してみても、なかなか「これ」といった情報が見付からず、何かの役に立つかも知れないため自分の中でそこそこ上手く行っている知見を書いてみたい。

なるべく外部CLIツールに依存したくないため、全てGitの標準機能（Git aliasなど）で実現している。

**"Co-authored-by"機能自体は、チームビルディングやアジャイル開発の文脈において非常に有用であり、積極的に使うことが望ましいと考えている。**記事の後半では、"Co-authored-by"で署名する事で期待できる効果についても考察や私見を述べる。

## コマンドライン上でのコミット例

紹介するGit設定を使ってターミナル上からコミットする例を画像で示す。次のようなシナリオである。

* あなたはアリスとボブと同じチームに所属している。
* 今日は `CONTRIBUTING.md` にGitリポジトリのセットアップ方法を追記した。
* このドキュメントを編集したのはあなたで、ボブも同席して編集内容のレビューやフィードバックを行った。アリスは離席していた。
* コミットメッセージとして、同席していたボブとの共同作者であることを明記するため `Co-authored-by: Bob <bob@example.com>` を付与した。アリスは同席していなかったため、"Co-authored-by"による署名を有効にしなかった。

<img src="/images/create-git-co-authored-commit.gif" alt="コマンドラインからCo-authored-by情報をコミットするサンプル" width="575px" height="437px" style="width: 668px; max-width: 100%; height: auto;">

## 必要なGitの設定

先ほどのコミット例のようにコミットメッセージに同席者を用意しておくために設定を仕込んでおくファイルは次の通りである。

ディレクトリ `repo` はGitHubなどのリモートサーバーから `git clone` されたGitリポジトリを指す。

```bash
$ tree ~
.
|-- .gitconfig
|-- .config
|   `-- git
|       `-- ignore
|-- git-co-authors.txt
`-- repo
    `-- git-co-authors.txt
```

設定するファイルを順番に見て行く。

### ~/.gitconfig（Git aliasの設定）

`~/.gitconfig` では、Git aliasの設定を記述する。

```bash
[alias]
	ci = commit -v
	cimob = "!git commit -v --template=$(for i in $(git rev-parse --show-toplevel)/git-co-authors.txt ${HOME}/git-co-authors.txt; do [ -f $i ] && echo $i && break; done)"

```

* `commit -v` オプションは、コミット時に差分情報を表示する。普段は `git ci` でコミットしていて、共同作者情報をコミットメッセージに含めたい時は別途用意したaliasを使う。
* `git cimob` が実行された時、 `commit --template` オプションで作者情報の記述されたファイル `git-co-authors.txt` を指定する。
    * `cimob` は別に `cipair` でも構わないし、短いaliasが好みなら `cim` でも良い。自分の覚えやすいものを設定する。
    * `git-co-authors.txt` というファイル名も、とくに決まりのあるものではない。面倒なら `authors.txt` でも何でも、好みの名前で構わない。
* `git cimod` 実行時のシェルスクリプトでは、2箇所の `git-co-authors.txt` を探索する。
    * コミット時に作業しているGitリポジトリのトップ、今回の例では `~/repo/git-co-authors.txt` が存在すれば、そちらをテンプレートファイルとして指定する。
    * Gitリポジトリ直下に `git-co-authors.txt` が見付からない時は、HOMEディレクトリの `~/git-co-authors.txt` をテンプレートファイルとして指定する。

### ~/.config/git/ignore（無視設定ファイル）

`git-co-authors.txt` がコミット対象に含まれないよう、 `~/.config/git/ignore` に記述しておく。

```bash
# Template for co-authored commits
git-co-authors.txt
```

ただ、チーム内として同じファイルをコミットテンプレートに採用する共通認識が取れているのであれば、敢えて無視設定をせずGitリポジトリにコミットしてしまっても良いように思われる。

### git-co-authors.txt（共同作者に入れる人のテンプレート）

`git-co-authors.txt` では、Gitコミットする際に"Co-authored-by"で署名したい人のアカウントを列挙する。繰り返しになるが、ファイル名はとくに決まっている訳ではない。

* `~/repo/git-co-authors.txt`では、対象Gitリポジトリの共同メンテナを列挙しておく
* `~/git-co-authors.txt` では、Gitリポジトリに `git-co-authors.txt` が見付からなかった際にフォールバックして使われるため、特定のプロジェクトに限定せず、よく共同作業する人を列挙しておく。

このファイルは以下のような内容となっている。署名の上に空行が必要な点に注意されたい。実際に設定してみると分かる。

```bash


# Co-authored-by: Alice <alice@example.com>
# Co-authored-by: Bob <bob@example.com>
```

署名部分は、必ずしもコメントアウト状態でなくても構わない。例えば、常にAliceとペアワークしていて必ず共同作者としてコミットメッセージに含めるなら、Aliceのアカウント情報は最初からコメントアウトせず有効行として用意しておいた方が便利である。

## "Co-authored-by"コミットの活用場面とその効果

"Co-authored-by"コミットは、GitHubで使われ始めた事からも明らかな通り、オープンソース製品を複数人で育てて行く上で有用であるが、例えばGitHub Enterpriseのように企業内ホスティング環境でも良い効果があると考える。

とくに次のようなロールの人は、GitHubには複数の作者情報を付与する機能があることを理解し、場面によっては率先して使うことが望ましい。

* Engineering Manager
* Scrum Master
* Tech Lead

この機能を使うと役立つ場面について私見を述べる。

### Pull Requestレビューを受けた結果をコミット

Pull Requestでレビューコメントを受けて、実装を変更してコミットする際に、"Co-authored-by"としてレビュワーのアカウント情報を付与する。

誰のレビューで変更したか明確になるし、レビュワー側もより良いフィードバックを継続するモチベーションになる。

### プロジェクト内の規約や方針の合意内容をコミット

コード規約やGitリポジトリレイアウト、特定のフレームワーク採用を決定した際などで、その場に居た全員を"Co-authored-by"としてコミットメッセージに含めておく。

こうすることで、チームにおける規約や合意内容は、全員の成果である共通認識が生まれる。とくにScrum MasterやTech Leadといった人が覚えておくと良いテクニックである。

### ペアプログラミングやモブプログラミングにおけるコミット

アジャイル開発におけるメジャーな手法として、ペアでの作業や、3人以上（モブ）での作業をするペアプロ・モブプロがある。この時にドライバーがコミットメッセージを作成する際、ナビゲーターのアカウントを"Co-authored-by"として記述する。

ナビゲーターの意識が目の前の作業に集中し易くなり、ペアワークやモブワークに同席できなかったEngineering Managerも、コミットログを辿ることで、チームがどんな作業をしたか、チームの状態が健全かチェックできる。

とくにペアプロやモブプロでは、作業の得意な特定メンバーだけがずっと操作役のドライバーを担当していないか、注意して観察する必要がある。ドライバーが"Co-authored-by"の署名をしてくれると、この辺りに偏りが生じていないか知る手掛かりにもなる。

### 1on1やミーティング議事録におけるネクストアクションを記録するコミット

組織によってはEngineering ManagerやTech Leadがチームメンバーと週次で1on1を行う事がある。また、チーム全員で集まって振り返りの場を設定する事もある。これらの場で出されたネクストアクションや合意事項も、ドキュメント置き場としてGitHub Enterpriseを採用しているのであれば、参加者のアカウントを"Co-authored-by"に含めておくと良い。

ネクストアクションを生んだ共同作者として記録される事で、「決まったまま次のミーティングまで実行されないネクストアクション」を予防する効果が期待できる。

## まとめ

GitHubの複数の作者情報を署名する"Co-authored-by"機能をコマンドラインから手軽に入力するための設定方法と、この機能を使うと良い場面や期待される効果について書いた。

かれこれ半年間ほど使ってみて、思った以上にチームへ良い影響を与えている実感があるため、広まって欲しいと思っている。コマンドラインからコミットする際の知見はあまり先行事例が見付からなかったため、色んなやり方が共有される事を望んでいる。
