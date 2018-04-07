Title: RaspberryPiでffmpegをビルドしてハードウェアデコーダ/エンコーダを試す
Date: 2018-04-08 01:22
Category: Computer
Tags: Linux, RaspberryPi
Slug: raspberrypi-ffmpeg

RaspberryPiでffmpegのMPEG2のハードウェアデコーダ(mpeg2_mmal)と、H.264のハードウェアエンコーダ(h264_omx)を使ってみたかったので試してみました。
が、aptでインストールできる3.2.10でmpeg2_mmalを使ってデコードすると解像度が320x240に固定されてしまうというバグを
見事に踏み抜いてしまったので結局自分でビルドすることになりました。

3.2.10で [ERBラボのサンプルストリーム パケットサイズ188バイト版](https://www.erb.jp/labo/samplestream.html) をエンコードしたログ

    :::
    $ time ffmpeg -fflags +discardcorrupt -c:v mpeg2_mmal -i isdbt188.ts -t 00:00:10 -c:a copy -bsf:a aac_adtstoasc -c:v h264_omx -b:v 4096k isdbt188.mp4
    ffmpeg version 3.2.10-1~deb9u1+rpt1 Copyright (c) 2000-2018 the FFmpeg developers
      built with gcc 6.3.0 (Raspbian 6.3.0-18+rpi1) 20170516
      configuration: --prefix=/usr --extra-version='1~deb9u1+rpt1' --toolchain=hardened --libdir=/usr/lib/arm-linux-gnueabihf --incdir=/usr/include/arm-linux-gnueabihf --enable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libebur128 --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libmp3lame --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx-rpi --enable-mmal --enable-openal --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
      libavutil      55. 34.101 / 55. 34.101
      libavcodec     57. 64.101 / 57. 64.101
      libavformat    57. 56.101 / 57. 56.101
      libavdevice    57.  1.100 / 57.  1.100
      libavfilter     6. 65.100 /  6. 65.100
      libavresample   3.  1.  0 /  3.  1.  0
      libswscale      4.  2.100 /  4.  2.100
      libswresample   2.  3.100 /  2.  3.100
      libpostproc    54.  1.100 / 54.  1.100
    [mpegts @ 0x2450660] PES packet size mismatch
    [mpegts @ 0x2450660] Dropped corrupted packet (stream = 1)
    Input #0, mpegts, from 'isdbt188.ts':
      Duration: 00:01:00.87, start: 109.851700, bitrate: 17304 kb/s
      Program 23664
        Metadata:
          service_name    : ?ERB?|
          service_provider:
        Stream #0:0[0x200]: Video: mpeg2video ([2][0][0][0] / 0x0002), yuv420p(top first), 320x240, 16712 kb/s, 29.97 fps, 29.97 tbr, 90k tbn, 59.94 tbc
        Stream #0:1[0x201]: Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 186 kb/s
    [h264_omx @ 0x2456f00] Using OMX.broadcom.video_encode
    Output #0, mp4, to 'isdbt188.mp4':
      Metadata:
        encoder         : Lavf57.56.101
        Stream #0:0: Video: h264 (h264_omx) ([33][0][0][0] / 0x0021), yuv420p, 320x240, q=2-31, 4096 kb/s, 29.97 fps, 30k tbn, 29.97 tbc
        Metadata:
          encoder         : Lavc57.64.101 h264_omx
        Stream #0:1: Audio: aac (LC) ([64][0][0][0] / 0x0040), 48000 Hz, stereo, 186 kb/s
    Stream mapping:
      Stream #0:0 -> #0:0 (mpeg2video (mpeg2_mmal) -> h264 (h264_omx))
      Stream #0:1 -> #0:1 (copy)
    Press [q] to stop, [?] for help
    [mpeg2_mmal @ 0x2455fe0] Changing output format.
    Input stream #0:0 frame changed from size:320x240 fmt:yuv420p to size:1440x1080 fmt:yuv420p
    frame=  300 fps= 33 q=-0.0 Lsize=    3553kB time=00:00:09.98 bitrate=2915.2kbits/s dup=11 drop=0 speed=1.09x
    video:3321kB audio:222kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.274571%
    
    real    0m9.823s
    user    0m9.022s
    sys     0m0.769s

n3.4.2でのログ

    :::
    $ time LD_LIBRARY_PATH=/home/pi/usr/local/lib/ ~/usr/local/bin/ffmpeg -fflags +discardcorrupt -c:v mpeg2_mmal -i isdbt188.ts -t 00:00:10 -c:a copy -bsf:a aac_adtstoasc -c:v h264_omx -b:v 4096k isdbt188.mp4
    ffmpeg version n3.4.2-1~deb9u1+rpt1 Copyright (c) 2000-2018 the FFmpeg developers
      built with gcc 6.3.0 (Raspbian 6.3.0-18+rpi1+deb9u1) 20170516
      configuration: --prefix=/home/pi/usr/local --extra-version='1~deb9u1+rpt1' --toolchain=hardened --enable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libmp3lame --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx-rpi --enable-mmal --enable-openal --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
      libavutil      55. 78.100 / 55. 78.100
      libavcodec     57.107.100 / 57.107.100
      libavformat    57. 83.100 / 57. 83.100
      libavdevice    57. 10.100 / 57. 10.100
      libavfilter     6.107.100 /  6.107.100
      libavresample   3.  7.  0 /  3.  7.  0
      libswscale      4.  8.100 /  4.  8.100
      libswresample   2.  9.100 /  2.  9.100
      libpostproc    54.  7.100 / 54.  7.100
    [mpegts @ 0x17bee10] PES packet size mismatch
    [mpegts @ 0x17bee10] Dropped corrupted packet (stream = 1)
    Input #0, mpegts, from 'isdbt188.ts':
      Duration: 00:01:00.87, start: 109.851700, bitrate: 17304 kb/s
      Program 23664
        Metadata:
          service_name    : ?ERB?|
          service_provider:
        Stream #0:0[0x200]: Video: mpeg2video ([2][0][0][0] / 0x0002), yuv420p(top first), 320x240, 16712 kb/s, 29.97 fps, 29.97 tbr, 90k tbn, 59.94 tbc
        Stream #0:1[0x201]: Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 186 kb/s
    Stream mapping:
      Stream #0:0 -> #0:0 (mpeg2video (mpeg2_mmal) -> h264 (h264_omx))
      Stream #0:1 -> #0:1 (copy)
    Press [q] to stop, [?] for help
    [mpeg2_mmal @ 0x17c47e0] Changing output format.
    [h264_omx @ 0x1945960] Using OMX.broadcom.video_encode
    Output #0, mp4, to 'isdbt188.mp4':
      Metadata:
        encoder         : Lavf57.83.100
        Stream #0:0: Video: h264 (h264_omx) (avc1 / 0x31637661), yuv420p, 1440x1080 [SAR 4:3 DAR 16:9], q=2-31, 4096 kb/s, 29.97 fps, 30k tbn, 29.97 tbc
        Metadata:
          encoder         : Lavc57.107.100 h264_omx
        Stream #0:1: Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 186 kb/s
    frame=  300 fps= 30 q=-0.0 Lsize=    5404kB time=00:00:09.98 bitrate=4433.7kbits/s dup=11 drop=0 speed=0.989x
    video:5171kB audio:222kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.181688%
    
    real    0m10.665s
    user    0m2.694s
    sys     0m3.117s

どちらも縮小はしていないのですが、 `Output` の `Stream #0:0` を見ると3.2.10では `320x240` になっているのに対し、n3.4.2では正しく `1440x1080` になっています。
実際に出力されたファイルを再生してみてもその通りの解像度になっていました。
よくよくログを見るとほぼ同じながら `[mpeg2_mmal @ 0x2455fe0] Changing output format.` の位置が前後していて、3.2.10では出力のフォーマットを決定したあとに出力されています。
細かい原因は探っていませんが、3.2.10ではそのあたりに問題がありn3.4.2では解消されているようです。

ビルドとは直接関係ありませんが、mpeg2_mmalを使うにはライセンスが必要なので、 [公式](http://www.raspberrypi.com/mpeg-2-license-key/) で購入して設定します。
`/boot/config.txt` を編集するのと、 `raspi-config` で `5 Interfacing Options` -> `P1 Camera` を選択してカメラ機能を有効にする必要がありました。
再起動して `vcgencmd codec_enabled MPG2` を実行して `MPG2=enabled` と出力されれば有効になっています。
(ちなみにaptでインストールされるffmpegでもmpeg2_mmalとh264_omxがサポートされた状態でビルドされています。
h264_omxに関しては問題なかったので、MPEG2のデコーダを必要としないなら自分でビルドする必要はありません。)

ビルドの手順に関しては [KaoriYaさんの記事](https://www.kaoriya.net/blog/2017/10/07/) にそって進めるのが楽でした。
`/etc/apt/sources.list` を編集して `sudo apt install ffmpeg` と `sudo apt build-dep ffmpeg` を実行するまでは同じでOKです。

今回任意のバージョンを色々試したかったのでgitでソースを取得しました。

    :::
    $ sudo apt install git
    $ git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
    $ cd ffmpeg
    $ git checkout n3.4.2

`./configure` も基本3.2.10のコピペで問題ありませんでした。
ただし `--enable-libebur128` が使えなくなっているので削除したのと、インストール先を変更するために `--prefix=/usr` を修正、
`--libdir=/usr/lib/arm-linux-gnueabihf` と `--incdir=/usr/include/arm-linux-gnueabihf` を削除して以下のようにしてビルドしました。

    :::
    $ ./configure --prefix=$HOME/usr/local --extra-version='1~deb9u1+rpt1' --toolchain=hardened --enable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libmp3lame --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx-rpi --enable-mmal --enable-openal --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
    $ make -j4
    $ make install

`~/usr/local/bin/ffmpeg` としてインストールされるのでこのようにすれば実行できます。
(もちろん上書きしていないので単純にffmpegと実行すればaptでインストールしたものも実行できます。)

    :::
    $ LD_LIBRARY_PATH=~/usr/local/lib/ ~/usr/local/bin/ffmpeg -version
    ffmpeg version n3.4.2-1~deb9u1+rpt1 Copyright (c) 2000-2018 the FFmpeg developers
    built with gcc 6.3.0 (Raspbian 6.3.0-18+rpi1+deb9u1) 20170516
    configuration: --prefix=/home/pi/usr/local --extra-version='1~deb9u1+rpt1' --toolchain=hardened --enable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libmp3lame --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx-rpi --enable-mmal --enable-openal --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
    libavutil      55. 78.100 / 55. 78.100
    libavcodec     57.107.100 / 57.107.100
    libavformat    57. 83.100 / 57. 83.100
    libavdevice    57. 10.100 / 57. 10.100
    libavfilter     6.107.100 /  6.107.100
    libavresample   3.  7.  0 /  3.  7.  0
    libswscale      4.  8.100 /  4.  8.100
    libswresample   2.  9.100 /  2.  9.100
    libpostproc    54.  7.100 / 54.  7.100

