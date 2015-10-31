Title: WN-G300UAを使ってみる
Date: 2015-11-01 03:30
Category: Computer
Tags: Linux, Gentoo
Slug: wn-g300ua

今までWiFiのアクセスポイントには [WLI-UC-GNM](http://buffalo.jp/product/wireless-lan/client/wli-uc-gnm/) を使用していたのですが、たまにOSごと巻き込んでクラッシュするのとアンテナがないので電波が悪い部屋があったので交換してみることに  
アンテナがついている機種でLinuxでの動作実績がありそうなものを探した結果 [WN-G300UA](http://www.iodata.jp/product/network/adp/wn-g300ua/) が [RaspberryPiでの動作実績もあるみたい](http://itkobo-z.jp/wp/archives/432) で良さそうだったので購入してみました  
ちなみにWLI-UC-GNMは772円、WN-G300UAは1470円でした  
上述の参考サイトにはモジュールのオプションでパワーマネージメントを無効にすれば普通に動くということだったのですが、これから色々ハマるとは思いもしませんでした…

* このデバイス用のドライバがカーネルに含まれていますがまともに動作しませんでした (繋がるけれどすぐ切れるという動作 Kernel 3.14.48)
* チップセットメーカーもドライバを提供していて参考にしていたサイトではそれを使うように説明がありました  
しかし手元のカーネルではビルドすらできませんでした  
参考にしていたサイトはRaspberryPiを使ったサイトが多かったのですが、彼らの使用しているカーネルは古かったようです

いろいろ検証した結果ArchLinuxのパッケージで使われているリポジトリとパッチを当てたものを使用すれば動作することがわかりました  
Arch以外のディストリビュージョンではそのままビルドすることができないのでArchで使っているリポジトリをサブモジュールにしてMakefileとWN-G300UA用のパッチを追加したリポジトリを作成しました

* [8192cu](https://github.com/lostman-github/8192cu)
* [hostapd-rtl](https://github.com/lostman-github/hostapd-rtl)

以下の手順でビルドすることができます

    :::bash
    $ git clone https://github.com/lostman-github/8192cu
    $ cd 8192cu
    $ git checkout WN-G300UA
    $ git submodule init
    $ git submodule update
    $ make
    $ cd -
    
    $ git clone https://github.com/lostman-github/hostapd-rtl
    $ cd hostapd-rtl
    $ git checkout WN-G300UA
    $ git submodule init
    $ git submodule update
    $ make
    $ cd -

これで `8192cu/src/8192cu.ko` と `hostapd-rtl/src/hostapd/hostapd` がビルドされます  
`hostapd-rtl/src/hostapd/hostapd.conf` にWN-G300UA用の修正も含まれているので以下の部分を書き換えるだけで動作するはず

* ssid
* wpa_passphrase

修正したら以下のコマンドでアクセスポイントを起動します

    :::bash
    # insmod 8192cu/src/8192cu.ko rtw_power_mgnt=0 rtw_enusbss=1 rtw_ips_mode=1
    # ./hostapd-rtl/src/hostapd/hostapd -P /run/hostapd.pid -B hostapd-rtl/src/hostapd/hostapd.conf

今の所このドライバとhostapdの組み合わせで大きな問題は起きていませんが、稀にhostapdがおかしくなるようでアクセスポイントに接続できなくなってしまうことがあります  
その場合はhostapdを再起動すると解消するようです (ただ面倒くさい)  
電波の問題は解決できましたが、結局安定性に関しては以前よりはマシだがいまいち解決せずという状況です…
