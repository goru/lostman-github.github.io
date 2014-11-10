Title: Macのホスト名を固定する
Date: 2014-11-10 09:51
Category: Computer
Tags: Mac
Slug: mac-hostname

自宅のMacでは設定済みだったんだけれど、オフィスのMacでは未設定だったのでメモ

    :::bash
    $ scutil --get HostName
    HostName: not set

この結果になる場合ターミナルで表示されるホスト名がDNSから逆引きしたものになることがあるみたい  
オフィスの環境だとならないけれど、自宅の環境だと `System Preferences -> Sharing` で  
元々設定してある大文字小文字混じりのホスト名が全て小文字に変わってしまう  
ここの `Edit` を押すと `Use dynamic global hostname` といういかにもそれっぽい設定があるけれどこれは特に効果はなし  
そのような場合は冒頭で確認するために使ったコマンドを使って固定することができる

    :::bash
    # scutil --set HostName YourHostName

ただこの設定はSystem Preferencesの設定とは別にあるようで同期しない  
そのためここで元々の設定とは全く別の値を指定することができるが  
混乱の元なのでそういったことが起きないように気をつける必要がある
