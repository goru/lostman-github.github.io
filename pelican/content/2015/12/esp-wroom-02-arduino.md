Title: ESP-WROOM-02をArduinoとして使ってみた
Date: 2015-12-06 19:00
Category: Embedded
Tags: ESP-WROOM-02, Arduino
Slug: esp-wroom-02-arduino

前回はPCからATコマンドをESP-WROOM-02へ送信してサーバからデータを取得してみました。
今回はESP-WROOM-02をArduinoとして動作させてみたいと思います。
外部機器を必要とせずArduinoとして自立して動作するので、センサーのデータを継続的に送信するデバイスの作成等が容易にできるようになるはずです。

まずBoards ManagerをサポートしているArduino IDEが必要なので [公式サイト](https://www.arduino.cc/en/Main/Software) から最新の1.6.6をダウンロードしてインストールしておきます。
手元の環境は古いままで1.0.6がインストールされていました。

Arduino IDEを起動したらBoards ManagerにESP8266のサイトを登録します。
ソースはgithubの [esp8266/Arduino](https://github.com/esp8266/Arduino) で管理されていて手順が記載されていました。

1. `Arduino -> Preferences -> Additional Board Manager URLs` を開いて `http://arduino.esp8266.com/stable/package_esp8266com_index.json` を追加します。
2. Arduino IDEを一度再起動して、 `Tools -> Board -> Boards Manager` を開きます。
自動で一覧が読み込まれ、 `esp8266 by ESP8266 Community` が表示されているはずなので選択してインストールします。 (現時点では2.0.0でした。)
4. インストール後にもう一度IDEを再起動して (Boardの表示が二重になっていておかしかったので) `Tools -> Board -> Generic ESP8266 Module` を選択します。
5. 最後に `Tools -> Port ->` で接続しているUSBシリアルのデバイスを選択すれば準備は完了です。

スケッチを書き込むにはESP-WROOM-02をUART download modeで起動する必要があります。 ([Hardware User Guide](http://doc.switch-science.com/datasheets/0B-ESP8266__Hardware_User_Guide__EN_v1.1.pdf) の `4.2. Download Firmware` )
他の人の作例では `IO0` と `RST` にタクトスイッチを接続しているケースが多いようで、以下の動作になるようにスイッチを操作します。

1. IO0をGNDと接続
2. ESP-WROOM-02を(再)起動
3. IO0をGNDから切断 (起動したタイミングでのみチェックしているので)

とりあえず空のスケッチを書き込んでみたらこのように出力されたのでうまくできていそうです。

    :::

    Sketch uses 198,580 bytes (45%) of program storage space. Maximum is 434,160 bytes.
    Global variables use 32,982 bytes (40%) of dynamic memory, leaving 48,938 bytes for local variables. Maximum is 81,920 bytes.
    Uploading 202736 bytes from /var/folders/2r/gnf1wxzd7ysd8ps4cwmhpsn00000gp/T/build47405d589e6a6ed4482aeeb82c132d10.tmp/sketch_dec06a.ino.bin to flash at 0x00000000
    ......................................................................................................................................................................................................


試しにアクセスポイントへ接続して、ウェブサーバーから取得したデータを、シリアル経由で送信するスケッチを書いてみました。
(一度だけ実行されればいいのでsetupに全ての処理を書いています。)
上述の手順でスケッチをアップロードし、アップロードが終わったらシリアルモニタを開いてみましょう。
シリアルモニタに取得したHTMLが表示されていれば成功です。

    :::c

    #include <ESP8266WiFi.h>
    
    #define WIFI_SSID   "<SSID>"
    #define WIFI_PASSWD "<PASSWORD>"
    
    #define TARGET_HOST "www.google.com"
    #define TARGET_PORT 80
    
    void setup() {
      Serial.begin(115200);
      
      Serial.println();
      Serial.print("Connecting to ");
      Serial.print(WIFI_SSID);
      
      WiFi.begin(WIFI_SSID, WIFI_PASSWD);
      
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      
      Serial.println();
      Serial.print("IP address is ");
      Serial.println(WiFi.localIP());
    
      WiFiClient client;
      Serial.print("Connecting to ");
      Serial.println(TARGET_HOST);
      
      if (!client.connect(TARGET_HOST, TARGET_PORT)) {
        Serial.println("Could not connect.");
        return;
      }
    
      client.print("GET / HTTP/1.0\r\n\r\n");
    
      delay(100);
      
      while (client.available()) {
        Serial.print(client.readStringUntil('\r'));
      }
    
      Serial.println();
      Serial.println("Done");
    }
    
    void loop() {
      // put your main code here, to run repeatedly:
    
    }
