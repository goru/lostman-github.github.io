Title: ATmega328を取り外して動作させる
Date: 2015-04-26 23:22
Category: Embedded
Tags: Arduino, ATmega328
Slug: atmega328

Arduino Uno を使って動作確認をした回路をなにかのケースに組み込んで使いたいときに  
Arduino をそのまま組み込むのは大きすぎるし、高いしあまり現実的ではないので  
Arduino に使われている [ATmega328](http://akizukidenshi.com/catalog/g/gI-03142/) を取り外して単体で使えることを確認してみた  

まず購入直後の ATmega328 には Arduino として動作させるためのブートローダが書き込まれていないので  
Arduino Uno を使ってブートローダの書き込みをしなければいけない  
Arduino に搭載されている ATmega328 は 16MHz / 5V で動作しているが、これには外部クロックが必要  
それ以外に ATmega328 の内部に搭載されている 8MHz のクロックを使う方法がある  
これを使う場合、部品点数が少なくなるし、 5V もしくは 3.3V で動作させることができる  
今回は速度は必要ではないしそれで十分なので簡単な 8MHz / 5V を選択  
その場合ブレッドボード等は既に持っているので追加で必要なものは ATmega328 と 10μF のコンデンサだけ

参考にすべきページは

* [ArduinoISP](http://www.arduino.cc/en/Tutorial/ArduinoISP) の `Instructions`
* [ArduinoToBreadboard](http://www.arduino.cc/en/Tutorial/ArduinoToBreadboard) の `Minimal Circuit`

で、前者にはおおまかな手順、後者には回路図が載っている  
ただ、 `Instructions` の方に書いてあるが、この回路図のままだと Arduino Uno では動かないので注意  
実際には回路図に加えて `RESET` と `GND` の間にコンデンサを接続する必要がある  
(できれば回路図の方に注意書きを加えておいて欲しかったなぁ)

Arduino Uno と ATmega328 の接続は回路図のままでこのようにする  
コンデンサはあとから無理やり付けたので適当だけれど気にしない

Arduino Uno | ATmega328 |
------------|-----------|
5V          | 7         |
5V          | 20        |
GND         | 8         |
GND         | 22        |
10          | 1         |
11          | 17        |
12          | 18        |
13          | 19        |

これで回路は完成  
[![image](/static/images/2015/04/DSC_0107_s.JPG)](/static/images/2015/04/DSC_0107.JPG)

Arduino IDE の準備

1. [ArduinoToBreadboard](http://www.arduino.cc/en/Tutorial/ArduinoToBreadboard) のページから `Breadboard1-0-x.zip` または `Breadboard1-5-x.zip` をダウンロードする  
(インストール済みの IDE が 1.0.6 だったので今回は `Breadboard1-0-x.zip` を使用)
2. zip を解凍して出てくる `breadboard` ディレクトリを `~/Documents/Arduino/hardware/` 以下に配置  
(場所は `Arduino` -> `Preferences` -> `Sketchbook location` で確認できる)
3. Arduino IDE を再起動すると `Tools` -> `Board` に `ATmega328 on a breadboard (8 MHz internal clock)` が追加される

Arduino Uno の準備

1. `File` -> `Examples` -> `ArduinoISP` を選択してスケッチを開く
2. `Tools` -> `Board` が `Arduino Uno` になっていることを確認してから `Upload`  

これで Arduino Uno を使ってブートローダを書き込むことができる  
ブートローダの書き込みは

1. `Tools` -> `Board` が `ATmega328 on a breadboard (8 MHz internal clock)` になっていることを確認
2. `Tools` -> `Programmer` が `Arduono as ISP` になっていることを確認
3. `Tools` -> `Burn Bootloader` で書き込み

これで ATmega328 を Arduino として動作させることができる  
実際にスケッチを書き込んで動作させるためには、また別の回路に接続しなおす必要がある  
回路図のページの `Uploading sketches to an ATmega on a breadboard` の図を参考にして以下のようにする  
この際 Arduino Uno に元から搭載されている ATmega328 は取り外しておく

Arduino Uno | ATmega328 |
------------|-----------|
RESET       | 1         |
5V          | 7         |
5V          | 20        |
GND         | 8         |
GND         | 22        |
0           | 2         |
1           | 3         |

実際にサンプルの Blink を書き込んで動作を確認してみる  
上記の回路に加えて ATmega328 の 19 番に LED を接続しておく  
Arduino Uno のピンに対応する ATmega328 のピン番号は [ATmega168/328-Arduino Pin Mapping](http://www.arduino.cc/en/Hacking/PinMapping168) に記載されている

1. `File` -> `Examples` -> `01.Basics` -> `Blink` を選択してスケッチを開く
2. `Tools` -> `Board` が `ATmega328 on a breadboard (8 MHz internal clock)` になっていることを確認してから `Upload`

[![image](/static/images/2015/04/DSC_0111_s.JPG)](/static/images/2015/04/DSC_0111.JPG)

以上で動作確認は終了  
ブートローダの書き込みと、スケッチの書き込みで回路を繋ぎ変えたりしなければいけないので結構面倒だった  
ブートローダは Arduino Uno に載せる書き込み用のシールドを作っておくと便利だろう  
スケッチの書き込みは多分シリアルがつながればいいのでUSBシリアルを載せた基板を用意しておくといいのかもしれない
