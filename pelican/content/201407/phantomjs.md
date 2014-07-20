Title: PhantomJSを使ってみた
Date: 2014-07-20 03:30
Category: Programming
Tags: JavaScript, PhantomJS
Slug: phantomjs

はじめて[PhantomJS](http://phantomjs.org/)使ってみました  
仕事で間接的に使ったことはありましたが、  
プライベートで使ったのははじめてということでテストも兼ねて記事にしてみます

なにに使ったかというと  
ドメインの管理ページのDNSの設定の書き換えの自動化です  
このサイトのドメインは[スタードメイン](http://www.star-domain.jp/)で管理しているのですが、  
ここはDDNSの機能は提供していないんですね  
このサイトはCNAMEを固定で設定できればいいので特に必要はないんですが、  
サブドメインを使って固定IPアドレスでない自宅のマシンにもアクセスできるようにしたかったのです  
ただ手動では面倒なのでできれば何らかの方法で自動的に更新しようと考えました

一般的には[MyDNS](http://www.mydns.jp/)等の外部のDDNSの機能を提供しているサービスを使用して  
このドメインで使用しているネームサーバをDDNSが提供しているものに変更するみたいです  
一応この方法も試して動作することも確認しましたが、  
PhantomJSを使って書き換える方法も比較的容易に実現できそうだったのでやってみました

ソースは[ここ](https://github.com/lostman-github/stardomain-ddns)に置いてあります  
READMEにも書いてありますが実行方法は以下です

    :::bash
    phantomjs stardomain-ddns.js "<email address>" "<password>" "<file name of DNS records>"

メールアドレスとパスワードはログインするために必要なもの  
あとはDNSの設定が書いてあるファイルのファイル名を指定します  
このファイルの中身はスタードメインの管理ページの  
「レコード一括編集(テキストエリア)」のページに表示される形式にしておきます  
なので一度手動で設定しておいて、一括編集の画面からコピペしてファイルを作ると簡単です  
スクリプトを実行すると現在の設定とファイルの中身が一致しなかった場合更新します

このスクリプトを書くにあたってはまった部分がクリックの操作です  
inputタグのボタンをクリックするには以下のようします

    :::js
    funcs.push(function () {
      page.evaluate(function() {
        document.getElementsByName('action_user_dns_index')[0].click();
      });
    });

しかし、aタグのリンクをクリックしたい場合はうまくいきません (Firefoxでは上の書き方でも動作するんですよね  
色々調べたら安心と信頼の[Stack Overflow](http://stackoverflow.com/questions/2705583/how-to-simulate-a-click-with-javascript/2706236#2706236)に書いてあったのでそれを参考にしました  
以下のようにするとクリックイベントを発生させることができました

    :::js
    funcs.push(function () {
      page.evaluate(function() {
        var elem = document.getElementsByClassName('submenu_04')[0].firstElementChild;
        var e = document.createEvent('Events');
        e.initEvent('click', true, false);
        elem.dispatchEvent(e);
      });
    });
