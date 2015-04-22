Title: ibusからuim-mozcへ移行
Date: 2015-04-23 02:08
Category: Computer
Tags: uim, Mozc, Gentoo
Slug: uin-mozc

一時期 ibus が色々話題になりましたね [*1](http://cpplover.blogspot.jp/2013/10/ibus-15.html) [*2](http://www.kaoriya.net/blog/2013/10/18/)  
僕の環境では ibus-mozc を使っていたのですが、 1.5 系へは移行せず 1.4 系にとどまっていました  
このまま放置していてもよかったんだけれど、 Gentoo のリポジトリから 1.4 が  
なくなっていることに気がついたので別のインプットメソッドへ移行することにしました

Linux でのインプットメソッドで代表的なものは ibus 、 uim 、 fcitx といくつかあるけれど  
Mac で MacUIM を使っているので Linux のマシンでも uim を使うことにしました  
ただ Gentoo の公式リポジトリのパッケージでは mozc を uim と組み合わせることができないみたいだったので  
自分で ebuild を書くか、他の人が書いたものを使わせてもらうかのどちらかがあるみたいです  
今回は [wjn-overlay](https://bitbucket.org/wjn/wjn-overlay) を使わせてもらうことにしました

ここ [https://wiki.gentoo.org/wiki/Overlay/ja](https://wiki.gentoo.org/wiki/Overlay/ja) に書いてあるのですが crossdev を使っている場合は  
既に /usr/local/portage が存在するので移動しておくか別の場所を使う必要があるみたいです  
自分の場合は crossdev を使っているので既にディレクトリが存在しました  
なので別の場所へ移動しておきます

    :::bash
    # mv /usr/local/portage /usr/local/portage-crossdev
    # echo local-crossdev > /usr/local/portage-crossdev/profiles/repo_name
    # mkdir /usr/local/portage

wjn-overlay を /usr/local/portage/wjn-overlay に clone します

    :::bash
    # git clone https://bitbucket.org/wjn/wjn-overlay.git /usr/local/portage/wjn-overlay

最後に make.conf に登録すれば使えるようになります

    :::
    PORTDIR_OVERLAY="/usr/local/portage-crossdev /usr/local/portage/wjn-overlay"

equery で確認すると uim のフラグが使えるようになっているはずです

    :::bash
    $ equery u mozc
    [ Legend : U - final flag setting for installation]
    [        : I - package is installed with flag     ]
    [ Colors : set, unset                             ]
     * Found these USE flags for app-i18n/mozc-2.16.2068.102:
     U I
     - - emacs                    : Enable support for virtual/emacs
     - - fcitx                    : Enable support for app-i18n/fcitx
     - - ibus                     : Enable support for app-i18n/ibus
     + + python_targets_python2_7 : Build with Python 2.7
     + + qt4                      : Add support for the Qt GUI/Application Toolkit version 4.x
     - - renderer                 : Enable native candidate window
     - - test                     : Enable src_test phase for runtests
     + + uim                      : Enable support for app-i18n/uim

いつも通り emerge してインストール

    :::bash
    # emerge -av mozc

インストール後は [ここ](https://bitbucket.org/wjn/wjn-overlay/wiki/Mozc-ebuild-%E3%83%98%E3%83%AB%E3%83%97-%28JA%29) に書いてあるように  
ibus を終了してから XMODIFIERS 等をエクスポートして uim を起動すれば使えるようになるはず

    :::bash
    $ export XMODIFIERS="@im=uim"
    $ export GTK_IM_MODULE=uim
    $ export QT_IM_MODULE=uim
    $ uim-xim &
    $ uim-toolbar-gtk-systray &

その他にウインドウマネージャによってはシステムトレイのアイコンがおかしくなったりするので [ここ](https://archlinuxjp.kusakata.com/wiki/uim_%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%82%92%E5%85%A5%E5%8A%9B#uim-toolbar-gtk-systray:_.E3.83.88.E3.83.AC.E3.82.A4.E3.82.A2.E3.82.A4.E3.82.B3.E3.83.B3.E3.81.8C.E3.81.A4.E3.81.B6.E3.82.8C.E3.81.A6.E3.81.BE.E3.81.99) を参考に設定を変更する  
実際に変更した設定は

* `全体設定 → 入力方式の利用準備 → 標準の入力方式` を `Mozc` に
* `ツールバー → 入力方式切り替えメニュー` のチェックボックスを `オフ` に
* `ツールバー → ボタン` のチェックボックスを `全てオフ` に
* `ツールバー → 濃色背景向けアイコンを使用する` のチェックボックスを `オン` に
* `Mozc → ツールバー → 有効にするボタン` を `入力モード` のみに編集
* `Mozc → 特殊操作 → vi協調モードを有効にする` のチェックボックスを `オン` に
