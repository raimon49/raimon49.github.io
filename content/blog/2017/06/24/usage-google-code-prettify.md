Title: Google code-prettifyの使い方（2017年6月現在）
Date: 2017-06-24 23:59:00
Category: JavaScript
Tags: JavaScript
Slug: usage-google-code-prettify
Authors: raimon
Summary: 2017年6月現在のGoogle code-prettifyをお手軽に導入する方法

Googleによって公開され、Google CodeからGitHubに移転し、現在も開発が続けられている[code-prettify](https://github.com/google/code-prettify)という構文ハイライトをCSS & JavaScriptで行ってくれるオープンソースライブラリがある。

個人的に同ライブラリの最新版へ追従する機会があり、日本語情報では廃れた方法が散見されたため、自分の理解を再整理する意味も込めて、2017年6月現在の導入方法をまとめておく。

## ライブラリのロードにはスクリプトローダーを使う

まず、ライブラリのロードにはCDNのURLを指定し、スクリプトローダーに任せてしまえば良い。

```html
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
```

この1行でCSSファイルも同時にロードされる。

ライブラリをダウンロードして自分のサーバに配置して読み込む利用方法は、もちろん現在も可能であるが、イントラネット上での利用などネットワークポリシーとして必要な場合のみ選択し、個人のブログやWikiに導入するのであればCDNから読み込んでしまう方が簡単である。

リクエストパラメータとして`skin`を与えると、[好みのデザインテーマ](https://cdn.rawgit.com/google/code-prettify/master/styles/index.html)に該当するCSSを読み込んでくれる。例えば以下のようにするとSunburstテーマが読み込まれる。

```html
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js?skin=sunburst"></script>
```

## 構文ハイライトさせたいpre要素を用意する

`class`属性に`prettyprint`を指定した`pre`要素や`code`要素を用意する。

```html
<pre class="prettyprint">
// 構文ハイライトさせたいコードスニペット
</pre>
```

この時`class`属性でハイライトさせるプログラミング言語のヒントを与えることもできる。ここ数年でRustやSwiftといった言語サポートも追加されているので[ソースコード](https://github.com/google/code-prettify/tree/master/src)を参考にすると良い。

```html
<pre class="prettyprint lang-js">
// 構文ハイライトさせたいJavaScriptコードスニペット
</pre>
```

## 構文ハイライトを実行する

以前は `prettyPrint` という関数名だったが最新の実装では `PR.prettyPrint` と名前空間オブジェクトが付与された。この関数を`body`要素の`onload`属性で呼ぶことで構文ハイライトが実行される。

```html
<body onload="PR.prettyPrint()">
```

利用しているブログツールやWikiツールといったCMSの制限によっては、HTMLテンプレートをカスタマイズすることが難しいケースも考えられるが、そのような場合はJavaScriptでまとめてやってしまうのが良いだろう。

例えば`id="main"`とされた要素直下の`pre`要素をすべて構文ハイライトさせたければ、スクリプトローダーでcode-prettifyを読み込んだ上で、次のようなJavaScriptコードを実行する。

```javascript
var initPrettyPrint = function() {
    Array.prototype.slice.call(document.querySelectorAll("#main > pre")).forEach(function(pre) {
        // メインとなる要素直下に存在する全てのpre要素にclass="prettyprint"を付与
        pre.setAttribute("class", "prettyprint");
    });

    // 構文ハイライトを実行
    PR.prettyPrint();
};

// 上記の初期化処理を画面ロード時に一度だけ呼ぶ
window.addEventListener("load", initPrettyPrint, false);
```

## 参考情報

* [Getting Started google/code-prettify](https://github.com/google/code-prettify/blob/master/docs/getting_started.md)
