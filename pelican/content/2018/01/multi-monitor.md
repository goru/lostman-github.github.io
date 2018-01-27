Title: Linuxで複数モニタを使うときのメモ
Date: 2018-01-25 01:14
Category: Computer
Tags: Gentoo, Linux
Slug: multi-monitor

以前買った [IGZO液晶](/posts/2015/12/akizuki-igzo.html) はたまにRaspberryPiを接続したり、
臨時のモニタとして活躍していました。ただ、最近活躍の機会もあまりないのと、
小画面で常時表示しておきたいような用途を思いついたのでデスクトップPCのサブモニタとしてしばらく使ってみることにしました。

デスクトップPCのマザーボードは [H77M-ITX](https://www.asrock.com/mb/Intel/H77M-ITX/index.jp.asp) を使っていて、
既存のモニタはDVI経由で接続しています。
このマザーボードはDVIとHDMI両方を使ってのマルチモニタに対応しているので、素直にHDMIに接続すれば物理的な準備は終わり。

ただ縦長の解像度が問題なのか、一般的なモニタを接続した場合も同じなのかはわからないけれど、
両方のモニタを接続しているとBIOSの画面が表示されなくなりました。
(キーを押すと入れはするけれど画面の表示がされない状態)
その為BIOSに入る必要がある時はIGZO液晶側の電源を切るかケーブルを抜いておく必要がありました。

次にLinux側の対応で、やりたいことは以下の3つ

- ミラーリングになっていたのでそれぞれ別に使えるようにする。
- 今まで使っていたモニタを今まで通りメインのモニタとして使う。
- IGZO液晶はポートレート表示がデフォルトなので回転させてランドスケープで使う。
- IGZO液晶はメインモニタの左側に配置する。

調べてみたら設定を変更するにはxrandrを使って動的に変更するかxorg.confに静的に書くかの2通りがありました。

その他にディスプレイマネージャにSLiMを使っていたのですが、
もう [開発が止まっているらしい](https://wiki.archlinux.org/index.php/SLiM) のとマルチモニタに対応していないみたいなので、
[LigntDM](https://www.freedesktop.org/wiki/Software/LightDM/) に置き換えました。
ウインドウマネージャは [Awesome](https://awesomewm.org/) でこちらは対応していて特に設定の必要なく使えました。

xrandrを使うにしろ、xorg.confに書くにしろ、まずLinux側にどのように認識されているか調べる必要があります。
単純にxrandrコマンドを実行すれば現在の状況が確認できました。

    :::
    $ xrandr
    Screen 0: minimum 8 x 8, current 3840 x 1200, maximum 32767 x 32767
    DP1 disconnected primary (normal left inverted right x axis y axis)
    DP2 disconnected (normal left inverted right x axis y axis)
    DP3 disconnected (normal left inverted right x axis y axis)
    HDMI1 connected 1920x1200+1920+0 (normal left inverted right x axis y axis) 550mm x 350mm
       1920x1200     59.95*+
       1920x1080     60.00
       1600x1200     60.00
       1680x1050     59.88
       1280x1024     75.02    60.02
       1440x900      59.90
       1280x960      60.00
       1152x864      75.00
       1024x768      75.08    70.07    60.00
       832x624       74.55
       800x600       72.19    75.00    60.32    56.25
       640x480       75.00    72.81    66.67    60.00
       720x400       70.08
    HDMI2 disconnected (normal left inverted right x axis y axis)
    HDMI3 connected 1920x1200+0+0 left (normal left inverted right x axis y axis) 90mm x 150mm
       1200x1920     60.00*+
    VGA1 disconnected (normal left inverted right x axis y axis)
    VIRTUAL1 disconnected (normal left inverted right x axis y axis)

手元の環境ではHDMI1にDVIのメインで使っているモニタ、HDMI3にIGZO液晶が接続されていると認識されていました。
xrandrのオプションやxorg.confでモニタを指定する時にこのHDMI1やHDMI3を使います。

まずxrandrで動作確認をしてからxorg.confに同じ設定を書き込むのがよさそうなのでそうしました。
manを見てみるとオプションを色々つけることで一度のコマンド実行で目的の設定に変更することができそうです。
ひとまずミラーリングになっていてメインの方も少しおかしな感じになっていたのでモニタをオフにするために以下を実行。

    :::
    xrandr --output HDMI3 --off

モニタの配置はHDMI1が正面、HDMI3が左側になっているのでこのようなコマンドを実行しました。
( `--noprimary` は指定しているけれど、どのように動作が変わるのかはよくわからない)

    :::
    xrandr --output HDMI3 --auto --left-of HDMI1 --rotate left --noprimary

これで期待通りの表示になることが確認できました。
毎回動的に変更したいのであれば単純にxrandrコマンドを.xinit等に書き込めばよさそうです。
自分はその必要はないのでxorg.confにこのように書き込みました。
再起動するかXを起動しなおして問題なければこれで終わりです。

    :::
    $ cat /etc/X11/xorg.conf.d/90xrandr.conf
    Section "Monitor"
        Identifier "HDMI1"
        Option     "Primary" "true"
    EndSection
    
    Section "Monitor"
        Identifier "HDMI3"
        Option     "LeftOf" "HDMI1"
        Option     "Rotate" "left"
    EndSection

更にメモ、放置すると一定時間でモニタがオフになるがそれを無効化する方法

    :::
    # 無効化
    xset s off -dpms
    # 有効化
    xset s default +dpms
