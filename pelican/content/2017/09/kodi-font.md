Title: Kodiのフォントを雑に変更する
Date: 2017-09-09 00:51
Category: Computer
Tags: Android, Kodi
Slug: kodi-font

[BRAVIA KJ-55X8500D](http://www.sony.jp/bravia/products/KJ-X8500D/) に [Kodi](https://play.google.com/store/apps/details?id=org.xbmc.kodi)
をインストールしているのですが、中華フォントが使われるので簡単にフォントを追加変更する方法がないか調べてみました。

現状では変更するUIはあるけれど、 `スキンのデフォルト` を使うか、 `Arialベース` の2択のみで、
パスを指定してフォントを追加したりといったことはできませんでした。
正攻法 ([HOW-TO:Add_a_new_true_type_font_to_the_skin](http://kodi.wiki/view/HOW-TO:Add_a_new_true_type_font_to_the_skin)) では
スキンを編集して使用可能なフォントを定義した上で、スキンのディレクトリにフォントを配置することになるみたいです。
しかしデフォルトのスキンはAndroidでは書き込み権限がある場所にないため、コピーするなりして新規に作る必要がありそうです。
それは面倒くさい。

KodiのWikiのフォントについてのページ ([Fonts](http://kodi.wiki/view/Fonts)) を確認したら、
フォントの読み込みは以下のようになっているらしく、スキンのディレクトリ以下にフォントがない場合は、
次に `XBMC/media/fonts` を見に行くようです。
(おそらく最終的にKodiのインストールされているディレクトリのフォントを見に行く。)

    :::
    There's one special file called font.xml. This file contains a list of all fonts the skin uses.
    XBMC will load all the fonts mentioned in this file from the /myskin/fonts directory first,
    and if that fails, will attempt to load them from XBMC/media/fonts.
    In the event that Kodi is unable to locate the specified font, it will default to "font13".
    You can modify this file as you like and add/delete/change fonts.
    The user friendly font name is referenced by the other xml files mentioned below.

`XBMC/media/fonts` とはどこかというと字幕のページ ([subtitles#Adding_fonts](http://kodi.wiki/view/subtitles#Adding_fonts))
にちょっとだけ出てきていました。
Userdataフォルダの1つ上が `Kodi(XMBC) folder` ということらしいです。

    :::
    Additional fonts can be stored in the Kodi folder (one level below userdata) at Kodi/media/Fonts/

で、Userdataフォルダがどこかというと、これについては専用のページ ([Userdata#Android_location](http://kodi.wiki/view/Userdata#Android_location))
があって、Androidであれば `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/` になるみたいです。
ということは、`/sdcard/Android/data/org.xbmc.kodi/files/.kodi/media/Fonts/` です。
ここなら書き込み権限があるので、任意のフォントを配置することができます。

AndroidではバージョンやデバイスによってSDカードのディレクトリが微妙に違うことがあります。
KJ-55X8500Dでの正確なパスは `/storage/sdcard0/Android/data/org.xbmc.kodi/files/.kodi/media/Fonts/` でした。

設定で `Arialベース` を選択するとKodiは `arial.ttf` を決められたフォルダを順に探すので、
上で調べたディレクトリにこのファイル名で配置しておけばOK。

AndroidTVはUSB経由でADBにつなぐことができないので、デバッグを有効にしたらWiFi経由で接続

    :::
    $ adb connect <IP Address>:5555

`fonts` フォルダがないので作成

    :::
    $ adb shell mkdir /storage/sdcard0/Android/data/org.xbmc.kodi/files/.kodi/media/fonts

任意のフォントを `arial.ttf` として保存

    :::
    $ adb push "/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc" /storage/sdcard0/Android/data/org.xbmc.kodi/files/.kodi/media/fonts/arial.ttf
    /System/Library/Fonts/ヒラギノ角ゴシック W5.ttc: 1 file pushed. 1.3 MB/s (7260984 bytes in 5.419s)

切断

    :::
    $ adb disconnect <IP Address>:5555

作業が終わったらデバッグを無効にしておく。
Kodiを再起動すると新しいフォントが使われるようになっているはず。
離れた場所から見るのに適したフォントがあるのかもしれないけれど、そのあたりの試行錯誤は後日。
