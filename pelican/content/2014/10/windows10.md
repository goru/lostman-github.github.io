Title: Windows10を試してみた
Date: 2014-10-06 01:45
Category: Computer
Tags: Linux, Gentoo, KVM, Windows
Slug: windows10

[Windows10 Technical Preview](http://windows.microsoft.com/ja-jp/windows/preview)がでたのでKVMにインストールしてみた  
このサイトにLinuxからアクセスすると「お使いのオペレーティング システムにはプレビュー版をインストールできません。」と  
表示されるがUserAgentをIEに変更してから再度アクセスしたらダウンロードすることができた

QEMUはひさしぶりなので使い方を忘れていたんだけれど以下のようにすることで特に問題なくインストールして動作させることができた

    :::bash
    $ qemu-img create -f qcow2 windows10.img 32G
    $ qemu-system-x86_64 -enable-kvm -cpu host -hda windows10.img -cdrom Windows10-en-x64.iso -boot d -m 4G

ただ電源の切り方がWindows8.1から更に変更されているので少し戸惑った

![Windows10 with KVM](/static/images/2014/10/windows10.jpg)
