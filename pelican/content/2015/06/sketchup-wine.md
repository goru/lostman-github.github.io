Title: SketchUpをWineで使う
Date: 2015-06-06 01:51
Category: Computer
Tags: Linux, Wine
Slug: sketchup-wine

SketchUp を Mac にインストールして使用していたのですが、 Mac のタッチパッドだといまいち操作性が良くありませんでした  
大画面でマウスを使って操作したかったのでデスクトップの Linux マシンにインストールしてみました  
SketchUp は Linux 版が提供されていないので Wine を使用することになります (公式の FAQ にもしれっと記述があった  
[WineHQ](https://www.winehq.org/) にも [SketchUpのWikiページ](http://wiki.winehq.org/Sketchup) があり情報がまとめられています  
ただ多少ハマった部分があったのでやったことを残しておく

まず [公式サイト](http://www.sketchup.com/ja/download) からインストーラを入手する  
自分がダウンロードしたのは `SketchUpMake-ja-x64.exe` だった  
インストール後にバージョンを確認したら `15.3.331 64ビット` となっていた

デフォルトの `Windows XP` だとバージョンチェックで起動できないので `winecfg` を起動して `Windows 7` へ変更する  
インストールするディレクトリを変えたい場合は `WINEPREFIX` 環境変数を使ってwine関係のコマンドを実行する  
(デフォルトでは `~/.wine` が使われる)

    :::bash
    $ WINEPREFIX=${HOME}/winedir/sketchup winecfg

次にインストーラを起動してインストールする  
Wine の USE フラグに `X abi_x86_64 fontconfig jpeg mono opengl png ssl truetype xcomposite` を追加しておいた  
インストーラの起動も winecfg と同様に WINEPREFIX を使って起動する

    :::bash
    $ WINEPREFIX=${HOME}/winedir/sketchup wine64 SketchUpMake-ja-x64.exe

これでインストーラが起動するはずだけれど手元の環境ではフォントのサイズが極端に大きくなっていて  
画面のレイアウトが操作できないレベルで崩れていた  
タブを4回、スペースを1回押すことでインストールを続行できた

インストールができて起動してみると `mfc100u.dll` が必要であるというエラーがでて起動できない  
mfc100u.dll は Visual C++ の再頒布可能パッケージに含まれているのでそれを入手する必要がある  
mfc100u.dll は [このサイト](http://www.wdic.org/w/TECH/Visual%20C%2B%2B%20%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA) によると [Visual C++ 2010](http://www.microsoft.com/ja-jp/download/details.aspx?id=14632) または [Visual Studio 2012](http://www.microsoft.com/ja-jp/download/details.aspx?id=30679) に含まれている  
今回は 2010 の方を使用した

Microsoft のサイトへ行くと `vcredist_x64.exe` を入手することができる  
このファイルを実行して展開する必要があるのだけれど、どうしても Wine を使ってはうまくできなかったので  
仕方なく Windows のマシンを使用して展開した  
Windows のコマンドプロンプトで `/x:c:\target\dir` のようにオプションを指定しすると  
指定したディレクトリへ中身を展開することができた

    :::
    > vcredist_x64.exe /x:c:\target\dir

展開したファイルの中に `vc_red.cab` というファイルがあるので  
それを更に展開すると `F_CENTRAL_mfc100u_x64` をいうファイルを入手することができる  
Linux で展開する場合は `cabextract` コマンドが利用できる  
`F_CENTRAL_mfc100u_x64` を Linux の環境へコピーしたら `system32` へ mfc100u.dll というファイル名でコピーする

    :::bash
    $ cp F_CENTRAL_mfc100u_x64 drive_c/windows/system32/mfc100u.dll

以上で基本的な作業は終了

これ以外の細かい設定は、 SketchUp を起動するには実行するユーザが `video` グループに所属していることと  
実行時のオプションに `/DisableRubyAPI` が必要だった

    :::
    libGL error: failed to open drm device: Permission denied
    
が起きる場合、実行するユーザがvideoグループに所属していない

    :::
    libGL error: unable to load driver: i965_dri.so

が起きる場合、 `media-libs/mesa` で `classic` USE フラグが有効になっていないので  
`/usr/lib/dri/i965_dri.so` が存在しない

    :::
    err:ntdll:RtlpWaitForCriticalSection section 0x2c8b8 "?" wait timed out in thread 0009, blocked by 0000, retrying (60 sec)
    
が起きる場合、コマンドラインオプションに /DisableRubyAPI をつけていない

最終的に以下のコマンドで正常に SketchUp を起動することができた

    :::bash
    $ WINEPREFIX=${HOME}/winedir/sketchup wine64 "${HOME}/winedir/sketchup/drive_c/Program Files (x86)/SketchUp/SketchUp 2015/SketchUp.exe" /DisableRubyAPI
