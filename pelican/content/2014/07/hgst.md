Title: HGST 0S03361買いました
Date: 2014-07-20 20:30
Category: Computer
Tags: HDD, Linux, RAID, LVM
Slug: hgst

おみくじと話題(?)のHGST 0S03361、ドスパラで15960円でした  
RAIDを組むので2つ買ってきたところどちらもALEでした

MicroServerのスロットは4つとも埋まっていて3TBx2と1TBx2の  
2つのRAID1のアレイをLVMで1つの領域に束ねています  
今回は1TBのアレイを交換したいのでこのアレイを縮退状態にして  
スロットを1つ空けてから4TBのHDDを挿しました  
このHDDで新規に縮退状態のアレイを作成してLVMに追加します  
その後1TBのアレイをLVMから取り外してスロットからも取り外し、  
空いたスロットに2つ目の4TBのHDDを挿して新規に作成したアレイを  
縮退状態から復帰させます

まず1TBのアレイを縮退状態にして1つ取り外します

    :::bash
    $ sudo mdadm --manage /dev/md1 --fail /dev/sdd
    $ sudo mdadm --manage /dev/md1 --remove /dev/sdd
    $ cat /proc/mdstat
    Personalities : [raid1] 
    md1 : active raid1 sdc[2]
          976762448 blocks super 1.0 [2/1] [U_]
          
    md0 : active raid1 sdb[2] sda[0]
          2930266448 blocks super 1.0 [2/2] [UU]
          
    unused devices: <none>

mdadmコマンドでsddをRAIDアレイから取り外します  
このあと一度電源を落としてsddのHDDを挿し替えました  
新しいHDDはRAIDアレイのメンバではないので起動後も縮退状態のままになっています  
早く正常な状態に戻したいですね(震え声…  
この状態でhdparm等のコマンドを実行してみました

    :::bash
    $ sudo hdparm -itT /dev/sdd
    Password: 
    
    /dev/sdd:
    
     Model=HGST HMS5C4040ALE640, FwRev=MPAOA580, SerialNo=xxxxxxxxxxxxxx
     Config={ HardSect NotMFM HdSw>15uSec Fixed DTR>10Mbs }
     RawCHS=16383/16/63, TrkSize=0, SectSize=0, ECCbytes=56
     BuffType=DualPortCache, BuffSize=unknown, MaxMultSect=16, MultSect=off
     CurCHS=16383/16/63, CurSects=16514064, LBA=yes, LBAsects=7814037168
     IORDY=on/off, tPIO={min:120,w/IORDY:120}, tDMA={min:120,rec:120}
     PIO modes:  pio0 pio1 pio2 pio3 pio4 
     DMA modes:  mdma0 mdma1 mdma2 
     UDMA modes: udma0 udma1 udma2 udma3 udma4 udma5 *udma6 
     AdvancedPM=yes: disabled (255) WriteCache=disabled
     Drive conforms to: unknown:  ATA/ATAPI-2,3,4,5,6,7
    
     * signifies the current active mode
    
     Timing cached reads:   2472 MB in  2.00 seconds = 1235.36 MB/sec
     Timing buffered disk reads: 410 MB in  3.00 seconds = 136.50 MB/sec

smartctlの値はこんな感じ

    :::bash
    $ sudo smartctl -a /dev/sdd
    Password: 
    smartctl 6.1 2013-03-16 r3800 [x86_64-linux-3.10.7-gentoo-r1] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
    
    === START OF INFORMATION SECTION ===
    Device Model:     HGST HMS5C4040ALE640
    Serial Number:    xxxxxxxxxxxxxx
    LU WWN Device Id: 5 000cca 22eca57e1
    Firmware Version: MPAOA580
    User Capacity:    4,000,787,030,016 bytes [4.00 TB]
    Sector Sizes:     512 bytes logical, 4096 bytes physical
    Rotation Rate:    5700 rpm
    Device is:        Not in smartctl database [for details use: -P showall]
    ATA Version is:   ATA8-ACS T13/1699-D revision 4
    SATA Version is:  SATA 3.0, 6.0 Gb/s (current: 3.0 Gb/s)
    Local Time is:    Sun Jul 20 20:44:15 2014 JST
    SMART support is: Available - device has SMART capability.
    SMART support is: Enabled
    
    === START OF READ SMART DATA SECTION ===
    SMART overall-health self-assessment test result: PASSED
    
    General SMART Values:
    Offline data collection status:  (0x80) Offline data collection activity
                                            was never started.
                                            Auto Offline Data Collection: Enabled.
    Self-test execution status:      (   0) The previous self-test routine completed
                                            without error or no self-test has ever 
                                            been run.
    Total time to complete Offline 
    data collection:                (   28) seconds.
    Offline data collection
    capabilities:                    (0x5b) SMART execute Offline immediate.
                                            Auto Offline data collection on/off support.
                                            Suspend Offline collection upon new
                                            command.
                                            Offline surface scan supported.
                                            Self-test supported.
                                            No Conveyance Self-test supported.
                                            Selective Self-test supported.
    SMART capabilities:            (0x0003) Saves SMART data before entering
                                            power-saving mode.
                                            Supports SMART auto save timer.
    Error logging capability:        (0x01) Error logging supported.
                                            General Purpose Logging supported.
    Short self-test routine 
    recommended polling time:        (   1) minutes.
    Extended self-test routine
    recommended polling time:        ( 705) minutes.
    SCT capabilities:              (0x003d) SCT Status supported.
                                            SCT Error Recovery Control supported.
                                            SCT Feature Control supported.
                                            SCT Data Table supported.
    
    SMART Attributes Data Structure revision number: 16
    Vendor Specific SMART Attributes with Thresholds:
    ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
      1 Raw_Read_Error_Rate     0x000b   100   100   016    Pre-fail  Always       -       0
      2 Throughput_Performance  0x0005   100   100   054    Pre-fail  Offline      -       0
      3 Spin_Up_Time            0x0007   100   100   024    Pre-fail  Always       -       0
      4 Start_Stop_Count        0x0012   100   100   000    Old_age   Always       -       3
      5 Reallocated_Sector_Ct   0x0033   100   100   005    Pre-fail  Always       -       0
      7 Seek_Error_Rate         0x000b   100   100   067    Pre-fail  Always       -       0
      8 Seek_Time_Performance   0x0005   100   100   020    Pre-fail  Offline      -       0
      9 Power_On_Hours          0x0012   100   100   000    Old_age   Always       -       0
     10 Spin_Retry_Count        0x0013   100   100   060    Pre-fail  Always       -       0
     12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       3
    192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       5
    193 Load_Cycle_Count        0x0012   100   100   000    Old_age   Always       -       5
    194 Temperature_Celsius     0x0002   176   176   000    Old_age   Always       -       34 (Min/Max 25/34)
    196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
    197 Current_Pending_Sector  0x0022   100   100   000    Old_age   Always       -       0
    198 Offline_Uncorrectable   0x0008   100   100   000    Old_age   Offline      -       0
    199 UDMA_CRC_Error_Count    0x000a   200   200   000    Old_age   Always       -       0
    
    SMART Error Log Version: 1
    No Errors Logged
    
    SMART Self-test log structure revision number 1
    Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
    # 1  Short offline       Completed without error       00%         0         -
    
    SMART Selective self-test log data structure revision number 1
     SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
        1        0        0  Not_testing
        2        0        0  Not_testing
        3        0        0  Not_testing
        4        0        0  Not_testing
        5        0        0  Not_testing
    Selective self-test flags (0x0):
      After scanning selected spans, do NOT read-scan remainder of disk.
    If Selective self-test is pending on power-up, resume after 0 minute delay.

0で埋めた結果はこれ

    :::bash
    $ time sudo dd if=/dev/zero of=/dev/sdd bs=5M
    763088+3 records in
    763087+3 records out
    4000787030016 bytes (4.0 TB) copied, 38047.6 s, 105 MB/s
    
    real    634m9.277s
    user    0m5.266s
    sys     147m9.377s

とりあえずチェックは以上  
あとはこのHDDを使って縮退状態のアレイを作成します

    :::bash
    $ sudo mdadm --create /dev/md/2 --metadata 1.0 --level=raid1 --raid-devices=2 /dev/sdd missing
    mdadm: array /dev/md/2 started.
    
    $ cat /proc/mdstat 
    Personalities : [raid1] 
    md2 : active raid1 sdd[0]
          3907018432 blocks super 1.0 [2/1] [U_]
          
    md1 : active raid1 sdc[2]
          976762448 blocks super 1.0 [2/1] [U_]
          
    md0 : active raid1 sdb[2] sda[0]
          2930266448 blocks super 1.0 [2/2] [UU]
          
    unused devices: <none>

作成できました  
忘れずに新しいアレイの情報を/etc/mdadm.confに追記しておきます

    :::bash
    $ sudo sh -c "mdadm --detail --scan | grep /dev/md/2 >>/etc/mdadm.conf"

このRAIDアレイをLVMに追加できるようにPVを作成します

    :::bash
    $ sudo pvcreate --metadatatype 2 --dataalignment 64K /dev/md2
      Physical volume "/dev/md2" successfully created
    
    $ sudo pvdisplay /dev/md2
      "/dev/md2" is a new physical volume of "3.64 TiB"
      --- NEW Physical volume ---
      PV Name               /dev/md2
      VG Name               
      PV Size               3.64 TiB
      Allocatable           NO
      PE Size               0   
      Total PE              0
      Free PE               0
      Allocated PE          0
      PV UUID               FAqA95-B5nh-2cCe-bhqr-08Fl-pLmH-B37gYg

PVを作成したら既存のVGに追加します

    :::bash
    $ sudo vgextend vg0 /dev/md2                                                           
      Volume group "vg0" successfully extended
    
    $ sudo pvdisplay /dev/md2                                                              
      --- Physical volume ---
      PV Name               /dev/md2
      VG Name               vg0
      PV Size               3.64 TiB / not usable 23.69 MiB
      Allocatable           yes 
      PE Size               128.00 MiB
      Total PE              29808
      Free PE               29808
      Allocated PE          0
      PV UUID               FAqA95-B5nh-2cCe-bhqr-08Fl-pLmH-B37gYg

1TBのHDDからPEを移動する (今回追加したHDDに余裕があるのでそっちに移動するはず)  
6時間くらいかかりました、Allocated PEが0になっています

    :::bash
    $ sudo pvmove /dev/md1 
    Password: 
      /dev/md1: Moved: 0.0%
      ...
      /dev/md1: Moved: 100.0%

    $ sudo pvdisplay /dev/md1 
    Password: 
      --- Physical volume ---
      PV Name               /dev/md1
      VG Name               vg0
      PV Size               931.51 GiB / not usable 13.58 MiB
      Allocatable           yes 
      PE Size               128.00 MiB
      Total PE              7452
      Free PE               7452
      Allocated PE          0
      PV UUID               wrcffi-LQoQ-ctKc-ewxQ-X0Qg-JX3Y-AsqoRX

これでようやくこのアレイをLVMから切り離すことができます  
以下のコマンドで切り離して、VG Nameが空になっていることがわかります

    :::bash
    $ sudo vgreduce vg0 /dev/md1
      Removed "/dev/md1" from volume group "vg0"

    $ sudo pvdisplay /dev/md1 
      "/dev/md1" is a new physical volume of "931.51 GiB"
      --- NEW Physical volume ---
      PV Name               /dev/md1
      VG Name               
      PV Size               931.51 GiB
      Allocatable           NO
      PE Size               0   
      Total PE              0
      Free PE               0
      Allocated PE          0
      PV UUID               wrcffi-LQoQ-ctKc-ewxQ-X0Qg-JX3Y-AsqoRX

LVMから切り離したので今後md1は使用しません  
RAIDアレイを停止して、スーパーブロックも消去  
/etc/mdadm.confからもエントリを削除します

    :::bash
    $ sudo mdadm -S /dev/md1
    mdadm: stopped /dev/md1

    $ cat /proc/mdstat                                                                     
    Personalities : [raid1] 
    md2 : active raid1 sdd[0]
          3907018432 blocks super 1.0 [2/1] [U_]
          
    md0 : active raid1 sdb[2] sda[0]
          2930266448 blocks super 1.0 [2/2] [UU]
          
    unused devices: <none>

    $ sudo mdadm --zero-superblock /dev/sdc

    $ sudo vi /etc/mdadm.conf

この状態で一度電源を落として1TBのHDDを抜き、4TBに差し替えます  
今度はbs=10Mで実行してみた結果

    :::bash
    $ time sudo dd if=/dev/zero of=/dev/sdd bs=5M
    381545+0 records in
    381544+0 records out
    4000787030016 bytes (4.0 TB) copied, 37510.9 s, 107 MB/s
    
    real    625m10.977s
    user    0m3.075s
    sys     139m55.362s

新しく挿したHDDをRAIDのメンバに追加します  
これで今回作成したRAIDが縮退状態から回復します  
(ちなみにddと同じくらい時間かかりました)

    :::bash
    $ sudo mdadm /dev/md2 -a /dev/sdc
    mdadm: added /dev/sdc

    $ cat /proc/mdstat 
    Personalities : [raid1] 
    md2 : active raid1 sdc[2] sdd[0]
          3907018432 blocks super 1.0 [2/1] [U_]
          [>....................]  recovery =  0.0% (189504/3907018432) finish=687.1min speed=94752K/sec
          
    md0 : active raid1 sda[0] sdb[2]
          2930266448 blocks super 1.0 [2/2] [UU]
          
    unused devices: <none>

Free PEの値を指定して、今回追加したアレイ全体を使用するようにLVを拡張します

    :::bash
    $ sudo lvextend -L +2861568 /dev/vg0/lv0
      Extending logical volume lv0 to 6.37 TiB
      Logical volume lv0 successfully resized

    $ sudo pvdisplay /dev/md2
      --- Physical volume ---
      PV Name               /dev/md2
      VG Name               vg0
      PV Size               3.64 TiB / not usable 23.69 MiB
      Allocatable           yes (but full)
      PE Size               128.00 MiB
      Total PE              29808
      Free PE               0
      Allocated PE          29808
      PV UUID               FAqA95-B5nh-2cCe-bhqr-08Fl-pLmH-B37gYg

最後にファイルシステムを拡張します

    :::bash
    $ df -h /mnt/lvm/
    Filesystem           Size  Used Avail Use% Mounted on
    /dev/mapper/vg0-lv0  3.6T  2.9T  578G  84% /mnt/lvm
    
    $ sudo resize2fs /dev/mapper/vg0-lv0 
    Password: 
    resize2fs 1.42.7 (21-Jan-2013)
    Filesystem at /dev/mapper/vg0-lv0 is mounted on /mnt/lvm; on-line resizing required
    old_desc_blocks = 233, new_desc_blocks = 408
    The filesystem on /dev/mapper/vg0-lv0 is now 1709309952 blocks long.
    
    $ df -h /mnt/lvm/
    Filesystem           Size  Used Avail Use% Mounted on
    /dev/mapper/vg0-lv0  6.3T  2.9T  3.2T  48% /mnt/lvm
