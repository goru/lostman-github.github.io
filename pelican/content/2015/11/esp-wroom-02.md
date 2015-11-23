Title: ESP-WROOM-02を試してみた
Date: 2015-11-23 19:20
Category: Embedded
Tags: ESP-WROOM-02
Slug: esp-wroom-02

ESP-WROOM-02を試してみました。
ESP-WROOM-02はデフォルトではATコマンドで操作を受け付けるファームウェアが書き込まれています。
それ以外にArduinoやNodeMCUとして使えるファームウェアも使用することができるみたいです。

今回試したのはATコマンドでの動作です。
これはPCとUSBシリアルで接続してシリアルコンソールからATコマンドを送ることで操作します。
今回使ったものは以下。

* [FT231X USBシリアル変換モジュール AE-FT231X](http://akizukidenshi.com/catalog/g/gK-06894/) 750円
* [低損失CMOS三端子レギュレータ 3.3V 500mA NJU7223F33](http://akizukidenshi.com/catalog/g/gI-00432/) 50円
* [ESP-WROOM-02ピッチ変換済みモジュール《フル版》](https://www.switch-science.com/catalog/2347/) 1100円
* その他抵抗等

USBシリアルは今後もよく使うと思うのでこのような変換基板を作ってみました。
今回は使わないけれど、リセットボタンと5V/3Vの切り替えスイッチ付き。

[![image](/static/images/2015/11/usb-serial_s.png)](/static/images/2015/11/usb-serial.png)

上記のUSBシリアル変換基板とESP-WROOM-02を次のように接続するだけで動作確認できます。
ESP-WROOM-02への電源は消費電力の問題から、USBシリアルの3.3Vは使用せず、5Vを三端子レギュレータを介して入力するようにします。
([ESP-WROOM-02を使ってみる3 -そんな電源で大丈夫か-](http://nemuisan.blog.bai.ne.jp/?eid=216185))

[![image](/static/images/2015/11/esp-wroom-02_s.png)](/static/images/2015/11/esp-wroom-02.png)
[![image](/static/images/2015/11/DSC_0565_s.JPG)](/static/images/2015/11/DSC_0565.JPG)

次にPCとの接続にはUSBシリアルのドライバをインストールしなければいけないので、FTDIのページからVCP Driverをダウンロードしてインストールしておきます。

* [Virtual COM Port Drivers](http://www.ftdichip.com/Drivers/VCP.htm)

PCと接続したらArduino IDEを起動して `Tools -> Serial Port` から認識されているデバイスを選択します。
選択したら `Tools -> Serial Monitor` をクリックしてシリアルモニタを起動します。

[![image](/static/images/2015/11/Screenshot_2015-11-01-15-12-00_s.png)](/static/images/2015/11/Screenshot_2015-11-01-15-12-00.png)

シリアルモニタが起動したら `Both NL & CR` 、 `115200 baud` に設定を変更します。
`AT` と入力して `OK` が返ってくればモジュールの起動には成功して使用可能状態になっています。
以下の `>` の行のコマンドを入力していくと、WiFiのアクセスポイントに接続し、HTTPで外部のリソースにアクセスすることができます。
([Arduino勉強会/0N-WiFiモジュールその１](http://www.pwv.co.jp/~take/TakeWiki/index.php?Arduino%E5%8B%89%E5%BC%B7%E4%BC%9A%2F0N-WiFi%E3%83%A2%E3%82%B7%E3%82%99%E3%83%A5%E3%83%BC%E3%83%AB%E3%81%9D%E3%81%AE%EF%BC%91))

    :::
    > AT
    
    OK
    
    # Stationモードにする (APモードなどもある)
    > AT+CWMODE=1
    
    OK
    
    # アクセスポイントに接続
    > AT+CWJAP="SSID","PASSWORD"
    
    WIFI DISCONNECT
    WIFI CONNECTED
    WIFI GOT IP
    
    OK
    
    # モジュールに割り当てられているIPアドレスとMACアドレスを表示
    > AT+CIFSR
    
    +CIFSR:STAIP,"IP_ADDRESS"
    +CIFSR:STAMAC,"MAC_ADDRESS"
    
    OK
    
    # サーバに接続
    > AT+CIPSTART="TCP","www.google.co.jp",80
    
    CONNECT
    
    OK
    
    # 送信するバイト数を設定、今回は `GET / HTTP/1.0` と改行2回分の18Byte
    > AT+CIPSEND=18
    
    OK
    
    > GET / HTTP/1.0
    
    Recv 18 bytes
    
    SEND OK
    
    +IPD,494:HTTP/1.0 302 Found
    Cache-Control: private
    Content-Type: text/html; charset=UTF-8
    Location: http://www.google.co.jp/?gfe_rd=cr&ei=L601Vq2QHfP98wf0qZKADQ
    Content-Length: 261
    Date: Sun, 01 Nov 2015 06:11:59 GMT
    Server: GFE/2.0
    
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
    <TITLE>302 Moved</TITLE></HEAD><BODY>
    <H1>302 Moved</H1>
    The document has moved
    <A HREF="http://www.google.co.jp/?gfe_rd=cr&amp;ei=L601Vq2QHfP98wf0qZKADQ">here</A>.
    </BODY></HTML>
    
    CLOSED

とりあえずGoogleにアクセスすることはできました。
ATコマンド経由で使用するにはシリアル経由で他のデバイスと接続する必要があり、その場合無駄に複雑になってしまいます。
せっかくESP-WROOM-02自体をArduinoとして使用できるので、そうすればとてもシンプルなシステムになるはず。
次回はこのモジュールをArduinoとして使う方法を試したいと思います。
