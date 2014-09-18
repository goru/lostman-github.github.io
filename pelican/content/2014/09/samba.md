Title: 今更Sambaをインストールした
Date: 2014-09-01 13:42
Category: Computer
Tags: Samba, Linux, Gentoo, Windows, Mac
Slug: samba

しばらく前に[ASUS VivoTab Note 8](http://www.asus.com/jp/Tablets_Mobile/ASUS_VivoTab_Note_8_M80TA/)を買ったり、[HP Pavilion 15-n200 (AMD)](http://h50146.www5.hp.com/directplus/personal/notebooks/dp_pavilion15_n200_amd/)が29800円だったので妻に買ったりMacBook Airもあるし  
Linux以外のマシンが増えてきたので、これらのマシンからもファイルサーバを利用できるようにSambaの導入をしました  
今までは自分のLinuxマシンだけだったんでNFSで間に合ってたんだけどね

Gentooでのインストールは特に気にすることなくいつも通り  
自分はクライアントの機能は不要だったので `-client` と `-smbclient` を指定した  
デフォルトの設定ファイルをコピーして自分の設定を作っていく

    :::bash
    # emerge -av samba
    # cp /etc/samba/smb.conf.default /etc/samba/smb.conf

以下に変更した設定をメモしておく

* workgroup = WORKGROUP  
Windowsのデフォルトに合わせる
* hosts allow = 10.0.0.  
hosts deny = all  
LAN内のマシン以外からのアクセスを拒否する
* load printers = no  
プリンタはいらない
* interfaces = br0  
bind interfaces only = yes  
LAN側のNICでのみ待ち受ける
* max protocol = smb2  
全てWindows8.1なので新しいプロトコルが使える
* map to guest = Bad User  
ログインに失敗した場合はGuestユーザとして扱う  
共有ディレクトリの設定の部分で `public = yes` と設定するとアクセス可能になる

共有ディレクトリの設定はこのようにした  
元々あった `homes` と `printers` は不要なのでコメントアウトして  
新たにSamba用のディレクトリ以下を公開することにした

    :::
    [Home]
       comment = Home Directories
       path = /mnt/lvm/samba/%u
       writable = yes
       printable = no
    
    [Public]
       comment = Public
       path = /mnt/lvm/samba/Public
       public = yes
       writable = yes
       printable = no

共有ディレクトリにアクセスできるユーザを作るにはまずLinuxのユーザを作成しなければいけない  
その後、既存のLinuxのユーザをSambaへ登録する操作が必要になる

    :::bash
    # useradd sambauser
    # pdbedit -a -u sambauser

なおSamba側に登録されているユーザの一覧は `pdbedit -L -v` で確認できる

以上で設定は終了  
`testparm` コマンドを実行すると設定の確認ができる  
最後にサービスへの登録と起動をする

    :::bash
    # rc-update add samba default
    # /etc/init.d/samba start

これでクライアント側から見れるようになるはず  
ただWindows、Macどちらの場合もワークグループ名を明示的に指定しないとログインできなかった  
ユーザ名の欄に `WORKGROUP\sambauser` のようにワークグループ名を指定した形式で入力しなければならない

* Windowsは `エクスプローラ` の `ネットワーク` にサーバが表示されるのでダブルクリックして接続
* Macは `Finder` -> `Go` -> `Connect to Server` で表示されるダイアログに `smb://hostname` と入力し接続

これらの設定で今のところ問題なく使用できている  
しかし `/var/log/samba/log.smbd` にこのようなログが出ているのでそのうち修正したい [*1](http://inaz2.hatenablog.com/entry/2013/07/07/054616) [*2](http://consultancy.edvoncken.net/index.php/HOWTO_Disable_printing_in_Samba)

    :::
    Unable to open printcap file /etc/printcap for read!

この設定の追加で上記のエラーが出なくなった

* printing = bsd
* printcap name = /dev/null
