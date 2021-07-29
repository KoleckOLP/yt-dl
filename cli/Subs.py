import os
# Imports from this project
from kolreq.kolreq import clear
from shared.Subs import subs_shared_list, subs_shared_download, subs_shared_paths_for_ffmpeg, subs_shared_lines_for_ffmpeg


def Subs(call):
    lang = ""
    print(f"cookie={call.settings.Youtubedl.cookie}")
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
                cmd = subs_shared_list(url)
                call.process_start(cmd)
                print("choose language of the subtitles by typing it's code")
                lang = input("#")
        else:  # playlist
            pass

        cmd, temp = subs_shared_download(url, bool(numb), items, lang, call.floc, call.settings.Youtubedl.cookie)

        print("starting youtube-dl please wait...")

        call.process_start(cmd)

        subpath, newsubpath = subs_shared_paths_for_ffmpeg(temp.name + os.path.sep, call.settings.Youtubedl.videoDir)

        FfmpegLines = subs_shared_lines_for_ffmpeg(call, subpath, newsubpath)

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
