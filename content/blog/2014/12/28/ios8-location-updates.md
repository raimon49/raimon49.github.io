Title: iOS 8では「Appのバックグラウンド更新」がOFFでもバックグラウンドで位置情報の更新は通知される
Date: 2014-12-27 15:17:00
Modified:
Category: iOS
Tags: Objective-C, Xcode, iOS
Slug: ios8-location-updates
Authors: raimon
Summary: iOS 7とiOS 8ではバックグラウンドで位置情報取得する時の「Appのバックグラウンド更新」設定による影響が異なる。

## バックグラウンドでの位置情報取得

バックグラウンドに回されても位置情報を取得し続けるロガーアプリのような機能を実装したい場合、Xcodeの「Capabilities」-「Background modes」-「Location updates」にチェックを入れてアプリバイナリをビルドし、バッテリーをほとんど消費せずに済む[CLLocationManager](https://developer.apple.com/library/mac/documentation/CoreLocation/Reference/CLLocationManager_Class/index.html)クラスの `significantLocationChange` を監視し、帯電話基地局の切り替わりによる大規模な位置情報の更新を通知してもらう方法が定石である。

![Xcode設定画面](/images/xcode-location-updates-setting.png)

## 「Appのバックグラウンド更新」権限による影響

この時、iOS 7ではユーザーがアプリ毎に許可を与える「Appのバックグラウンド更新」という権限がONでなければ位置情報の更新が通知されなかった。iOS 7リリース当時のネットメディア記事などにも、この制限が書かれて残っている。参考：[「Appのバックグラウンド更新」はオフにしてもだいじょうぶ? - いまさら聞けないiPhoneのなぜ | マイナビニュース](http://news.mynavi.jp/articles/2013/11/23/iphone_why131/)

> 「Appのバックグラウンド更新」をオフにすると、バックグラウンドに回ったアプリは動作を禁止されます。たとえば、ランニングの経路を測るアプリの場合、他のアプリを起動してしまうとGPSログを取得できなくなります。電話の着信があったときなど、他のアプリを起動せざるをえない場面の多さを考えると、このスイッチをオフにすることの意味がわかると思います。

許可されているか否かは以下のプロパティから取得できる。

```objc
UIBackgroundRefreshStatus backgroundRefreshStatus = [UIApplication sharedApplication].backgroundRefreshStatus;
```

しかしながら、iOS 8からは、この設定がONでもOFFでも、大規模な位置情報の更新は通知されるようになった。

ただしiOS側から自動でスケジューリングしてバックグラウンド処理をさせてくれる「Background fetch」を使う場合は、iOS 7/8どちらの場合もこの設定がONであることが引き続き求められる。

ミニマムなコードで表現すると次のような感じになる。iOS 8以降、最初に位置情報を取得しようとする時に必要となった `kCLAuthorizationStatusAuthorizedAlways` をリクエストする処理に関しては今回の調査と関係無いため省略している。

```objc
@interface AppDelegate () <CLLocationManagerDelegate>

@property (nonatomic) CLLocationManager *locationManager;

@end

@implementation AppDelegate


- (BOOL)application:(UIApplication *)application
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // 大規模位置情報更新の監視を開始し、更新の通知を自身で受け取る
    self.locationManager = [CLLocationManager new];
    self.locationManager.delegate = self;
    [self.locationManager startMonitoringSignificantLocationChanges];

    // Background fetchの登録
    [application setMinimumBackgroundFetchInterval:UIApplicationBackgroundFetchIntervalMinimum];

    return YES;
}

#pragma mark - CLLocationManagerDelegate

- (void)locationManager:(CLLocationManager *)manager
     didUpdateLocations:(NSArray *)locations
{
    if (self.locationManager == manager) {
        // 大規模位置情報更新の通知
        // iOS 7ではコールバックされるには「Appのバックグラウンド更新」許可が必要
    }
}

#pragma mark - Background fetch

- (void)application:(UIApplication *)application
    performFetchWithCompletionHandler:(void (^)(UIBackgroundFetchResult))completionHandler
{
    // Background Fetchの発火
    // iOS 7/8どちらもコールバックされるには「Appのバックグラウンド更新」許可が必要

    UIBackgroundFetchResult fetchResult = UIBackgroundFetchResultNoData;
    if (/* some background code successed */) {
        fetchResult = UIBackgroundFetchResultNewData;
    }

    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(30 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        // 30秒以内に処理完了させる必要がある
        completionHandler(fetchResult);
    });
}
```

iOS 7からサポートされるようになったリモートプッシュの1つであるSilent notificationの到達についても、「Appのバックグラウンド更新」の影響を受けるかどうかがiOS 8とで変わったような感触があるのだけど、もう手元に検証用端末としてiOS 7.xのものが残っていないのでハッキリとは分からない。リモートプッシュは検証環境を作るだけで大変なので多分やらない。
