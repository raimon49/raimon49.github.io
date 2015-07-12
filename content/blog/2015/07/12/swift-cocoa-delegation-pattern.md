Title: SwiftでCocoa Delegation Patternに合わせたカスタムビューのProtocolを設計する
Date: 2015-07-12 12:43:22
Modified:
Category: iOS
Tags: Objective-C, Swift, iOS
Slug: swift-cocoa-delegation-pattern
Authors: raimon
Summary: カスタムビューを定義した時に通知するProtocolの設計をCocoa Delegation Patternに合わせる

## Delegateを通したカスタムビューとのやり取り

Objective-C/Swiftでは各オブジェクトの応答できるメソッドの約束事（他のプログラミング言語ではInterfaceと呼ばれるもの）としてProtocolを宣言する。

Protocolの中でもUIKitに含まれるようなビュークラスでは、Cocoa Delegation Patternと形容されるやり方が存在しており、自前でカスタムビューを作る時も、このパターンに合わせておくとユーザーコードも分かり易いものになる。

Swiftでこのやり方をする場合のコードを整理しておく。

## Objective-Cの場合

Objective-Cの場合は、定義したカスタムビューのヘッダファイル前方にDelegationの仕様を明示する事が一般的だと思う。

`@class` アノテーションを宣言する事で、コンパイルエラーとならずにカスタムビュー定義の前方にProtocolを書ける。

メソッドシグネチャの第1引数をカスタムビュー自身のオブジェクトにておくと、画面内で複数配置しているようなケースで、どのビューから応答が来たか判別できる。UIKitのクラスでは大抵こうなっている。

カスタムビュー側では `weak` 参照した状態で `MCVMyCustomViewDelegate` に適合するオブジェクトを保持する。

```objc
import <UIKit/UIKit.h>

@class MCVMyCustomView;

@protocol MCVMyCustomViewDelegate <NSObject>

@optional
- (void)myCustomViewDidLoad:(MCVMyCustomView *)myCustomView;
- (void)myCustomView:(MCVMyCustomView *)myCustomView didSelectAtViewNumber:(NSUInteger)viewNumber;

@end

@interface MCVMyCustomView : UIView

@property (weak, nonatomic) id <MCVMyCustomViewDelegate> delegate;

@end
```

`MCVMyCustomView.m` から応答する時は `respondsToSelector` で実装されているか確認した上でメッセージを送信する（クラッシュ対策）。

```objc
if ([self.delegate respondsToSelector:@selector(myCustomViewDidLoad:)]) {
    [self.delegate myCustomViewDidLoad:self];
}

if ([self.delegate respondsToSelector:@selector(myCustomView:didSelectAtViewNumber:)]) {
    [self.delegate myCustomView:self
          didSelectAtViewNumber:1];
}
```

## Swiftの場合

Swiftの場合もObjective-C同様のところに気を遣って設計すると、以下のようなコードになる。

Protocolで宣言したメソッドへの適合（実装）を任意としたい時は `@objc` 属性か `NSObject` の継承が必要になる。

カスタムビューでは、このProtocolをOptionalなweak参照のオブジェクトとして保持するのが妥当だと考えられる。


```swift
import UIKit

@objc protocol MyCustomViewDelegate: NSObject {
    optional func myCustomViewDidLoad(myCustomView: MyCustomView)
    optional func myCustomView(myCustomView: MyCustomView, didSelectAtViewNumber viewNumber: UInt)
}

class MyCustomView: UIView {
    weak var delegate: MyCustomViewDelegate?
}
```

応答コードはSwiftでは非常に短く書ける。

ただし、型としてのOptionalや実装任意のメソッド呼び出しを安全に取り出すため各所に `?` が登場し、やや読みにくい印象を受ける。

```swift
delegate?.myCustomViewDidLoad?(self)
delegate?.myCustomView?(self, didSelectAtViewNumber: 1)
```

## 参考情報

* [Using Swift with Cocoa and Objective-C: Adopting Cocoa Design Patterns](https://developer.apple.com/library/ios/documentation/Swift/Conceptual/BuildingCocoaApps/AdoptingCocoaDesignPatterns.html)
* [The Swift Programming Language: Protocols](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Protocols.html)
