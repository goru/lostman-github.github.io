Title: MacUIM/Mozcを使う
Date: 2014-08-02 02:04
Category: Computer
Tags: Mac, MacUIM, Mozc
Slug: macuim-mozc

ターミナルは[rxvt-unicode](http://software.schmorp.de/pkg/rxvt-unicode.html)をビルドして使用しています  
これはX11のアプリなのでMacの標準のインプットメソッド経由では日本語を入力することができません  
今までほとんど困ることはなくて、必要なときはコピペで対応していました  
ただ最近ここをvimで書いていることもあり、[MacUIM](https://code.google.com/p/macuim/)をインストールして入力できるようにしました

1. まず上記サイトからダウンロードしてきたアーカイブをインストールします
1. 次に `System Preferences -> Language & Text -> Input Sources` で `MacUIM (Japanese)` のチェックを入れる
1. `System Preferences -> MacUIM` を開いて
    1. `General -> Input Method` で `Mozc` を選択
    1. `Helper -> Use Helper-Applet` をチェック (メニューバーに状態が表示される)
    1. `Uim -> Global settings -> Specify default IM` をチェック
    1. `Uim -> Global settings -> Default input method` で `Mozc` を選択
    1. 右下の `Apply` ボタンを押す
1. `~/.xinitrc.d/uim-xim.sh` に以下の内容で起動スクリプトを配置する  
このファイルを追加することでX11の起動時にUIMが起動する

        :::bash
        #!/bin/sh
        /Library/Frameworks/UIM.framework/Versions/Current/bin/uim-xim &


1. `~/.bashrc` にでも以下の環境変数を追加する  
X11でurxvtしか使わないのであればこれでOK  
他のアプリでも使用する場合は他からも見える位置で環境変数を定義する

        :::bash
        export XMODIFIERS="@im=uim"
        export GTK_IM_MODULE="uim"

1. urxvtの起動時に `-pt OffTheSpot` を追加する

とりあえずここまででデフォルトの `Shift+Space` を使用すれば日本語入力ができるようになっているはず  
ここからはおまけ  
Input sourceはMacUIM固定で `Cmd+Space` を日英の切り替えに使用したければ以下の設定をする

1. `System Preferences -> Language & Text -> Input Sources` を開いて
    1. `Input source shortcuts` にあるショートカットを無効にする
    1. `Input source options` は `Use the same one in all documents` を選択
1. `~/.uim.d/customs/custom-mozc-keys.scm` をエディタで開いて以下の部分を編集する

        :::
        (define mozc-on-key '("<Meta> "))
        (define mozc-on-key? (make-key-predicate '("<Meta> ")))
        (define mozc-off-key '("<Meta> "))
        (define mozc-off-key? (make-key-predicate '("<Meta> ")))

1. `System Preferences -> MacUIM` を開いて
    1. `Uim -> Global settings -> Enable input method toggle by hot key` のチェックを外す
    1. `Uim -> Mozc key bindings` の `on` と `off` が `<Meta>space` になっていることを確認
    1. 右下の `Apply` ボタンを押す

以上で `Cmd+Space` の入力でネイティブでもX11でも日本語入力の切り替えをすることができるようになりました
