Title: AquesTalk pico LSIの動作確認
Date: 2014-07-21 17:49
Category: Embedded
Tags: Arduino, AquesTalk pico LSI
Slug: aquestalk

以前購入していた[ATP3011F1-PU](http://www.a-quest.com/products/aquestalkpicolsi.html)([秋月](http://akizukidenshi.com/catalog/g/gI-06220/))の動作確認をしてみました  
紹介動画にもありますがArduino UNOに挿してアンプ付きのスピーカと接続、  
PCからシリアルモニタで文字を送信するだけで音声を出すことができます  
(技術資料 13.4. Arduinoボードを利用した簡易動作 を参照)  
通常Arduinoから使う場合はI2C接続で使うことになると思いますが、  
I2C接続は後日試すとして今回はこの方法で動作確認をしてみました

まずうちにはアンプ付きのスピーカなんて無いのでそれを用意するところから  
せっかくなのでこれも秋月で買ってきて組み立ててみました  
といっても個別にパーツを揃えたわけでなく

* [ＰＡＭ８０１２使用２ワットＤ級アンプモジュール](http://akizukidenshi.com/catalog/g/gK-08217/)
* [３．５ｍｍステレオミニジャックＤＩＰ化キット](http://akizukidenshi.com/catalog/g/gK-05363/)
* [電池ボックス　単３×２本（リード線・耳付）](http://akizukidenshi.com/catalog/g/gP-02679/)
* 100均で売っているスピーカ

これらを接続しただけです  
今回試した手順を以下にまとめておきます  
後半は技術資料に書いてあるものそのままで、どちらかと言うと前半が僕には必要でした

1. ArduinoのLSIを取り外し、AquesTalkを取り付け
1. Arduinoのデジタル6番をアンプのIN+に接続
1. ArduinoのGNDをアンプのIN-に接続
1. アンプの+VとGNDをそれぞれ電池に接続
1. アンプのSPK+とSPK-をジャックのRとGに接続
1. ジャックにスピーカを接続
1. ArduinoをPCに接続、Arduino IDEを起動
1. メニューのTools -> Serial Monitorを開く
1. 右下のコンボボックスでCarriage returnと9600bpsを選択
1. 上のインプットボックスに `?` を入力してEnter
1. `konnichiwa` 等を入力してEnterを押すと発声する