Title: 使えなくなったHDDのS.M.A.R.T.の結果
Date: 2014-11-03 21:31
Category: Computer
Tags: HDD
Slug: smart

ずいぶん前の出来事だけれど、 [Hitachi Deskstar 7K1000.D](http://www.hgst.com/tech/techlib.nsf/techdocs/C2AF1DCDF0FBD887882578FE0082527B/$file/DS7K1000.D_ds.pdf) がエラーを吐いて使えなくなったので  
その時のS.M.A.R.T.の結果を記録しておく

こんなメールでRAIDのアレイから外したことを通知されました

    :::
    This is an automatically generated mail message from mdadm
    
    A Fail event had been detected on md device /dev/md1.
    
    It could be related to component device /dev/sdc.
    
    Faithfully yours, etc.
    
    P.S. The /proc/mdstat file currently contains the following:
    
    Personalities : [raid1]
    md1 : active raid1 sdd[1] sdc[0](F)
          976762448 blocks super 1.0 [2/1] [_U]
    
    md0 : active raid1 sdb[2] sda[0]
          2930266448 blocks super 1.0 [2/2] [UU]
    
    unused devices: <none>

とりあえずRAIDは手元にあった古いディスクに差し替えて  
問題のHDDのS.M.A.R.T.を確認してみたらこんな感じでした

    :::bash
    # smartctl -a /dev/sdf
    smartctl 6.1 2013-03-16 r3800 [x86_64-linux-3.10.7-gentoo-r1] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
    
    === START OF INFORMATION SECTION ===
    Model Family:     Hitachi Deskstar 7K1000.D
    Device Model:     Hitachi HDS721010DLE630
    Serial Number:    XXXXXXXXXXXXXX
    LU WWN Device Id: 5 000cca 37cc0c0f2
    Firmware Version: MS2OA5N0
    User Capacity:    1,000,204,886,016 bytes [1.00 TB]
    Sector Sizes:     512 bytes logical, 4096 bytes physical
    Rotation Rate:    7200 rpm
    Device is:        In smartctl database [for details use: -P show]
    ATA Version is:   ATA8-ACS T13/1699-D revision 4
    SATA Version is:  SATA 2.6, 6.0 Gb/s (current: 1.5 Gb/s)
    Local Time is:    Wed Aug 13 11:23:08 2014 JST
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
    data collection:                ( 7410) seconds.
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
    recommended polling time:        ( 124) minutes.
    SCT capabilities:              (0x003d) SCT Status supported.
                                            SCT Error Recovery Control supported.
                                            SCT Feature Control supported.
                                            SCT Data Table supported.
    
    SMART Attributes Data Structure revision number: 16
    Vendor Specific SMART Attributes with Thresholds:
    ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
      1 Raw_Read_Error_Rate     0x000b   079   079   016    Pre-fail  Always       -       824
      2 Throughput_Performance  0x0005   141   141   054    Pre-fail  Offline      -       74
      3 Spin_Up_Time            0x0007   124   124   024    Pre-fail  Always       -       185 (Average 185)
      4 Start_Stop_Count        0x0012   100   100   000    Old_age   Always       -       966
      5 Reallocated_Sector_Ct   0x0033   100   100   005    Pre-fail  Always       -       62
      7 Seek_Error_Rate         0x000b   100   100   067    Pre-fail  Always       -       0
      8 Seek_Time_Performance   0x0005   130   130   020    Pre-fail  Offline      -       28
      9 Power_On_Hours          0x0012   099   099   000    Old_age   Always       -       11362
     10 Spin_Retry_Count        0x0013   100   100   060    Pre-fail  Always       -       0
     12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       71
    192 Power-Off_Retract_Count 0x0032   099   099   000    Old_age   Always       -       1247
    193 Load_Cycle_Count        0x0012   099   099   000    Old_age   Always       -       1247
    194 Temperature_Celsius     0x0002   171   171   000    Old_age   Always       -       35 (Min/Max 17/45)
    196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       110
    197 Current_Pending_Sector  0x0022   100   100   000    Old_age   Always       -       0
    198 Offline_Uncorrectable   0x0008   100   100   000    Old_age   Offline      -       0
    199 UDMA_CRC_Error_Count    0x000a   200   200   000    Old_age   Always       -       0
    
    SMART Error Log Version: 1
    No Errors Logged
    
    SMART Self-test log structure revision number 1
    Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
    # 1  Short offline       Completed without error       00%     11361         -
    # 2  Short offline       Completed without error       00%     11319         -
    # 3  Short offline       Completed without error       00%     11228         -
    # 4  Short offline       Completed without error       00%     10769         -
    # 5  Short offline       Completed without error       00%     10702         -
    # 6  Short offline       Completed without error       00%     10702         -
    # 7  Short offline       Completed without error       00%     10446         -
    # 8  Short offline       Completed without error       00%      9861         -
    # 9  Short offline       Completed without error       00%      9817         -
    #10  Short offline       Completed without error       00%      9492         -
    #11  Short offline       Completed without error       00%      9431         -
    #12  Short offline       Completed without error       00%      8981         -
    #13  Short offline       Completed without error       00%         1         -
    
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

OS側からエラーだからといって外されるのにS.M.A.R.T.では検出されないのね…
