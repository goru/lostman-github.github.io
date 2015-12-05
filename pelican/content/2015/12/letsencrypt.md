Title: GentooとNginxでLet's Encryptを使う
Date: 2015-12-05 22:30
Category: Computer
Tags: Gentoo, Nginx
Slug: letsencrypt

[Let's Encrypt](https://letsencrypt.org/) がPublic Betaになったので使ってみました。
Gentooに関してはまだ実験的なサポートで、Nginxはこれからプラグインが取り込まれる予定みたいです。 (なので他の組み合わせて使うより多少不便なのかもしれない)
ただ試してみた結果現状でもとても簡単に利用できました。

基本的には [ドキュメント](https://letsencrypt.readthedocs.org/en/latest/intro.html) の [Installation](https://letsencrypt.readthedocs.org/en/latest/intro.html#installation) と [How to run the client](https://letsencrypt.readthedocs.org/en/latest/intro.html#how-to-run-the-client) の章を読めば事足りて、
あとは必要に応じて [User Guide](https://letsencrypt.readthedocs.org/en/latest/using.html) も読むといいはず。

まず必要なファイルはgithubからcloneするだけ、コマンドを実行したタイミングでディストリビュージョンごとに必要なパッケージが自動でインストールされるようになっていました。
Gentooの場合は `bootstrap/_gentoo_common.sh` に書かれていて以下のパッケージがインストールされるようになっていました。
あと普通に実行するとGentooは実験的なサポートなので `--debug` をつけて実行するように言われるのでそのようにします。
ただこれは初回のパッケージのインストール時のみ必要みたいなので、次回以降はつける必要がありませんでした。

    :::bash
    PACKAGES="dev-vcs/git
      dev-lang/python:2.7
      dev-python/virtualenv
      dev-util/dialog
      app-admin/augeas
      dev-libs/openssl
      dev-libs/libffi
      app-misc/ca-certificates
      virtual/pkgconfig"

とりあえず `--help` を指定して起動してみると、これだけでパッケージのインストールが始まりました。

    :::bash
    $ git clone https://github.com/letsencrypt/letsencrypt
    $ cd letsencrypt
    $ ./letsencrypt-auto --debug --help

これで下準備が済んだので証明書の取得ができます。
コマンドを実行するとLet's Encryptのアカウント?の取得から証明書の生成までを自動で行ってくれるみたいです。

* まだプラグインが対応していないNginxを使うので `certonly` と `--standalone` を指定。
* `--standalone-supported-challenges tls-sni-01` を指定する必要がありました。
僕の環境ではHTTPSしか通らないようになっているので `tls-sni-01` を指定。
(おそらく)ドメインの存在確認のためにLet's Encryptのコマンドが80か443のポートで待ち受ける必要があるみたいです。
なのでこのコマンドは実際に使用するドメインが割り当てられているマシン、かつNginxを停止した状態で実行する必要があると思われます。
(停止しないで実行するとエラーになりました、Apacheなどの対応しているウェブサーバーの場合は停止しないで実行できるのだと思います)
詳細は [User Guide/Plugins/Standalone](https://letsencrypt.readthedocs.org/en/latest/using.html#standalone) を参照
* `--email` にメールアドレスを指定。
適当なアドレスを指定できましたが、アカウントの情報を復活させるためにも使われるみたいなので連絡がつくアドレスを指定したほうがよさそうです。
* `-d` は証明書を使うドメイン名を指定。

実際のコマンドはこのようにしました。

    :::bash
    $ ./letsencrypt-auto certonly --standalone --standalone-supported-challenges tls-sni-01 --email <Your email address> -d <Your domain name>
    Updating letsencrypt and virtual environment dependencies.......
    Running with virtualenv: sudo /home/admin/.local/share/letsencrypt/bin/letsencrypt certonly --standalone --standalone-supported-challenges tls-sni-01 --email <Your email address> -d <Your domain name>

コマンドを実行するとこのような同意画面が出るのでよく読んで同意

[![image](/static/images/2015/12/letsencrypt-terms.png)](/static/images/2015/12/letsencrypt-terms.png)

最後にこのようなメッセージが表示されました。
`/etc/letsencrypt` に生成された諸々のファイルが保存されているのでバックアップするように、と書かれています。
あと証明書の有効期限は3ヶ月と短くなっているので有効期限が過ぎる前に更新する必要があります。
同じコマンドを再度実行することで更新できます。
([User Guide/Renewal](https://letsencrypt.readthedocs.org/en/latest/using.html#renewal) を参照、ここにはcrontabに書いておくようにと記載があります)

    :::bash
    IMPORTANT NOTES:
     - If you lose your account credentials, you can recover through
       e-mails sent to <Your email address>.
     - Your account credentials have been saved in your Let's Encrypt
       configuration directory at /etc/letsencrypt. You should make a
       secure backup of this folder now. This configuration directory will
       also contain certificates and private keys obtained by Let's
       Encrypt so making regular backups of this folder is ideal.
    
     - Congratulations! Your certificate and chain have been saved at
       /etc/letsencrypt/live/<Your domain name>/fullchain.pem. Your cert
       will expire on 2016-03-03. To obtain a new version of the
       certificate in the future, simply run Let's Encrypt again.
     - If like Let's Encrypt, please consider supporting our work by:
    
       Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
       Donating to EFF:                    https://eff.org/donate-le

最後にNginxで生成された証明書を使うように設定します。
`/etc/letsencrypt/live/<Your domain name>/` 以下に指定したドメインの証明書一式が保存されているので、
`/etc/nginx/nginx.conf` のSSL証明書の部分を以下のように編集して再起動すればOKです。
再起動したらブラウザで接続してLet's Encryptの証明書が使われているか確認してみます。

    :::
    ssl_certificate     /etc/letsencrypt/live/<Your domain name>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<Your domain name>/privkey.pem;


