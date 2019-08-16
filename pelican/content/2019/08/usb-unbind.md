Title: USBデバイスを接続したまま取り外した状態にしたい
Date: 2019-08-17 02:22
Category: Computer
Tags: Linux, Kindle
Slug: usb-unbind

KindleをPCに接続すると自動的に `USBドライブモード` に切り替わってしまい、充電しながらの操作ができなくなる。
Windowsでは `ハードウェアの取り外し` 的な操作をすればいいのだけれど、それってLinux(CLI)でどうやるの?というお話。

まず接続した状態でdmesgを確認する。

    :::
    $ dmesg
    [1483324.916878] usb 3-2.1: new high-speed USB device number 79 using xhci_hcd
    [1483325.003399] usb 3-2.1: New USB device found, idVendor=1949, idProduct=0324
    [1483325.003405] usb 3-2.1: New USB device strings: Mfr=0, Product=4, SerialNumber=5
    [1483325.003409] usb 3-2.1: Product: Internal Storage
    [1483325.003412] usb 3-2.1: SerialNumber: XXXXXXXXXXXXXXXX
    [1483325.004173] usb-storage 3-2.1:1.0: USB Mass Storage device detected
    [1483325.004664] scsi host14: usb-storage 3-2.1:1.0
    [1483326.005526] scsi 14:0:0:0: Direct-Access     Kindle   Internal Storage 0401 PQ: 0 ANSI: 2
    [1483326.005886] sd 14:0:0:0: Attached scsi generic sg2 type 0
    [1483326.008649] sd 14:0:0:0: [sdc] Attached SCSI removable disk
    [1483328.145867] sd 14:0:0:0: [sdc] 57319341 512-byte logical blocks: (29.3 GB/27.3 GiB)
    [1483328.365616] sd 14:0:0:0: [sdc] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
    [1483328.586605]  sdc:

ついでにlsusbも確認すると

    :::
    $ lsusb -t
    /:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/4p, 5000M
        |__ Port 2: Dev 2, If 0, Class=Hub, Driver=hub/4p, 5000M
    /:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/4p, 480M
        |__ Port 1: Dev 75, If 0, Class=Hub, Driver=hub/3p, 480M
            |__ Port 1: Dev 76, If 0, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 3: Dev 77, If 0, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 3: Dev 77, If 1, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 3: Dev 77, If 2, Class=Human Interface Device, Driver=usbhid, 12M
        |__ Port 2: Dev 3, If 0, Class=Hub, Driver=hub/4p, 480M
            |__ Port 1: Dev 79, If 0, Class=Mass Storage, Driver=usb-storage, 480M
    /:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
        |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/8p, 480M
    /:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
        |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/6p, 480M

こんな感じの出力が得られて、お目当てのデバイスは `3-2.1` というバス&ポートに接続されていることがわかる。
この識別子を `/sys/bus/usb/drivers/usb/unbind` へ書き込むと切断することができる。

    :::
    $ sudo sh -c "echo -n 3-2.1 >/sys/bus/usb/drivers/usb/unbind"

dmesgにはあまりログはでないが

    :::
    $ dmesg
    [1483346.910295] sd 14:0:0:0: [sdc] Synchronizing SCSI cache

lsusbからは消えていることが確認できる

    :::
    $ lsusb -t
    /:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/4p, 5000M
        |__ Port 2: Dev 2, If 0, Class=Hub, Driver=hub/4p, 5000M
    /:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/4p, 480M
        |__ Port 1: Dev 75, If 0, Class=Hub, Driver=hub/3p, 480M
            |__ Port 1: Dev 76, If 0, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 3: Dev 77, If 0, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 3: Dev 77, If 1, Class=Human Interface Device, Driver=usbhid, 12M
            |__ Port 3: Dev 77, If 2, Class=Human Interface Device, Driver=usbhid, 12M
        |__ Port 2: Dev 3, If 0, Class=Hub, Driver=hub/4p, 480M
    /:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
        |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/8p, 480M
    /:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
        |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/6p, 480M

同じように `/sys/bus/usb/drivers/usb/bind` へ書き込むと再認識させることもできる。

    :::
    $ sudo sh -c "echo -n 3-2.1 >/sys/bus/usb/drivers/usb/bind"
