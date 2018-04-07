Title: RaspberryPi ZeroをOTGモードで使う
Date: 2018-01-28 22:43
Category: Computer
Tags: Gentoo, Linux, RaspberryPi
Slug: zero-org

RaspberryPi Zeroに [USB Stem](https://shop.pimoroni.com/products/zero-stem-usb-otg-connector) を
取り付けてみました。

取り付けとRaspbianの準備に関しては [PIMORONI](https://shop.pimoroni.com/products/zero-stem-usb-otg-connector) と
そこからリンクされている [公式](https://zerostem.io/installation/) と
[Gist](https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a) を参考にすれば簡単にできました。

Macで使う場合は、ドライバも必要ないしBonjourも動作しているのでなんの準備も必要なくSSHでつなぐことができました。
インターネット共有の設定をすればインターネットへ接続するのもOK。

ただ自分のLinuxの環境はGentooなのでドライバも無効になっていたし、Avahiも入っていなかったので少しハマりました。
まずカーネルの設定で `CONFIG_USB_NET_CDCETHER` を有効にするとRaspberryPiを認識できるようになります。

    :::
    Device Drivers  --->
      Network device support  --->
        USB Network Adapters  --->
          Multi-purpose USB Networking Framework
            CDC Ethernet support (smart devices such as cable modems)

有効にした上で接続するとdmesgとifconfigにこのように出力されます。(なんかエラーでてるけど…)

    :::
    $ dmesg
    [ 1450.001875] usb 3-1.2: new high-speed USB device number 6 using xhci_hcd
    [ 1450.341883] usb 3-1.2: device descriptor read/64, error -71
    [ 1451.137854] usb 3-1.2: device descriptor read/64, error -71
    [ 1451.311832] usb 3-1.2: new high-speed USB device number 7 using xhci_hcd
    [ 1451.402720] usb 3-1.2: New USB device found, idVendor=0525, idProduct=a4a2
    [ 1451.402725] usb 3-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=0
    [ 1451.402728] usb 3-1.2: Product: RNDIS/Ethernet Gadget
    [ 1451.402730] usb 3-1.2: Manufacturer: Linux 4.9.59+ with 20980000.usb
    [ 1451.412841] cdc_ether 3-1.2:1.0 usb0: register 'cdc_ether' at usb-0000:00:14.0-1.2, CDC Ethernet Device, a2:a1:76:81:c5:63
    [ 1451.416086] cdc_ether 3-1.2:1.0 enp0s20u1u2: renamed from usb0

    $ ifconfig enp0s20u1u2
    enp0s20u1u2: flags=4098<BROADCAST,MULTICAST>  mtu 1500
            ether a2:a1:76:81:c5:63  txqueuelen 1000  (Ethernet)
            RX packets 0  bytes 0 (0.0 B)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 0  bytes 0 (0.0 B)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

で、Avahiを入れようと思ったのだけれど、いまいちよくわかっていないのと、
このためだけに入れるのもどうなのかなと思っていたら
[digで問い合わせることができる](http://hateda.hatenadiary.jp/entry/mdns-and-vagrant)
という情報を見つけたのでこの方法を試してみることにしました。

参考にしたサイトでは省略されているけれど、今回はNICが複数あるので
(元からあるNICとRaspberryPiがNICとして認識されているため)
digコマンドを実行する時に `-b` オプションでbindするIPアドレスを渡して
マルチキャストのパケットを送出する元のNICを指定する必要がありました。
(そうでなければデフォルトゲートウェイのNIC?)

インターフェイス名ではなくIPアドレスなので、mDNSで使われる適当な
[リンクローカルアドレス](https://en.wikipedia.org/wiki/Link-local_address) を与えてNICを有効にしました。

    :::
    # ifconfig enp0s20u1u2 169.254.0.1 up

    $ ifconfig enp0s20u1u2
    enp0s20u1u2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 169.254.0.1  netmask 255.255.0.0  broadcast 169.254.255.255
            inet6 fe80::f0a3:d4ff:fe8b:fb1c  prefixlen 64  scopeid 0x20<link>
            ether f2:a3:d4:8b:fb:1c  txqueuelen 1000  (Ethernet)
            RX packets 911  bytes 34763 (33.9 KiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 29  bytes 2318 (2.2 KiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

次にbindするIPアドレスを指定して `raspberrypi.local` を問い合わせると
RaspberryPiのIPアドレスを得ることができました。SSHの接続もOK。

    :::
    $ dig +short raspberrypi.local. @224.0.0.251 -p 5353 -b 169.254.0.1
    169.254.39.21

    $ ssh pi@169.254.39.21
    The authenticity of host '169.254.39.21 (169.254.39.21)' can't be established.
    ECDSA key fingerprint is SHA256:eKyA7UiU1i+l0eAh+YT7MrjTadCdewpTuwcjSdw3aUg.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added '169.254.39.21' (ECDSA) to the list of known hosts.
    pi@169.254.39.21's password:
    Linux raspberrypi 4.9.59+ #1047 Sun Oct 29 11:47:10 GMT 2017 armv6l
    
    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.
    
    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Thu Jan 25 09:34:23 2018 from 169.254.10.10
    
    SSH is enabled and the default password for the 'pi' user has not been changed.
    This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

インターネット共有に関しては試してないけれど恐らくブリッジを使えばうまく行くんじゃないかな(適当
