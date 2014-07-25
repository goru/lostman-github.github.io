Title: AquesTalk pico LSIをI2Cで接続する
Date: 2014-07-25 23:49
Category: Embedded
Tags: Arduino, AquesTalk pico LSI
Slug: aquestalk-i2c

ArduinoとAquesTalkをI2Cで接続してみました  
配線は以下の通り  
(表にしたらテーマの関係上すごく見づらかったので変更する予定)

    :::
    PIN | AquesTalk | -> | Arduino
    ----|-----------|----|--------
    1   | /RESET    |    | RESET
    4   | SMOD0     |    | GND
    5   | SMOD1     |    | 5V
    7   | VCC       |    | 5V
    8   | GND       |    | GND
    20  | VCC       |    | 5V
    22  | GND       |    | GND
    27  | SDA       |    | A4
    28  | SCL       |    | A5

SMOD0/SMOD1についてはデータシートの 表9.1 通信モード を参照  
I2Cで接続するには SMOD0 = 0, SMOD1 = 1 にする必要があります  
あとは12番のAOUTをアンプのIN+、GNDをIN-に接続します

![AquesTalk pico LSI I2C](/static/images/2014/07/IMAG1036.jpg)

データシートの 5. 基本回路 にある回路図を見ると、これ以外にVCCとAOUTにコンデンサが追加されています  
これはバイパスコンデンサというものらしく電源の安定化やノイズの発生を抑えたりする役割があるそうです [*1](http://www.geocities.jp/zattouka/GarageHouse/micon/circuit/VoltREG.htm#pascon)  
とりあえず、無しでも動きました(ぇ

他に 9.2. I2C通信 の部分を見るとSDA、SCL共に5KΩ程度のプルアップ抵抗が必要とあります  
プルアップ抵抗なんですが調べたところ標準のWire.hを使う場合Arduino内蔵の抵抗で問題なさそうなので [*2](http://www.senio.co.jp/bbs/viewtopic.php?f=7&t=260) [*3](http://myboom.mkch.net/modules/pukiwiki/180.html)  
これも無しで試したところ、動きました

というわけでAquesTalk以外に特に部品を追加することなく準備ができました  
動作確認に使用したスケッチは[GitHub](https://github.com/lostman-github/arduino/blob/master/Uno/AquesTalk/sample/sample.ino)にありますがここに貼り付けておきます [*4](http://enajet.air-nifty.com/blog/2012/01/aquestalk-pico-.html)

    :::cpp
    #include <Wire.h>
    
    #define PICO_I2C_ADDRESS 0x2E
    
    void setup() {
      Wire.begin();
    }
    
    void loop() {
      isReady();
    
      Wire.beginTransmission(PICO_I2C_ADDRESS);
      Wire.write("yukkurisiteittene\r");
      Wire.endTransmission();
    
      // send once
      while(1) {}
    }
    
    void isReady() {
      while(1) {
        Wire.requestFrom(PICO_I2C_ADDRESS, 1);
    
        while(Wire.available() > 0){
          if(Wire.read() == '>') {
            return;
          }
    
          delay(10);
        }
      }
    }

