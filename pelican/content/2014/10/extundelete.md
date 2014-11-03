Title: 操作ミスでファイルを消してしまった時の復活方法
Date: 2014-10-23 01:00
Category: Computer
Tags: Linux
Slug: extundelete

ファイルサーバのデータを整理中に `rm *hoge*` と入力しようとして `rm *` まで入力した状態で  
hogeをコピペで貼り付けようとしました  
この時hogeの先頭に改行が含まれていたため、 `rm *` が実行されてしまい  
カレントディレクトリ内のファイルを全て削除してしまいました、事故です  
このような場合、 [extundelete](http://extundelete.sourceforge.net/) というソフトを使うと復活できるみたいなので、試してみました

まず削除してしまったファイルがあるボリュームをroでマウントしなおします  
この作業はできるだけ早く行う必要があります  
自分の場合、別のプロセスがこのボリュームに書き込みをしていたので  
削除したファイルのinodeが再利用されてしまいかなりのファイルを失いました

    :::bash
    # mount -o remount,ro /mnt/lvm

次にdateコマンドで操作ミスが発生した時刻の確認をします

    :::bash
    $ date +%s
    1413993600

extundeleteで復活させます  
復活できなかったファイルが以下のようにログに出力されて  
復活できたファイルはカレントディレクトリの `RECOVERED_FILES` 以下に出力されます

    :::bash
    # extundelete --restore-all --after 1413993600 /dev/mapper/vg0-lv0
    Only show and process deleted entries if they are deleted on or after 1413993600 and before 9223372036854775807.
    NOTICE: Extended attributes are not restored.
    Loading filesystem metadata ... 52164 groups loaded.
    Loading journal descriptors ... 26255 descriptors loaded.
    Searching for recoverable inodes in directory / ...
    160 recoverable inodes found.
    Looking through the directory structure for deleted files ...
    Unable to restore inode 224265493 (/path/to/deleted/file): Space has been reallocated.
    Unable to restore inode 224265494 (/path/to/deleted/file): Space has been reallocated.
    Unable to restore inode 224265503 (/path/to/deleted/file): Space has been reallocated.
    ...
    Unable to restore inode 91544629 (/path/to/deleted/file): No undeleted copies found in the journal.
    Unable to restore inode 91544798 (/path/to/deleted/file): No undeleted copies found in the journal.
    Unable to restore inode 91544633 (/path/to/deleted/file): No undeleted copies found in the journal.
    ...
    30 recoverable inodes still lost.
    Unable to restore inode 99378493 (file.99378493): No undeleted copies found in the journal.
    Unable to restore inode 99379721 (file.99379721): No undeleted copies found in the journal.
    Unable to restore inode 99379967 (file.99379967): No undeleted copies found in the journal.
    ...

オペミス怖いですね…  
とりあえず `rm` は `rm -i` のエイリアスにしておこうかと思います
