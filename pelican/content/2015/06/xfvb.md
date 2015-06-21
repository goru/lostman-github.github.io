Title: Xvfb上でChromeを動かしてみた
Date: 2015-06-14 00:35
Category: Computer
Tags: Linux, Gentoo
Slug: xvfb

外出中にFlashを使ったサイトをチェックしたいという要望が某所から出てきたので環境を作ってみた  
普段から PC を持ち歩いている人には必要ないことかもしれないけれど普通の人は持ち歩いていないよね  
私も荷物を持つのが嫌いなのでポケットに入るスマホと財布くらいしか持ち歩いていないです  
ということで、スマホで見れるといいけれど Android の Firefox で使える Flash はもうサポートが切れているのでいまいちな感じ  
で、自宅には常時起動のマシンがあるのでそこで何か用意できないかなと考えて今回 Xvfb を試してみた

Xvfb はなにかというと通常 X はクライアントからの要求を受けてドライバを経由して実際のモニタに描画するのに対し、  
モニタでなくメモリ上に確保した仮想のフレームバッファに画面を描画します  
このため画面がないマシンでも GUI のアプリケーションが起動できます  
サーバ上で GUI のアプリを動かすにはうってつけですね  
ただこのままだと外部から描画された画面を見ることができないので  
x11vnc を使って外部から画面の様子をVNCクライアントを使って見れるようにしました  
Chrome を選択したのは Flash を動かすのに追加でプラグインが必要ないためってだけ

必要なものをインストールする前に package.use に必要は USE フラグを追加して

    :::
    app-text/ghostscript-gpl cups
    media-fonts/ja-ipafonts X
    net-libs/libvncserver threads
    net-misc/tigervnc -opengl server
    x11-base/xorg-server minimal -xorg xvfb
    x11-libs/cairo X
    x11-libs/gdk-pixbuf X

以下をインストール

* media-fonts/ja-ipafonts
* www-client/google-chrome
* x11-base/xorg-server
* x11-misc/x11vnc
* x11-misc/xdotool

日本語のフォントが必要なので media-fonts/ja-ipafonts を入れているのと、
ウインドウの操作をコマンドから行うために x11-misc/xdotool もインストールしている

最終的なスクリプトはこんな感じになった

    :::bash
    #!/bin/sh -x
    
    export DISPLAY=:0
    
    WIDTH=1280
    HEIGHT=670
    PASSWORD=hoge
    #SCALE="" 
    SCALE="-scale 1/2" 
    #SCALE="-scale 3/4" 
    #SCALE="-scale 4/5" 
    
    Xvfb ${DISPLAY} -screen 0 ${WIDTH}x${HEIGHT}x16 &
    xvfb_pid=$!
    
    sleep 2
    
    LANG=ja_JP.utf8 google-chrome-stable --start-fullscreen "http://awesome.website.com" &
    (sleep 10; xdotool search --onlyvisible -name chrome windowmove 0 0; xdotool search --onlyvisible -name chrome windowsize ${WIDTH} ${HEIGHT}) &
    
    x11vnc -display ${DISPLAY} -forever ${SCALE} -passwd ${PASSWORD}
    
    xdotool search --onlyvisible -name chrome windowkill
    
    sleep 2
    
    kill $xvfb_pid

* Xvfb はスマホの画面で使用できる領域と同じにしておく (今回はステータスバーのサイズを考慮して 1280x670 だった
* Chrome のオプションは [このページ](http://chrome.half-moon.org/43.html) にまとまっている
    * `--start-fullscreen` のオプションを指定しても画面的にはフルスクリーンになるけれど  
    使用可能領域全体を使ってくれなかった、そのため xdotool を使った
* xdotool
    * Chrome のウインドウを探して左上へ移動、画面のサイズに合わせてウインドウのサイズを変更  
    x11vnc サーバが終了したら Chrome のウインドウも閉じる、という操作を担当
* x11vnc
    * クライアントが切断しても再接続できるように `-forever` を指定
    * 通信量を節約するために `-scale` も指定

以上でサーバ側の設定は終わり  
スマホから VNC でつなぐにはこのサーバへ外部から接続できるようになっている必要がある  
本当は VPN などを用意するのだろうけれど、今回は SSH のポートフォワードの機能を使った

Android 側は [ConnectBot](https://play.google.com/store/apps/details?id=org.connectbot&hl=ja) を使ってサーバへ接続する  
この際ローカルの 5900 をサーバの 5900 へフォワードするように設定しておく  
そして [VNC Viewer](https://play.google.com/store/apps/details?id=com.realvnc.viewer.android&hl=ja) でローカルの 5900 に接続する  
この VNC クライアントは自動で画面を端末のサイズに合わせて拡大するので  
-scale オプションを使用して 1/2 に縮小していても端末の画面いっぱいに描画してくれる (ただし画質は落ちる
