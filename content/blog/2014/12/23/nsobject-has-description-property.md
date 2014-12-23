Title: Xcode 6.xからNSObjectはdescriptionプロパティを持っている
Date: 2014-12-23 19:06:00
Modified:
Category: Xcode
Tags: Mac, Objective-C, Xcode
Slug: nsobject-has-description-property
Authors: raimon
Summary: Xcode 6.xではNSObject.hでdescriptionプロパティが宣言されており、全てのNSObjectを継承したオブジェクトがこのプロパティを持っている。

## descriptionメソッド

Objective-Cでクラスを宣言する場合、通常 `NSObject` を継承する。

この時に `description` メソッドをオーバーライドすることで、`NSLog()` などで自動的に評価され、オブジェクトの概要を表現することができる。

```objc
// MyClass.h
@interface MyClass : NSObject

@property (copy, nonatomic) NSString *name;

@end

// MyClass.m
@implementation MyClass

- (NSString *)description
{
    return [NSString stringWithFormat:@"this object name: %@", self.name];
}

@end

// Use MyClass
MyClass *klass = [MyClass new];
klass.name = @"my object";

// this object name: my object
NSLog(@"%@", klass);

```

## Xcode 6.xにおける実行時エラー

Xcode 6.xでは以下のように自分でクラスを宣言して `description` というプロパティを作って使うと、実行時エラーが発生じてクラッシュするようになった。

```objc
// MyClass.h
@interface MyClass : NSObject

@property (copy, nonatomic) NSString *name;
@property (copy, nonatomic) NSString *description;

@end

// Use MyClass
MyClass *klass = [MyClass new];
klass.name = @"my object";
klass.description = @"my description";
// -[MyClass setDescription:]: unrecognized selector sent to instance 0x7fc6eb465bb0
```

プロパティとして `description` という名前を宣言しただけでも警告が出る。

## Xcode 6.xにおけるNSObject.h

この理由は、継承元である `NSObject` のヘッダファイルを見ると分かる。

全てを載せると長くなるので、関係する箇所だけ抜粋する。この内容はVersion 6.1.1 (6A2008a)時点のヘッダファイルである。

```objc
@protocol NSObject

@property (readonly, copy) NSString *description;
@optional
@property (readonly, copy) NSString *debugDescription;

@end

@interface NSObject <NSObject> {
    Class isa  OBJC_ISA_AVAILABILITY;
}

@end

```

（ちょっとややこしいが） `NSObject` が適合している `NSObject` プロトコルにおいて `description` は `readonly` 属性のプロパティとして宣言されているため、自分が宣言したクラスの中で `description` を再定義して暗黙的に `readwrite` な属性とすることはできないと云うことになる。

モダンなObjective-Cを書いている人には自明だが、プロパティとして `description` 宣言した場合、暗黙的にインスタンス変数 `_description` が作成され、セッターとゲッターに相当する以下のメソッドが `@synthesize` で合成される。

```objc
- (void)setDescription:(NSString *)description
- (NSString *)description
```

この時、Xcode 6.xからは親クラス `NSObject` で `readonly` として定義された `description` に対応する `setDescription:` にメッセージを送ることは不可能で、もし送信すると実行時エラーが発生することになる。

元々 `description` メソッドの存在は開発者には知られており、予約語みたいなものだったため、その性格をより強調する意味で明示的にプロパティとして持つようになったのだと考えらえる。
