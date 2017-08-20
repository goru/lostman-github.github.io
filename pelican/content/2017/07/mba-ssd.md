Title: MacBook Air (11-inch, Mid 2012) のSSDをM.2接続のSSDに換装した
Date: 2017-07-15 23:10
Category: Computer
Tags: Mac, SSD
Slug: mac-ssd

### JetDrive高すぎ問題

MacBook Air (11-inch, Mid 2012) のメモリを8GBにカスタマイズしたものを使っています。
このマシンは主に仕事で使っていて、XcodeやらIntelliJやらを入れているので標準の128GBではカツカツの状態でした。
ちょっと思うところがあってWindowsの仮想マシンを用意したいなと考えたのですが、この状態ではどうにもならないので思い切って換装することにしました。

MacBook AirのSSDを換装するとなるとTranscendの [JetDrive](https://jp.transcend-info.com/apple/jetdrive/) が主な選択肢になるようです。
ただし [Transcend JetDrive 480GB TS480GJDM520](http://amzn.asia/f7ZsZVw) が40196円なのに対して、
今回購入した [Crucial MX300 525GB CT525MX300SSD4/JP](http://amzn.asia/4doAZ53) は18080円で、自作などに使われるM.2のSSDと比べると倍くらいの値段になっています。
幸い使っているMacBook AirはM.2接続のSSDが使えることがわかっています。
できれば動作が保証されていそうなJetDriveを使いたいところですが、値段に負けてこちらを選ぶことにしました。

当然M.2のSSDをそのまま接続することはできないので [M.2のコネクタをMacBook AirのSSDのコネクタに変換するアダプタ](http://amzn.asia/9nSJNCb) と、
[MacBook AirのSSDをSATAへ変換するためのアダプタ](http://amzn.asia/0jF8ZJu) も合わせて購入しました。

- [Crucial MX300 525GB CT525MX300SSD4/JP](http://amzn.asia/4doAZ53) 18080円
- [M.2のコネクタをMacBook AirのSSDのコネクタに変換するアダプタ](http://amzn.asia/9nSJNCb) 1080円
- [MacBook AirのSSDをSATAへ変換するためのアダプタ](http://amzn.asia/0jF8ZJu) 1450円

[![image](/static/images/2017/07/DSC_1410_s.JPG)](/static/images/2017/07/DSC_1410.JPG)

これ以外に今回の場合SATAをUSBに変換するアダプタが必要でしたが、これは手持ちのものが使えました。
あとネジが特殊なので裏蓋用とSSD用の2種類のドライバーが必要だと思います。同僚が持っていたので借りることができました。
少し省かれたものもありますが、だいたい2万円程度で512GBへ換装することができることになります。
個人的に4万かかることに少し抵抗があったので、2万ちょっとで済むとなるとやってもいいかなという気持ちになりました。
換装後に残るMacBook AirのSSDはSATAに変換するアダプタも残るので、サーバマシンにでも内蔵しようかと思います。

### 使い方と手順

これらを組み合わせて換装の作業ではこのように使いました。

- MX300(M.2のSSD)をUSB経由で接続するときは  
  [MX300] -> [M.2 -> MBA変換] -> [MBA -> SATA変換] -> [SATA -> USB変換] -> [MBAのUSB]
- MX300をMacBook Airに内蔵するときは  
  [MX300] -> [M.2 -> MBA変換] -> [MBA内のコネクタ]
- MacBook AirのSSDをUSB経由で接続するときは  
  [MBAのSSD] -> [MBA -> SATA変換] -> [SATA -> USB変換] -> [MBAのUSB]

実際の換装の手順は以下のようになります。

1. MX300をUSB経由でMacBook Airへ接続
2. MacBook Airをリカバリーモードで起動
3. MX300を初期化 (パーティションの作成&フォーマット)
4. MacBook AirのSSDからMX300へディスクユーティリティの復元機能を使ってデータを移行
5. MacBook Airの裏蓋を開けて実際に換装

1-3はリカバリーモードへの入り方 ( [command + Rを押しながら起動](https://support.apple.com/ja-jp/HT201255) ) 以外は特に引っかかるところはありませんでした。
4の復元のやり方と、5での換装時に外しておくべき電源ケーブルの位置がよくわからなかったので以下にまとめておきます。

### 4. MacBook AirのSSDからMX300へディスクユーティリティの復元機能を使ってデータを移行

復元をする際に復元元と復元先、それぞれの対象を指定する必要がありますが、
元々Macユーザーではないせいか使い方がよくわかりませんでした。
結論としてはまず `復元先` の `パーティション` を選択してメニューの復元を実行します。
`復元元` を選ぶダイアログが表示されるので、ここで復元元の `パーティション` を選択して実行すればOKです。

[![image](/static/images/2017/07/DSC_1419_s.JPG)](/static/images/2017/07/DSC_1419.JPG)
[![image](/static/images/2017/07/DSC_1421_s.JPG)](/static/images/2017/07/DSC_1421.JPG)

### 5. MacBook Airの裏蓋を開けて実際に換装

ネジを外して裏蓋を開けるとバッテリーとSSD等にアクセスできます。
まず電源コネクタを上へ持ち上げるようにして外します。 (横方向へスライドさせるのではないので注意)
次にSSDのネジを外してSSDを横方向にスライドさせて取り外します。
取り付けは逆の手順で行います。

[![image](/static/images/2017/07/DSC_1427_s.JPG)](/static/images/2017/07/DSC_1427.JPG)
[![image](/static/images/2017/07/DSC_1428_s.JPG)](/static/images/2017/07/DSC_1428.JPG)

### おわり

無事新しいSSDで起動できたら作業は終わりです。
念の為旧SSDをUSB経由で接続して復元機能を使ってイメージでバックアップを取っておきました。

純正でないSSDではTrimが無効になるみたい [*](http://www.softantenna.com/wp/mac/trimforce-on-os-x-el-capitan-2/) なので、
trimforceコマンドを使って手動で有効にしました。

    :::bash
    $ sudo trimforce enable

現在の状態は `システム情報` から確認できます。

[![image](/static/images/2017/07/trim.png)](/static/images/2017/07/trim.png)

速度は計測していませんが、特別不満も感じないのでそこそこ出ているのでしょう (多分)
比較的安くストレージを増強することができました。
