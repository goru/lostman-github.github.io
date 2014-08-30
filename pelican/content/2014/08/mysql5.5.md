Title: MySQL5.1から5.5へアップデート
Date: 2014-08-31 03:32
Category: Computer
Tags: MySQL, Linux, Gentoo
Slug: mysql5.5

GentooからMySQL5.5がStableになったし5.1はmaskするよ、というお知らせが来ていました  
epgrecとMediatombで使っているのですが5.5でも問題なさそうなのでアップデートしました

    ::
    2014-08-20-mysql_5_5_upgrade_procedures
      Title                     MySQL 5.5 upgrade procedures
      Author                    Brian Evans <grknight@gentoo.org>
      Posted                    2014-08-20
      Revision                  1
    
    MySQL 5.5 is now stable across all arches. The upgrade process
    will require you to rebuild everything linked to
    libmysqlclient.so.16 and libmysqlclient_r.so.16.
    
    This may be done for you by portage with 'emerge @preserved-rebuild'.
    
    A small number of libraries may not be automatically rebuilt against
    the new MySQL libraries using preserved-rebuild.  If you have
    difficulties with packages not finding the new libraries, install
    app-portage/gentoolkit and run:
    # revdep-rebuild --library libmysqlclient.so.16
    # revdep-rebuild --library libmysqlclient_r.so.16
    
    The official upgrade documentation is available here:
    http://dev.mysql.com/doc/refman/5.5/en/upgrading.html
    
    Please be sure to review the upgrade document for any possible actions
    necessary before and after the upgrade. This includes running
    mysql_upgrade after the upgrade completion.
    
    Due to security flaws, MySQL 5.1 will be hard masked in 30 days after
    this news item is posted.  It will remain masked in the tree for
    3 months before removal.

1. MySQLの停止

        ::bash
        # /etc/init.d/mysql stop

1. emergeを使用してアップデート

        ::bash
        # emerge -uav mysql
        # etc-update

1. InnoDBが有効になっているとepgrecが遅くなるみたいなので設定を変更する [*](http://sarami.pv.s-labo.com/blog/zatta/?p=221)  
`/etc/mysql/my.cnf` に以下の二行を追加

        ::
        skip-innodb
        default-storage-engine=MyISAM

1. 関連パッケージの更新

        ::bash
        # emerge @preserved-rebuild -a
        # revdep-rebuild --library libmysqlclient.so.16
        # revdep-rebuild --library libmysqlclient_r.so.16

1. MySQLを再起動  
再起動すると `/var/log/mysql/mysqld.err` に以下のようなエラーが出力されて  
`mysql_upgrade` を実行するように指示されます [*](http://server-setting.info/centos/mysql5-1_mysql5-5_upgrade.html)

        ::bash
        # /etc/init.d/mysql start
        # tail /var/log/mysql/mysqld.err
        140830 20:53:41 [ERROR] Missing system table mysql.proxies_priv; please run mysql_upgrade to create it
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'events_waits_current' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'events_waits_history' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'events_waits_history_long' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'setup_consumers' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'setup_instruments' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'setup_timers' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'performance_timers' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'threads' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'events_waits_summary_by_thread_by_event_name' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'events_waits_summary_by_instance' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'events_waits_summary_global_by_event_name' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'file_summary_by_event_name' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'file_summary_by_instance' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'mutex_instances' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'rwlock_instances' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'cond_instances' has the wrong structure
        140830 20:53:41 [ERROR] Native table 'performance_schema'.'file_instances' has the wrong structure
        140830 20:53:41 [Note] Event Scheduler: Loaded 0 events

1. DBの更新と再度MySQLを再起動  
再起動後にログを確認してエラーがでていなければ完了

        ::bash
        # mysql_upgrade -u root -p
        # /etc/init.d/mysql restart
