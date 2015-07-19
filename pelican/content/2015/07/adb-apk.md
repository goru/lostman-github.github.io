Title: デバイスからAPKを抜き出す
Date: 2015-07-19 18:54
Category: Gadget
Tags: Android, SO-02G
Slug: adb-apk

[![image](/static/images/2015/07/so-02g_s.jpg)](/static/images/2015/07/so-02g.jpg)

SO-02Gのオレンジを買い増しました  
既に持っている白と同じアプリをインストールしようとしたのですが一部のアプリがストアから削除されていたので  
adb コマンドを使って apk を取り出してみました (色々便利なアプリがあるのは知ってる

インストールされているパッケージの一覧を表示  
全てのパッケージの apk のパスとパッケージ名が出力される  
(適当に grep して絞り込むといいと思う)

    :::bash
    $ adb shell pm list package -f

apk をデバイスからローカルへコピーする

    :::bash
    $ adb pull <device apk path>

インストール済みのパッケージを削除

    :::bash
    $ adb shell pm uninstall <package name>

ローカルの apk をデバイスへインストール

    :::bash
    $ adb install <local apk path>
