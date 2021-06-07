import os
# Imports from this project
from kolreq.kolreq import clear
from shared.Subs import subs_list_shared, subs_shared_part1, subs_shared_part2, subs_shared_part3


def Subs(call):
    lang = ""

    clear()
    print("link to video, playlist, 0. GoBack")
    url = input("#")
    if (url == "0"):
        clear()
        call.name()
    else:
        print("<Enter> a single video, \n" +
              "1. to download full playlist or follow example 1-3,7,9")
        numb = input("#")
        if (numb == "1"):  # fix for playlist
            items = ""
        else:
            items = numb

        if (numb == ""):  # no playlist
            print("<Enter> default lang (probably en)\n" +
                  "1. list languages")
            use_custom_lang = input("#")
            if use_custom_lang == "1":
                cmd = subs_list_shared(url)
                call.process_start(cmd)
                print("choose language of the subtitles by typing it's code")
                lang = input("#")
        else:  # playlist
            pass

        cmd, temp = subs_shared_part1(url, bool(numb), items, lang, call.floc)

        print("starting youtube-dl please wait...")

        call.process_start(cmd)

        subpath, newsubpath = subs_shared_part2(temp.name+os.path.sep, call.settings.Youtubedl.videoDir)

        FfmpegLines = subs_shared_part3(call, subpath, newsubpath)

        if isinstance(FfmpegLines, str):
            if FfmpegLines == "error":
                print(f"#yt-dl# found an issue aborting...\n")
            else:
                print(f"#yt-dl# file {FfmpegLines} already exists aborting...\n")

        else:
            for line in FfmpegLines:
                print("#yt-dl# starting ffmpeg please wait...\n")

                call.process_start(line)

                print("\a")

        temp.cleanup()
