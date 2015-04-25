Title: 静的ページジェネレータHexoで作成したブログをGitHub Pagesで公開する
Date: 2015-04-25 18:02:22
Modified:
Category: Node
Tags: GitHub, Hexo, Node, Pelican
Slug: create-blog-with-hexo
Authors: raimon
Summary: 静的ページジェネレータHexoを使ってブログを作る時の手順

JavaScript / Node製の静的ページジェネレータである[Hexo](https://github.com/hexojs/hexo)を使い、[GitHub Pages](https://pages.github.com/)で公開する手順について調べたのでまとめておく。

## 動機

調べた動機としては、

* 人気が上昇傾向で、特に中華圏での採用例が増えつつあるので使ってみたかった
* Node / npmの勉強用
* 日本語の解説記事では古いバージョンのものが多く、現行バージョン3.x系では変わってしまった手順が多々あった

などが挙げられる。

[Static Site Generators](https://staticsitegenerators.net/)から引くと、GitHub Starの付けられた数が2015-04-25現在、3位に居る。このブログでも利用しているPelicanは抜かれて4位となっていた。

![GitHub Starによるソート順](/images/static-site-generators-sort-by-star.png)

少なくとも2014年末時点ではPelicanの方が上だった筈だが、現在はHexoよりも上に居るのはGitHub上で人気のあるRuby製のJekyllとOctopressの2つだけとなっており、かなり勢いがあると言える。

## ブログの準備

今回の環境は

* Node 0.12.2
* npm 2.7.4

を使っている。Node本体は0.10.x系でも問題無く動く筈である。

Hexoのオフィシャルなインストール方法は `npm install hexo-cli -g` だが、なるべくグローバル領域にインストールしない形で進めたいと考えて、実際にやってみたら可能だった。

Gitリポジトリとしたいディレクトリに `hexo-cli` をローカルインストールし、`$(npm bin)` で実行コマンドのあるパスを取得してブログを準備する。

```sh
$ npm install hexo

$ $(npm bin)/hexo init blog
INFO  Copying data to ~/works/git/hexo-use-sample/blog
INFO  You are almost done! Don't forget to run 'npm install' before you start blogging with Hexo!
```

引数で指定した `blog` という名前のディレクトリが生成されているので、そこに入って `package.json` に書かれた依存ライブラリをローカルインストールする。

これだけで、 `hexo serve` コマンドでローカルサーバが立ち上がり、 `4000` ポートにウェブブラウザからアクセスすると、Hello, World記事のあるブログ画面が表示される。

```sh
$ cd blog
$ npm install
$ $(npm bin)/hexo server
INFO  Hexo is running at http://0.0.0.0:4000/. Press Ctrl+C to stop.
```

![Hello, Worldブログ画面](/images/hexo-hello-world.png)

Hexoのインストールを確認したら、一旦 `Ctrl+C` でストップする。

## ブログのテーマをインストールする

Hexoにも他のツールと同様に多数のテーマが用意されている。

テーマは[プロジェクトWikiページ](https://github.com/hexojs/hexo/wiki/Themes)でリスト化されている。今回はこの中から[Hueman](https://github.com/ppoffice/hexo-theme-hueman)というテーマをインストールした。

Hexoにおけるテーマのインストール方法は、ブログ内のディレクトリ `themes` 以下に、テーマのGitリポジトリを丸ごとクローンして入れるという原始的な手順らしい。これは `themes/theme-name/_config.yml` も評価して静的ページ生成するというHexoの設計も関係しているようだ。

```sh
$ git clone git://github.com/ppoffice/hexo-theme-hueman themes/hueman
```

長期的に運用して行きたい場合は、[Git Subtree](http://japan.blogs.atlassian.com/2014/03/alternatives-to-git-submodule-git-subtree/)による管理を検討すると良いだろう。Git Submoduleは純粋に外部リポジトリの参照であるため、テーマリポジトリ内の設定ファイル変更をコミットしておけないからだ。

テーマのGitリポジトリを取得したら、`blog/_config.yml` で指定してデザインを適用する。

```diff
--- a/blog/_config.yml
+++ b/blog/_config.yml
@@ -3,11 +3,11 @@
 ## Source: https://github.com/hexojs/hexo/

 # Site
-title: Hexo
+title: Hexo Use Sample Blog
 subtitle:
 description:
-author: John Doe
-language:
+author: raimon
+language: en
 timezone:

 # URL
@@ -62,9 +62,9 @@ pagination_dir: page
 # Extensions
 ## Plugins: http://hexo.io/plugins/
 ## Themes: http://hexo.io/themes/
-theme: landscape
+theme: hueman
```

Hexoの特徴として、中華圏のユーザーコミュニティが非常に厚く、テーマもデフォルトで言語設定が中国語となっているものが多い。

よって `language: en` としないと、メニューが中国語になってしまうテーマが幾つも見受けられた。Huemanテーマも同様だった。

この状態で先ほどと同様にローカルサーバを立ち上げると、ブログのデザインが変わっていることが確認できる。

## 記事を投稿する

テーマの設定が完了したので、記事を作成してみる。

自動生成されたHello, World記事はもう不要になるため消してしまい、`hexo new` コマンドで自分の記事を作成する。

```sh
$ git rm source/_posts/hello-world.md
rm 'blog/source/_posts/hello-world.md'
$ git commit -m 'Remove hello world post'

$ $(npm bin)/hexo new "hello-my-post"
INFO  Created: /path/to/repo/hexo-use-sample/blog/source/_posts/hello-my-post.md
```

ローカルサーバで確認してOKだったら `git commit` する。

## ブログをGitHub Pagesで公開する

Hexoは設定ファイルでブログの公開先としてGitリポジトリが指定できる。

この辺りはバージョン3.x系では別プラグインとして切り離されており、インストールが必要である。

```sh
$ npm install hexo-deployer-git --save
```

今回は次のような設定で公開することにした。

* リポジトリ名: `hexo-use-sample`
* ブランチ名: `gh-pages`
    * `master` ブランチでは記事の生成元となるMarkdown文書などを管理
* URL: `http://{username}.github.io/hexo-use-sample/`

実際に `blog/_config.yml` に反映すると以下のようになる。`type: git` となっている点は注意（古いバージョンでは `type: github` になっている）。

```diff
--- a/blog/_config.yml
+++ b/blog/_config.yml
@@ -12,8 +12,8 @@ timezone:

 # URL
 ## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
-url: http://yoursite.com
-root: /
+url: http://raimon49.github.io/hexo-use-sample/
+root: /hexo-use-sample/
 permalink: :year/:month/:day/:title/
 permalink_defaults:

@@ -67,4 +67,6 @@ theme: hueman
 # Deployment
 ## Docs: http://hexo.io/docs/deployment.html
 deploy:
-  type:
+  type: git
+  repo: git@github.com:raimon49/hexo-use-sample.git
+  branch: gh-pages
```

また、グローバルではなくローカルに `hexo-cli` をインストールした関係で、コマンド実行時に都度 `$(npm bin)` で実行パスを取得していたが、`npm-scripts` に定義して、覚えておかなくて良いようにする。

```diff
--- a/blog/package.json
+++ b/blog/package.json
@@ -5,15 +5,21 @@
   "hexo": {
     "version": "3.0.1"
   },
+  "scripts": {
+    "start": "hexo server",
+    "create": "hexo new",
+    "deploy": "hexo deploy -g"
+  },
   "dependencies": {
     "hexo": "^3.0.0",
+    "hexo-deployer-git": "0.0.4",
     "hexo-generator-archive": "^0.1.0",
```

参考記事として[npm-scriptsについて](http://qiita.com/axross/items/a2a0d148e40b66074858)と[npm で依存もタスクも一元化する](http://qiita.com/Jxck_/items/efaff21b977ddc782971)を挙げておく。

これで `package.json` の実行タスクが定義された。その中から `deploy` を実行すると、`master` ブランチの内容から静的ページが生成されて `gh-pages` ブランチとしてpushまで行き、自動的にGitHub Pagesで公開される。

```sh
$ npm run
Lifecycle scripts included in hexo-site:
  start
    hexo server

available via `npm run-script`:
  create
    hexo new
  deploy
    hexo deploy -g

$ npm run deploy

> hexo-site@0.0.0 deploy /home/raimon49/works/git/hexo-use-sample/blog
> hexo deploy -g

Branch master set up to track remote branch gh-pages from git@github.com:raimon49/hexo-use-sample.git.
INFO  Deploy done: git
```

また、新しい記事の作成も次回からは `npm-scripts` を使って可能になった。

```sh
$ npm run create "hexo-dependency
```

今回公開した記事は次のようなデザイン・内容になった。

* [Hello my post](http://raimon49.github.io/hexo-use-sample/2015/04/25/hello-my-post/)
* [hexo-dependency](http://raimon49.github.io/hexo-use-sample/2015/04/25/hexo-dependency/)

タグを複数指定したい時は、記事生成元のMarkdownで `tags: [GitHub, Hexo]` のように `[]` で囲って並べると可能なようだ。

## まとめと感想

* Hexoはグローバル領域にツールをインストールしなくても使えると分かった
* テーマインストールの項でも触れたが、中華圏のユーザーコミュニティが非常に活発で、詰まってFAQなどで情報を探した時にも実感した
* 記事のMarkdownテンプレートを作ってくれたり、デプロイまで面倒を見てくれるコマンドラインツールの機能は便利だった
* ブログに特化しており、インストールしてすぐに画面を確認できる点も良い
    * このお手軽さから、Static Site Generatorsでもっと上に行くかも知れないと感じた
