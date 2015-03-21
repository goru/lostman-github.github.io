Title: Redmineをインストールしてみた
Date: 2015-03-21 15:53
Category: Computer
Tags: Ruby, Redmine, Nginx
Slug: redmine

Googleカレンダーに予定を入れるようにしていたんだけれど、カレンダーなので日付を入れなくてはいけなくて  
日にちが決まってないけれどやろうと思っていることを入れておくことができないのでちょっと不便でした  
Redmine等のプロジェクト管理ソフトを入れるのは大袈裟な気がしていたんだけれどRedmineは以前仕事でも使っていたし  
自分のサーバにインストールして使うとなると思いの外選択肢が少ない感じだったのでRedmineを入れてみました

もやっとした要件は

* サービスでなく、自分のサーバにインストールできること
* 依存するものが少なく、導入が楽
* 日付を入れずにタスクを登録できる
* 優先度を設定できる
* 日付が入っているものはカレンダーで確認できる
* スマホからタスクを確認、編集できる

なんとなく導入が面倒というイメージを持っていたんだけれど、手順を見る限り簡単そうでした  
ただ、少しハマった部分もあるのでそれは後述 (最新は3.0.1なんだけれどドキュメントが2.xのまま更新されていなかったりする  
あとスマホでのタスクの確認はRedmineではできなくて、RedminePMというアプリから行うことにしました

今回RedmineをインストールするOSにはRubyが入っていないのでRedmine用のユーザを用意して  
ホームディレクトリにrbenvをインストール、rbenvを使ってRubyをインストール、Redmineをインストール  
と、全て専用ユーザのホームディレクトリ以下で済ますことにしました  
また、追加でインストールするものも抑えたかったのでRedmineはWEBRick、SQLite、ImageMagickなし、で動かすことにしました

まずユーザを作って、ログイン

    :::bash
    # useradd -m redmine
    # su - redmine

[rbenv](https://github.com/sstephenson/rbenv) と [ruby-build](https://github.com/sstephenson/ruby-build) をインストールする  
ここからは全てこのユーザのホームディレクトリ以下で作業

* [rbenvおよびbundlerの基本的な使用方法](https://www.qoosky.net/references/128/)  
* [Rails開発環境の構築（rbenvでRuby導入からBundler、Rails導入まで）](http://qiita.com/emadurandal/items/a60886152a4c99ce1017)

rbenvとruby-buildをclone

    :::bash
    $ git clone https://github.com/sstephenson/rbenv.git .rbenv
    $ git clone https://github.com/sstephenson/ruby-build.git .rbenv/plugins/ruby-build

rbenvの設定を.bashrcに追加

    :::bash
    $ echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >>.bashrc
    $ echo 'eval "$(rbenv init -)"' >>.bashrc
    $ source .bashrc

rbenvでrubyとbundlerをインストールする  
`rbenv install -l` でインストール可能なRubyのバージョン、 `rbenv versions` でインストール済みを確認できる

    :::bash
    $ rbenv install -l
    ...
      2.2.0-rc1
      2.2.0
      2.2.1
      2.3.0-dev
    ...
    $ rbenv install 2.2.1
    $ rbenv versions
      2.2.1
    $ rbenv global 2.2.1
    $ rbenv exec gem install bundler --no-rdoc --no-ri
    $ rbenv rehash

Redmineをインストールする

* [Redmine 3.0をCentOS 7.0にインストールする手順](http://blog.redmine.jp/articles/3_0/installation_centos/)
* [Redmineのインストール](http://redmine.jp/guide/RedmineInstall/)
* [Installing Redmine](http://www.redmine.org/projects/redmine/wiki/redmineinstall)

Redmineをclone (最新のバージョンは3.0なので、ブランチを切り替え)

    :::bash
    $ git clone https://github.com/redmine/redmine.git
    $ cd redmine
    $ git checkout 3.0-stable
    $ cp config/database.yml.example config/database.yml
    $ cp config/configuration.yml.example config/configuration.yml

`config/database.yml` は以下のSQLiteの部分以外すべてコメントアウト  
`config/configuration.yml` には本来メールサーバ等の設定が必要だけれど今回は必要ないので特に編集はしない

    :::
    # SQLite3 configuration example
    production:
      adapter: sqlite3
      database: db/redmine.sqlite3

RedmineがURLのサブディレクトリ以下に見えるようにインストールしたかったのでこれらを参考にした

* [Redmine 2.0 "No route matches"](http://www.redmine.org/boards/2/topics/30676?r=30881#message-30881)
* [Run Redmine in a sub directory results in "No route matches"](http://www.redmine.org/issues/11058)
* [FCGI mode does not support sub-URI](http://www.redmine.org/issues/11881#note-14)

`config/environment.rb` の末尾の部分がこのようになるように `default_scope` と `relative_url_root` を追加

    :::ruby
    RedmineApp::Application.routes.default_scope = { :path => '/redmine', :shallow_path => '/redmine' }
    # Initialize the Rails application
    Rails.application.initialize!
    Redmine::Utils::relative_url_root = "/redmine"

サブディレクトリにアクセスしてもpublicの中身が見えるようにリンクを作成

    :::bash
    $ ln -s . public/redmine

Redmineが依存するGemをインストール、各種初期データの生成

    :::bash
    $ bundle install --without development test rmagick --path vendor/bundle
    $ bundle exec rake generate_secret_token
    $ RAILS_ENV=production bundle exec rake db:migrate
    $ RAILS_ENV=production REDMINE_LANG=ja bundle exec rake redmine:load_default_data

ひと通りインストールが終わったので起動して [http://localhost:3000/redmine](http://localhost:3000/redmine) にアクセスしてみる

    :::bash
    $ ruby bin/rails server webrick -e production

* `bin/rails` を使う (2.x系と変わっているらしい
* デフォルトでは127.0.0.1にbindされるので別のマシンからアクセスしたい場合は `-b 192.168.1.1` オプションを使う
* デーモンとして起動させたい場合は `-d` オプションを使う

起動しなかったり、うまく動作していなさそうだったら `log/production.log` を確認する  
問題なさそうであれば `config/environments/production.rb` を編集してログレベルを下げる

    :::ruby
    config.log_level = :warn

前段のNginxに設定を追加して外からアクセスできるようにしておわり

    :::
    location /redmine {
            auth_basic "restricted - redmine";
            auth_basic_user_file /path/to/htpasswd/of/redmine;
            proxy_pass http://localhost:3000;
    }
