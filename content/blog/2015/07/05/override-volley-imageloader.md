Title: VolleyライブラリNetworkImageViewのタイムアウト時間を長くする
Date: 2015-07-05 15:08:04
Category: Android
Tags: Android, Android Studio, Java
Slug: override-volley-imageloader
Authors: raimon
Summary: VolleyライブラリNetworkImageViewのタイムアウト時間がデフォルト2500ミリ秒に設定されているのを書き換える

Android Open Source Projectでメンテナンスされている[定番ネットワークライブラリVolley](https://android.googlesource.com/platform/frameworks/volley)には、`NetworkImageView` という、ネットワーク上の画像リソースを取得・表示してくれる `ImageView` の拡張が含まれている。

非常にお手軽で便利だが、デフォルトのタイムアウト時間が2500ミリ秒に設定されており、例えば本番環境よりも貧弱な開発環境でちょっとした画像を作って返すサーバと通信するようなケースでは、タイムアウトしてしまう事がある。

このようなケースでは `ImageLoader` を自前で定義したクラスと差し替える事で `NetworkImageView` に取得・表示する画像リソースへのリクエストタイムアウト時間を変更できる。

## 環境

* Volley 1.0.16
    * Gradleで入れたいため[mcxiaokeリポジトリにForkされている](https://github.com/mcxiaoke/android-volley) `1.0.16 2015.05.18` を使っている

## クラスの定義

ここでは `Activity` や `Fragment` の中にネストで定義している前提として書いているが、必要に応じて独立したクラスとして切り出すなどする。タイムアウト時間は10秒とした。

```java
private static class CustomImageLoader extends ImageLoader {
    private static final int CUSTOM_TIMEOUT_MS = 10000;
    public CustomImageLoader(RequestQueue queue, ImageCache imageCache) {
        super(queue, imageCache);
    }

    @Override
    protected Request<Bitmap> makeImageRequest(String requestUrl, int maxWidth, int maxHeight,
                                                ImageView.ScaleType scaleType, final String cacheKey) {
        Request<Bitmap> request = super.makeImageRequest(requestUrl, maxWidth, maxHeight, scaleType, cacheKey);
        request.setRetryPolicy(new DefaultRetryPolicy(
                    CUSTOM_TIMEOUT_MS,
                    DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

        return request;
    }
}
```

## クラスの利用

`NetworkImageView` を使う箇所で、上の `CustomImageLoader` と差し替えて使うと、任意のタイムアウト時間設定でアクセスできる。

```java
// ImageLoaderの生成
requestQueue = Volley.newRequestQueue(getApplicationContext());
imageLoader = new CustomImageLoader(requestQueue, imageCache);

// ImageLoaderの利用
networkImageView.setImageUrl(url, imageLoader);
```
