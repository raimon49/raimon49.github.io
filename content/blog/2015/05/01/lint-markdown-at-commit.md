Title: コミット時にMarkdownファイルの構文が正しいかnpm testでチェックさせる
Date: 2015-05-01 20:05:32
Modified:
Category: Node
Tags: CI, Git, Markdown, Node
Slug: lint-markdown-at-commit
Authors: raimon
Summary: Hexoで作成したブログのリポジトリに対してコミット時にMarkdownファイルの構文チェックを走らせ、失敗時にはコミットを中止させるようにした

[静的ページジェネレータHexoで作成したブログをGitHub Pagesで公開する](/2015/04/25/create-blog-with-hexo.html)の記事で作成したブログのGitリポジトリに対して、コミット時にMarkdownファイルの構文チェックさせる方法は無いか調べた。

## 依存ツール

次のツールを利用することで可能だった。

* [husky](https://github.com/typicode/husky)
    * コミットやプッシュ時のGit hookを自動で作成してくれる
    * インストールすると `package.json` でこれらのタイミングに対して実行する `run-script` が定義可能になる
* [markdownlint](https://github.com/DavidAnson/markdownlint)
    * [カスタマイズ可能なルールベース](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)でMarkdownファイルの構文が妥当かチェックできるJavaScript APIが提供される
    * RubyGems向けに作られた[Markdownlint](https://github.com/mivok/markdownlint)のポーティングらしい
* [glob](https://github.com/isaacs/node-glob)
    * Markdownファイルをまとめて構文チェックに渡す際に使う
    * Grunt/Gulpといったタスクランナーを使う場合は、同様の事が可能なため、不要だと思われる

これらを `--save-dev` オプションを指定してインストールする。

```sh
$ npm install markdownlint husky glob --save-dev
```

## テストを書く

`test/markdown.js` として、Hexoのブログ記事生成元となるMarkdownファイル全体を構文チェックするテストを記述する。

`options.config` には [relaxed.json](https://github.com/DavidAnson/markdownlint/blob/master/style/relaxed.json)のようなJSONファイルで定義したルールを渡しても良いようだ。

`var result = markdownlint.sync(options)` で同期的に実行したチェック結果が返るので、その文字列表現としてエラー情報が取得できたか否かを見ている。

```javascript
var markdownlint = require("markdownlint"),
    glob = require("glob"),
    options = {
        "files": glob.sync("blog/source/_posts/*.md"),
        "config": {
            "default": true,
            "MD007": {"indent": 4}
        }
    };

var result = markdownlint.sync(options),
    resultString = result.toString();

if (resultString.length > 0) {
    console.log(resultString);
    process.exit(1);
} else {
    console.log("Markdown Syntax OK");
    process.exit(0);
}
```

標準付属している[assertモジュール](https://nodejs.org/api/assert.html)を使うべきかと考えたが、上手くアサーションで表現する方法が思いつかなかった。よって、原始的なやり方だが終了コードで失敗させることにした。

## run-scriptとして実行可能にする

テストコードが完成したのでリポジトリルートに `package.json` を置いて、コミット時に自動実行されるようにする。

```json
{
  "scripts": {
      "lint": "node test/markdown.js",
      "precommit": "npm run lint",
      "test": "npm run lint"
  },
  "devDependencies": {
    "glob": "^5.0.5",
    "husky": "^0.7.0",
    "markdownlint": "0.0.4"
  }
}
```

## コミット時に失敗するか確認する

仕込んだテストがコミット時にきちんと機能するか確認してみる。

`blog/source/_posts/hello-my-post.md` ファイルを、わざと構文エラーが出るように編集する。

* 見出しの順序を小さいレベルから開始させる
* 4スペースインデントで設定したルールを2スペースで破らせる

```diff
 Hexo最初のpost
-==============
+--------------

 リストのテスト
---------------
+==============

 - A
+  - AAA
```

この状態で `git commit` を実行すると、コミットログの入力へは進めず、 `husky` によって中止できた。

```sh
$ git commit -a
blog/source/_posts/hello-my-post.md: 7: MD002 First header should be a h1 header
blog/source/_posts/hello-my-post.md: 14: MD007 Unordered list indentation
blog/source/_posts/hello-my-post.md: 16: MD007 Unordered list indentation

husky - pre-commit hook failed (add --no-verify to bypass)
```

Nodeのプロセスで構文チェックを実行しているだけだが、意外と時間のかかる印象を持った。

huskyのフックでテストさせるのは `"precommit"` ではなく `"prepush"` が良かったかも知れない。

## CIサービスを使って自動テストさせる

ここまで来ると[Travis CI](https://travis-ci.org/)や[CircleCI](https://circleci.com/)といったCI as a Serviceを利用して、リポジトリへのプッシュやPull Requestの時に自動でテストを走らせることが可能になる。

上記のサービスは2つとも、Nodeプロジェクトであれば暗黙的に `npm test` が実行させるので、走らせるテストコマンドを特別に明示させる必要は無く、実行環境だけを設定ファイルに書いておけば上手くテストしてくれた。

### Travis CI

`.travis.yml` という名前のファイルを置く。

```ymal
language: node_js
node_js:
  - "0.12"
  - "0.10"
  - "iojs"
```

### CircleCI

`circle.yml` という名前のファイルを置く。というか、このファイルを置かなくても、サービス連携した時点で自動的にNodeのプロジェクトだと認識して、良い感じに動いてくれた。

```yaml
machine:
  node:
    version: 0.10.22
```

## まとめ

* huskyかなり便利だと感じた
    * `npm install` のタイミングで `.git` の中にファイルを作ってくれるため、複数人開発で強制力のあるフックを実現できそう
* Markdown構文チェックもやってみると便利だった
    * そのまま使うとチェックルールが少し厳格な印象があるので、もう少しルールを細かく見てカスタマイズ設定した方が良さそうだった
