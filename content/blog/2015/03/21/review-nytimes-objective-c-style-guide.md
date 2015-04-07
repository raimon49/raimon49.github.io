Title: iOSアプリのコーディング規約を考える時はGoogleよりもNYTimesのObjective-Cスタイルガイドを参考にすべき
Date: 2015-03-21 19:36:00
Modified:
Category: iOS
Tags: iOS, Objective-C, Xcode
Slug: review-nytimes-objective-c-style-guide
Authors: raimon
Summary: GitHubで公開されているNYTimesのNYTimesスタイルガイドについて参考になる点、自分とは少し考え方が異なる点を覚え書き。

## Googleのスタイルガイドは古い

複数人でiOSアプリをObjective-Cコードで書いて保守する時、コーディング規約を検討することになる。

参考にすべきスタイルガイドとして良く挙がるものに[Google Objective-C Style Guide](http://google-styleguide.googlecode.com/svn/trunk/objcguide.xml)があるが、これはいかんせん古い。メモリ管理ARCやNSNumberのリテラル構文など、比較的新しいトピックについても追記されてはいるが、

* インスタンス変数のアクセス修飾子
    * プロパティを使う事が主流となっている2015年現在、余り扱われない
* `autorelease` を使ったオブジェクト生成など、MRC時代の規約
* 何よりホスティング先が[サービス終了を発表されたGoogle Code](http://google-opensource.blogspot.jp/2015/03/farewell-to-google-code.html)であり、永続的な参照先として頼りない
    * そのうちGitHubに移るのだとは考えられる

などなど、うっかりGoogleのスタイルガイドを参考にすると「旧時代のObjective-C」スタイルにどっぷり浸かる地雷を踏みかねない。

## 参考にすべきはNYTimesのスタイルガイド

では何を参考にするのが良いかと考えると、[NYTimes/objective-c-style-guide](https://github.com/NYTimes/objective-c-style-guide)にホスティングされているNYTimesのスタイルガイドが良い。

第三者からのPull Requestでメンテナンスされているため透明性が高く、何よりも内容がモダンである。

iOSアプリの新規コードは徐々にSwiftに移って行くものと考えられるが、Objective-Cコードの保守も続くので、NYTimesのガイドを引用しつつ自分の考え方も整理してみたい。

なお、ここで引用したスタイルガイドはコミット[1265ed97ba85df89f36fb664cbecde1042fc1988](https://github.com/NYTimes/objective-c-style-guide/tree/1265ed97ba85df89f36fb664cbecde1042fc1988)時点の内容とする。

## Dot-Notation Syntax

> Dot-notation should **always** be used for accessing and mutating properties. Bracket notation is preferred in all other instances.

**For example:**
```objc
view.backgroundColor = [UIColor orangeColor];
[UTIApplication sharedApplication].delegate;
```

**Not:**
```objc
[view setBackgroundColor:[UIColor orangeColor]];
UIApplication.sharedApplication.delegate;
```

引数なしのメソッドはドット記法でも呼び出せるが、メソッドの呼び出しであればそうだと判別できるよう常にブラケット `[]` で囲うべきだとする。

他のプログラミング言語に慣れている人は後者の書き方を好んだりもするが、「保守し易いObjective-Cコード」を考える時、妥当なルール。

またsetterメソッドでなくドット記法のプロパティアクセスを使っている点も大事。Stack Overflowなどで拾ったコードをコピペしていると、この辺りの記述は一貫性が失われがちである。

## Spacing

> * Indent using 4 spaces. Never indent with tabs. Be sure to set this preference in Xcode.
> * Method braces and other braces (`if`/`else`/`switch`/`while` etc.) always open on the same line as the statement but close on a new line.

タブコードを使わず4 spacesによるインデントはXcode標準設定であり、妥当。

なおGoogleのスタイルガイドは2 spacesを、GitHubのスタイルガイドはタブコードを採用している。Objective-Cはコードが横に長くなりがちなため、狭くしたい心情は理解できる。

## Conditionals

> Conditional bodies should always use braces even when a conditional body could be written without braces (e.g., it is one line only) to prevent [errors](https://github.com/NYTimes/objective-c-style-guide/issues/26#issuecomment-22074256). These errors include adding a second line and expecting it to be part of the if-statement. Another, [even more dangerous defect](http://programmers.stackexchange.com/a/16530) may happen where the line "inside" the if-statement is commented out, and the next line unwittingly becomes part of the if-statement. In addition, this style is more consistent with all other conditionals, and therefore more easily scannable.

**For example:**
```objc
if (!error) {
    return success;
}
```

**Not:**
```objc
if (!error)
    return success;
```

or

```objc
if (!error) return success;
```

if文の条件に合致する処理は1行で書ける内容であっても、常にブレース `{}` で囲って改行させる。『リーダブルコード』などでもお馴染みのトピックであり、きわめて妥当。

## Ternary Operator

> The Ternary operator, ? , should only be used when it increases clarity or code neatness. A single condition is usually all that should be evaluated. Evaluating multiple conditions is usually more understandable as an if statement, or refactored into instance variables.

**For example:**
```objc
result = a > b ? x : y;
```

**Not:**
```objc
result = a > b ? x = c > d ? c : d : y;
```

三項演算子の入れ子をさせないというもの。

個人的には括弧 `()` で優先順を明示すれば、複数の入れ子もやって良いと考えるが、普通は1つに留めておくのが妥当だろう。

## Error handling

> When methods return an error parameter by reference, switch on the returned value, not the error variable.

**For example:**
```objc
NSError *error;
if (![self trySomethingWithError:&error]) {
    // Handle Error
}
```

**Not:**
```objc
NSError *error;
[self trySomethingWithError:&error];
if (error) {
    // Handle Error
}
```

このルールはちょっと良く分からないところ。

`NSError` 変数にエラー情報を書き込んで非 `nil` である事からハンドリングできれば良いし、さらにBOOLで返すのは、やや冗長な印象を受ける。

## Methods

> In method signatures, there should be a space after the scope (-/+ symbol). There should be a space between the method segments.

**For Example**:
```objc
- (void)setExampleText:(NSString *)text image:(UIImage *)image;
```

-/+シンボルの後ろにスペースを入れる。妥当。

## Variables

> Variables should be named as descriptively as possible. Single letter variable names should be avoided except in `for()` loops.
>
> Asterisks indicating pointers belong with the variable, e.g., `NSString *text` not `NSString* text` or `NSString * text`, except in the case of constants.
>
> Property definitions should be used in place of naked instance variables whenever possible. Direct instance variable access should be avoided except in initializer methods (`init`, `initWithCoder:`, etc…), `dealloc` methods and within custom setters and getters. For more information on using Accessor Methods in Initializer Methods and dealloc, see [here](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW6).

**For example:**

```objc
@interface NYTSection: NSObject

@property (nonatomic) NSString *headline;

@end
```

**Not:**

```objc
@interface NYTSection : NSObject {
    NSString *headline;
}
```

ポインタ型のアスタリスクを型と変数のどちらに寄せるかは良く議論の対象になるが、自分もNYTimesのスタイルガイドと同じく変数側に寄せる方法を支持したい。

Googleのスタイルガイドについて「古い」と指摘した通り、インスタンス変数の宣言ではなくプロパティの宣言を使うべきとしている点も含め、モダンで妥当なルール。

## Naming

> Apple naming conventions should be adhered to wherever possible, especially those related to [memory management rules](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html) ([NARC](http://stackoverflow.com/a/2865194/340508)).
>
> Long, descriptive method and variable names are good.

**For example:**

```objc
UIButton *settingsButton;
```

**Not**

```objc
UIButton *setBut;
```

単語を省略させるのは駄目だというルール。妥当。

> A three letter prefix (e.g. `NYT`) should always be used for class names and constants, however may be omitted for Core Data entity names. Constants should be camel-case with all words capitalized and prefixed by the related class name for clarity.


```objc
static const NSTimeInterval NYTArticleViewControllerNavigationFadeAnimationDuration = 0.3;
```

**Not:**

```objc
static const NSTimeInterval fadetime = 1.7;
```

Objective-Cには言語機構として名前空間が存在しないため、クラス名および定数名にはプレフィックスを付与しようというもの。例えばNYTimesの作ったクラス名であれば、そこから取った `NYT` と3文字を付与する。これは2文字のプレフィックスがAppleのフレームワーク用に予約済みであるため、妥当。 2文字のプレフィックスについて[補足の追記をPRで投げたところ、マージしてくれた](https://github.com/NYTimes/objective-c-style-guide/pull/99)。

> Properties and local variables should be camel-case with the leading word being lowercase.
>
> Instance variables should be camel-case with the leading word being lowercase, and should be prefixed with an underscore. This is consistent with instance variables synthesized automatically by LLVM. **If LLVM can synthesize the variable automatically, then let it.**

プロパティとローカル変数は小文字から始まるキャメルケースを用いる、またObjective-Cにはプロパティ宣言とインスタンス変数を合成するための `@synthesize` があるが、現在は自動でアンダースコアを付けて合成してくれるため、省略しておけば良いとしている。これも妥当だと思う。

```objc
// こう宣言したものは
@property (nonatomic, copy) NSString *myVariable;

- (instancetype)init
{
    self = [super init];
    if (self) {
        // この名前でインスタンス変数にアクセス可能
        _myVariable
    }

    return self;
}
```

## Comments

> When they are needed, comments should be used to explain **why** a particular piece of code does something. Any comments that are used must be kept up-to-date or deleted.
>
> Block comments should generally be avoided, as code should be as self-documenting as possible, with only the need for intermittent, few-line explanations. This does not apply to those comments used to generate documentation.

「hogeオブジェクトを生成」「foo変数に代入」など、何やってるか一目瞭然で情報量ゼロのコメントは入れるなという話で、これも妥当。

ブロックコメントをドキュメンテーション生成用のものには使って良いというルールについて補足をすると、Xcode 5からサポートされたJavadocライクな構文のことを指していると思われる。

```objc
/**
Check whether a file at a given URL has a newer timestamp than a given file.
Example usage:
@code
NSURL *url1, *url2;
BOOL isNewer = [FileUtils
         isThisFileNewerThanThatFile:url1 thatURL:url2];
@endcode
@see http://www.dadabeatnik.com for more information.
@param thisURL
        The URL of the source file.
@param thatURL
        The URL of the target file to check.
@return YES if the timestamp of @c thatURL is newer than the timestamp of @c thisURL,
         otherwise NO.
*/
+ (BOOL)isThisFileNewerThanThatFile:(NSURL *)thisURL thatURL:(NSURL *)thatURL;
```

なおSwiftでは、このようなドキュメンテーション生成用のブロックコメントはreStで表現できるようになっている。

参考情報を載せておく。

* [Documenting your code with comments in Xcode 5 | dada beatnik](http://blog.dadabeatnik.com/2013/09/25/comment-docs-in-xcode-5/)
* [Swift Documentation - NSHipster](http://nshipster.com/swift-documentation/)

## init and dealloc

> `dealloc` methods should be placed at the top of the implementation, directly after the `@synthesize` and `@dynamic` statements. `init` should be placed directly below the `dealloc` methods of any class.
>
> `init` methods should be structured like this:

```objc
- (instancetype)init {
    self = [super init]; // or call the designated initializer
    if (self) {
        // Custom initialization
    }

    return self;
}
```

イニシャライザ `init` では、継承元のクラスが `self` を生成して返せた場合のみ、自分で定義したカスタムクラス用の初期化を行うべきとするルール。Appleのガイドなどでも謳われており、妥当。

`dealloc` をimplementationの先頭で宣言しておくという点は今まで余り意識していなかった。

## Literals

> `NSString`, `NSDictionary`, `NSArray`, and `NSNumber` literals should be used whenever creating immutable instances of those objects. Pay special care that `nil` values not be passed into `NSArray` and `NSDictionary` literals, as this will cause a crash.

**For example:**

```objc
NSArray *names = @[@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul"];
NSDictionary *productManagers = @{@"iPhone" : @"Kate", @"iPad" : @"Kamal", @"Mobile Web" : @"Bill"};
NSNumber *shouldUseLiterals = @YES;
NSNumber *buildingZIPCode = @10018;
```

**Not:**

```objc
NSArray *names = [NSArray arrayWithObjects:@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul", nil];
NSDictionary *productManagers = [NSDictionary dictionaryWithObjectsAndKeys: @"Kate", @"iPhone", @"Kamal", @"iPad", @"Bill", @"Mobile Web", nil];
NSNumber *shouldUseLiterals = [NSNumber numberWithBool:YES];
NSNumber *buildingZIPCode = [NSNumber numberWithInteger:10018];
```

配列オブジェクトや辞書オブジェクトもリテラル構文で変数に代入した方がスッキリ見易いため、これも妥当である。Mutableな変数を作る場合もこれを使うと簡単になるのでオススメだ。

```objc
// リテラル構文で宣言したNSArrayオブジェクトにmutableCopyメッセージを送る
NSMutableArray *mutableNames = [@[@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul"] mutableCopy];

// なおnilを追加することは出来ないので、NSNullを使う
[mutableNames addObject:[NSNull null]];
```

## CGRect Functions

> When accessing the `x`, `y`, `width`, or `height` of a `CGRect`, always use the [`CGGeometry` functions](http://developer.apple.com/library/ios/#documentation/graphicsimaging/reference/CGGeometry/Reference/reference.html) instead of direct struct member access. From Apple's `CGGeometry` reference:
>
> > All functions described in this reference that take CGRect data structures as inputs implicitly standardize those rectangles before calculating their results. For this reason, your applications should avoid directly reading and writing the data stored in the CGRect data structure. Instead, use the functions described here to manipulate rectangles and to retrieve their characteristics.

```objc
CGRect frame = self.view.frame;

CGFloat x = CGRectGetMinX(frame);
CGFloat y = CGRectGetMinY(frame);
CGFloat width = CGRectGetWidth(frame);
CGFloat height = CGRectGetHeight(frame);
```

**Not:**

```objc
CGRect frame = self.view.frame;

CGFloat x = frame.origin.x;
CGFloat y = frame.origin.y;
CGFloat width = frame.size.width;
CGFloat height = frame.size.height;
```

CGRect構造体から座標やサイズを取り出すのに「CGRectXXXX」で定義されている関数を使うと良いとするルール。

ここもNYTimesのスタイルガイドを読むまで余り意識していなかったので気を付けたい。

## Constants

> Constants are preferred over in-line string literals or numbers, as they allow for easy reproduction of commonly used variables and can be quickly changed without the need for find and replace. Constants should be declared as `static` constants and not `#define`s unless explicitly being used as a macro.

**For example:**

```objc
static NSString * const NYTAboutViewControllerCompanyName = @"The New York Times Company";

static const CGFloat NYTImageThumbnailHeight = 50.0;
```

**Not:**

```objc
#define CompanyName @"The New York Times Company"

#define thumbnailHeight 2
```

文字列定数であればNSStringのポインタに対して `const` を付けて宣言する。これは自分も慣れるまでは後ろのfloatのようなスカラ値定数との間で良く混乱した。

また定数名には先述のプレフィックスを付与し、上書きされてしまうdefineマクロを使わないとするルールも妥当である。

## Enumerated Types

> When using `enum`s, it is recommended to use the new fixed underlying type specification because it has stronger type checking and code completion. The SDK now includes a macro to facilitate and encourage use of fixed underlying types ? `NS_ENUM()`

```objc
typedef NS_ENUM(NSInteger, NYTAdRequestState) {
    NYTAdRequestStateInactive,
    NYTAdRequestStateLoading
};
```

`NS_ENUM()` マクロで宣言しておくとswitch～caseの中でチェックしてくれるので使った方が良い。妥当。

## Bitmasks

> When working with bitmasks, use the `NS_OPTIONS` macro.

**Example:**

```objc
typedef NS_OPTIONS(NSUInteger, NYTAdCategory) {
  NYTAdCategoryAutos      = 1 << 0,
  NYTAdCategoryJobs       = 1 << 1,
  NYTAdCategoryRealState  = 1 << 2,
  NYTAdCategoryTechnology = 1 << 3
};
```

ビットマスクの定数は `NS_OPTIONS()` マクロで宣言する。妥当。

## Private Properties

> Private properties should be declared in class extensions (anonymous categories) in the implementation file of a class. Named categories (such as `NYTPrivate` or `private`) should never be used unless extending another class.

```objc
@interface NYTAdvertisement ()

@property (nonatomic, strong) GADBannerView *googleAdView;
@property (nonatomic, strong) ADBannerView *iAdView;
@property (nonatomic, strong) UIWebView *adXWebView;

@end
```

ここで言う「Private」は、「ヘッダファイルでクラス外部に公開する必要がない」という意味になる。

Privateなプロパティは実装ファイル「MyClass.m」側でクラスエクステンションとして宣言することで、自クラス内からのみ使うプロパティという扱いにできる。妥当。

## Image Naming

> Image names should be named consistently to preserve organization and developer sanity. They should be named as one camel case string with a description of their purpose, followed by the un-prefixed name of the class or property they are customizing (if there is one), followed by a further description of color and/or placement, and finally their state.

**For example:**

* `RefreshBarButtonItem` / `RefreshBarButtonItem@2x` and `RefreshBarButtonItemSelected` / `RefreshBarButtonItemSelected@2x`
* `ArticleNavigationBarWhite` / `ArticleNavigationBarWhite@2x` and `ArticleNavigationBarBlackSelected` / `ArticleNavigationBarBlackSelected@2x`.

画像ファイル名にもビュークラス名を入れるというルールの発想は無かった……。

## Booleans

> Since `nil` resolves to `NO` it is unnecessary to compare it in conditions. Never compare something directly to `YES`, because `YES` is defined to 1 and a `BOOL` can be up to 8 bits.
>
> This allows for more consistency across files and greater visual clarity.

```objc
if (!someObject) {
}
```

**Not:**

```objc
if (someObject == nil) {
}
```

`nil` は元々falsyに評価されるため、わざわざ比較しなくて良いという話。たしかに。

-----

**For a `BOOL`, here are two examples:**

```objc
if (isAwesome)
if (![someObject boolValue])
```

**Not:**

```objc
if (isAwesome == YES) // Never do this.
if ([someObject boolValue] == NO)
```

同様に、YES/NOとの比較も冗長であるとするルール。妥当。

> If the name of a `BOOL` property is expressed as an adjective, the property can omit the “is” prefix but specifies the conventional name for the get accessor, for example:

```objc
@property (assign, getter=isEditable) BOOL editable;
```

形容詞を採用するBOOL型のプロパティでは「is」プレフィックスを省略可能だが、その場合はゲッターメソッドに「is」を付与しておこうとするもの。好ましいルールだと思う。

## Singletons

> Singleton objects should use a thread-safe pattern for creating their shared instance.

```objc
+ (instancetype)sharedInstance {
    static id sharedInstance = nil;

    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });

    return sharedInstance;
}
```

Objective-CにおけるスレッドセーフなSingletonオブジェクトの生成コード。もはや定型句なので、テンプレートとしてXcodeに突っ込んでおくのが良い。

参考にすべき日本語資料として[Objective-CのSingleton、その歴史的経緯など](http://www.toyship.org/archives/1770)というエントリが挙げられる。

## Imports

> If there is more than one import statement, group the statements [together](http://ashfurrow.com/blog/structuring-modern-objective-c). Commenting each group is optional.
>
> Note: For modules use the [@import](http://clang.llvm.org/docs/Modules.html#using-modules) syntax.

```objc
// Frameworks
@import QuartzCore;

// Models
#import "NYTUser.h"

// Views
#import "NYTButton.h"
#import "NYTUserView.h"
```

importするファイルごとにグルーピングをせよというルール。

余り意識していなかったが、外部Frameworkを先頭にしておくのは妥当だろう。

## Xcode project

> The physical files should be kept in sync with the Xcode project files in order to avoid file sprawl. Any Xcode groups created should be reflected by folders in the filesystem. Code should be grouped not only by type, but also by feature for greater clarity.
>
> When possible, always turn on "Treat Warnings as Errors" in the target's Build Settings and enable as many [additional warnings](http://boredzo.org/blog/archives/2009-11-07/warnings) as possible. If you need to ignore a specific warning, use [Clang's pragma feature](http://clang.llvm.org/docs/UsersManual.html#controlling-diagnostics-via-pragmas).

Xcodeのプロジェクトエクスプローラにおけるグループと、ファイルシステム上のディレクトリツリーを動機しておくべきとするルール。

確かにXcodeのグループ機能は好き勝手に分けてしまえるので、リポジトリなどのツリーも揃えておく方が好ましい。

## まとめ

2015年3月現在、GoogleのスタイルガイドよりもNYTimesのスタイルガイドの方がモダンObjective-Cの流れに沿っていると言えるため、コーディング規約を考える時は後者を参考にするべき。
