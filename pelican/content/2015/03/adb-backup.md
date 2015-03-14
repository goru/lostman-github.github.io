Title: adb backupのデータを展開する
Date: 2015-03-14 16:53
Category: Gadget
Tags: Android, HTL21, SO-02G
Slug: adb-backup

会社から支給されていた HTL21 の調子がわるくて、最近いつの間にか電源が落ちていたりするので  
Xperia Z3 Compact (SO-02G) に変えてもらいました  
アプリは手動でインストールし直して済むくらいしか入っていないのでそれでよかっんだけれど  
本体に入っている画像等のデータを簡単に抜き出す方法がよくわかりませんでした  
Android 4.0 以降からは `adb backup` が使えるのでそれでデータを抜き出せそうな気がして調べてみたところ  
`adb backup` でバックアップされる独自形式のデータを tar 形式に変換するツールが既にありました

* [Android Backup Extractor](http://sourceforge.jp/projects/sfnet_adbextractor/)

これを使えばバックアップしたデータのうち必要なものだけ抜き出せそう  
SD カードになにもかも保存してくれると移行が楽でいいんだけれどなぁ

    :::
    adb backup [-f <file>] [-apk|-noapk] [-obb|-noobb] [-shared|-noshared] [-all] [-system|-nosystem] [<packages...>]
                                 - write an archive of the device's data to <file>.
                                   If no -f option is supplied then the data is written
                                   to "backup.ab" in the current directory.
                                   (-apk|-noapk enable/disable backup of the .apks themselves
                                      in the archive; the default is noapk.)
                                   (-obb|-noobb enable/disable backup of any installed apk expansion
                                      (aka .obb) files associated with each application; the default
                                      is noobb.)
                                   (-shared|-noshared enable/disable backup of the device's
                                      shared storage / SD card contents; the default is noshared.)
                                   (-all means to back up all installed applications)
                                   (-system|-nosystem toggles whether -all automatically includes
                                      system applications; the default is to include system apps)
                                   (<packages...> is the list of applications to be backed up.  If
                                      the -all or -shared flags are passed, then the package
                                      list is optional.  Applications explicitly given on the
                                      command line will be included even if -nosystem would
                                      ordinarily cause them to be omitted.)

`adb backup` の説明はこんな感じなので、アプリのバックアップが必要なければ `-shared` だけ指定すればよさそう  
`-shared` を付けて実行すると SD カードの中身までバックアップしようとするので実行前に外しておくこと  
実行するとコンソールにこのようなメッセージが出力されるので端末の画面を確認する

    :::bash
    $ adb backup -f backup.ab -shared
    Now unlock your device and confirm the backup operation.

[![dialog](/static/images/2015/03/Screenshot_2015-03-15-02-27-34_s.png)](/static/images/2015/03/Screenshot_2015-03-15-02-27-34.png)

端末側にこのようなダイアログが表示されるので、パスワードの入力をせずに `データのバックアップ` をタップする  
バックアップの処理中は特にプログレスが表示されるわけではないのでそのまま放置する  
処理が終了するとしれっとプロンプトが戻ってきているはず

これでデータの吸い出しは終わったので変換して展開すれば取り出すことができる  
[Android Backup Extractor](http://sourceforge.jp/projects/sfnet_adbextractor/) のサイトから `abe.jar` をダウンロードする

    :::
    unpack: java -jar abe.jar unpack <backup.ab> <backup.tar> [password]

README を読むと展開をするにはこのようなコマンドを実行すればいいみたいなのでそのとおりに実行する

    :::bash
    $ java -jar abe.jar unpack backup.ab backup.tar
    Strong AES encryption not allowed
    Magic: ANDROID BACKUP
    Version: 1
    Compressed: 1
    Algorithm: none
    1710935552 bytes written to backup.tar.

これで一般的な tar 形式に変換されたので展開して中身を取り出すことができた  
今回は取り出した中身を SD カードにコピーして新しい端末で使用することにした

参考
* [adb backup で Android 端末のバックアップを作成する(3)](http://port139.hatenablog.com/entry/2014/07/17/065152)
