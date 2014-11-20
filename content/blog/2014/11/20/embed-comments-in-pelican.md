Title: PelicanにDisqusでコメント欄を埋め込む
Date: 2014-11-20 23:12:00
Modified:
Category: Python
Tags: Pelican, Python
Slug: embed-comments-in-pelican
Authors: raimon
Summary: Pelicanで構築したブログのコメント欄としてコメントサービスDisqusを埋め込む方法について。

Pelicanで構築したこのブログにコメント欄を埋め込む方法は無いものかとオンラインヘルプを確認したところ、[Settingsの頁](http://docs.getpelican.com/en/3.5.0/settings.html)で `DISQUS_SITENAME` というパラメータが紹介されていた。

> Pelican can handle Disqus comments. Specify the Disqus sitename identifier here.

これを使えばコメント機能が埋め込めそうだと分かり、早速設定した。

## Disqusでアカウントとコメントを埋め込むサイトを作成

まずDisqusでアカウントを作成する。

TwitterアカウントのOAuth経由で作成するボタンを押してみたが、これは単にTwitter連携機能が自動ONになるだけで、別にアカウント作成に必要な情報（メールアドレスやパスワード等）がスキップできる訳では無かった。

アカウントを作成したら、

1. [Add Disqus to your site](https://disqus.com/admin/create/)でサイト名（ブログ名）を入力する。
2. サイト名から自動で「your unique Disqus URL」の項目も埋まるので、ユニーク性に違反していなければ、そのままにする。
3. Categoryは「Tech」とした。
4. 作成したDisqus URLの `{myblog}.disqus.com` の **myblog** 部分を `pelicanconf.py` に設定する。

```python
SQUS_SITENAME = 'steeldragon14106'
```

この状態でローカルサーバに反映すれば、記事ごとの個別URLを開くと、コメント欄が埋め込まれた状態で確認できた。

```bash
$ fab rebuild
$ fab serve
```
