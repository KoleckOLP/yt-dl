def Subs(call):
    if call.fdir:
        floc = f"--ffmpeg-location {spath}"
    else:
        floc = ""

    clear()
    temp = tempfile.mkdtemp() + os.path.sep
    print("link to video with subs or 0. GoBack")
    url = input("#")
    if (url == "0"):
        clear()
        call.name()
    else:
        print("<Enter> to download default sub (en),\n" +
              "1 to choose language")
        numb = input("#")
        if(numb == ""):
            lnk = f"-o \"{temp}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-format vtt --skip-download --prefer-ffmpeg {floc} \"{url}\""
        else:
            print("starting youtube-dl please wait...")
            os.system(f"youtube-dl --list-subs --noplaylist {url}")
            print("choose sub language")
            numb = input("#")
            lnk = f"-o \"{temp}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-lang \"{numb}\" --sub-format vtt --skip-download --prefer-ffmpeg {floc} \"{url}\""
        print("starting youtube-dl please wait...")
        os.system("youtube-dl  " + lnk)
        pie = glob.glob(f"{temp}*.vtt")
        cream = os.path.basename(pie[0])
        cream = cream[:-3]
        lick = f"{call.settings.Youtubedl.videoDir}{cream}srt"  # I don't like this fix to a complain about var type
        os.makedirs(call.settings.Youtubedl.videoDir, exist_ok=True)
        print("starting youtube-dl please wait...")
        os.system(f"ffmpeg -i \"{pie[0]}\" \"{lick}\"")
        print("\a")