Title: SwiftでHTTPS通信時に自己認証証明書の警告によるエラーを無視させる
Date: 2015-05-27 23:04:00
Modified:
Category: iOS
Tags: Objective-C, Swift, iOS
Slug: ignore-verify-self-signed-certificate
Authors: raimon
Summary: SwiftでNSURLRequestクラスのallowsAnyHTTPSCertificateForHostメソッドの書き換えを実現し、証明書の警告エラーを回避する

## NSURLConnectionにおけるkCFStreamErrorDomainSSLの発生

アプリ開発用途で自己認証証明書を使ったインターナルなAPIサーバを用意してHTTPS通信をする時、次のようなエラーが発生する。

```sh
NSURLConnection/CFURLConnection HTTP load failed (kCFStreamErrorDomainSSL, -9813)
```

このような場合、`NSURLRequest` クラスの非公開APIである `allowsAnyHTTPSCertificateForHost:` メソッドをオーバーライドすることで証明書の検証プロセスを回避できる。

## Objective-Cでのオーバーライド

Objective-Cの場合は `NSURLRequest` のカテゴリを定義し、該当のメソッドをオーバーライドすれば良い。

```objc
@implementation NSURLRequest(IgnoringCertificateError)

+ (BOOL)allowsAnyHTTPSCertificateForHost:(NSString *)host
{
    return YES;
}

@end
```

## Swiftでのオーバーライド

Swiftで同様のことができないか試してみたが、次のようにすると証明書の検証を回避できた。

ポイントとしては `extension` キーワードで既存クラスを拡張し、さらに `static` キーワードを付けてメソッドのシグニチャを揃えることでオーバーライドを実現する。

```swift
extension NSURLRequest {
    statuc func allowsAnyHTTPSCertificateForHost(host: String) -> Bool {
        return true
    }
}

```

## Releaseビルドには含めてはいけない

当然だが、非公開APIの挙動を書き換えているため、App Store提出時のReleaseビルドに含めてしまうと、Appleの審査フローいおいてリジェクトされるリスクがある。

また、万が一に審査を通ったとしても、アプリのユーザーを危険に晒すことになるため、この書き換えがReleaseビルドには含まれないようDebugビルドなどに限定しておくこと。
