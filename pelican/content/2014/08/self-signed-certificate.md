Title: Nginxで自己署名証明書を使う
Date: 2014-08-16 02:42
Category: Computer
Tags: Nginx
Slug: self-signed-certificate

ドメインを取ったのでそのうちきちんとした証明書を使おうかとは思っていますが  
とりあえずしばらくはオレオレ証明書で運用しようと思っています  
ということで作成の仕方をメモ

1. パスフレーズなしの秘密鍵を作成  
色々なサイトを見ていると一度パスフレーズありで作成してから  
パスフレーズを削除したファイルを作りなおすような手順を踏んでいたりしますがこれでよさそう

        :::bash
        # openssl genrsa -out server.key 2048
        Generating RSA private key, 2048 bit long modulus
        ................................................+++
        ........................................+++
        e is 65537 (0x10001)

1. 公開鍵の作成  
HTTPSで暗号化されていればいいだけなので `Common Name` 以外は適当でいいです  
`.` を入力した場合そのフィールドは空になるみたいなので全て空にしました

        :::bash
        # openssl req -new -key server.key -out server.csr
        You are about to be asked to enter information that will be incorporated
        into your certificate request.
        What you are about to enter is what is called a Distinguished Name or a DN.
        There are quite a few fields but you can leave some blank
        For some fields there will be a default value,
        If you enter '.', the field will be left blank.
        -----
        Country Name (2 letter code) [AU]:.
        State or Province Name (full name) [Some-State]:.
        Locality Name (eg, city) []:
        Organization Name (eg, company) [Internet Widgits Pty Ltd]:.
        Organizational Unit Name (eg, section) []:
        Common Name (e.g. server FQDN or YOUR name) []:<your domain name>
        Email Address []:
        
        Please enter the following 'extra' attributes
        to be sent with your certificate request
        A challenge password []:
        An optional company name []:

1. 証明書の作成

        :::bash
        # openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt
        Signature ok
        subject=/CN=<your domain name>
        Getting Private key

1. 以上で証明書の準備はできたので `/etc/nginx/nginx.conf` を編集して再起動すれば完了です

        :::bash
        server {
                listen 443 ssl;
                ssl_certificate     /path/to/certificate/server.crt;
                ssl_certificate_key /path/to/certificate/server.key;
