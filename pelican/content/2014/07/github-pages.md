Title: GitHub Pages関連で調べたこと
Date: 2014-07-24 00:16
Category: Internet
Tags: GitHub
Slug: github-pages

* [Adding a CNAME file to your repository](https://help.github.com/articles/adding-a-cname-file-to-your-repository)  
  サブドメインを使用する場合はリポジトリに割り当てたいサブドメインを書いた `CNAME` ファイルを追加するのと、  
  使用しているDNSの設定でサブドメインと `hoge.github.io` をCNAMEで関連付ける
* [Using submodules with Pages](https://help.github.com/articles/using-submodules-with-pages)  
  gitのsubmoduleを使用する場合、リポジトリのURLは `git://` でなく `https://` を使用しなければいけない
* [Turning Jekyll off](https://help.github.com/articles/using-jekyll-with-pages#turning-jekyll-off)  
  デフォルトでJekyllが有効になっているので `*.rst` なファイルをアップロードすると変換しようとする  
  これを無効にするために `.nojekyll` をリポジトリのルートに作成する
