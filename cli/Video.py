import os
# Imports from this project
from release import spath
from kolreq.kolreq import clear


def Video(call):
    if call.fdir:
        floc = f"--ffmpeg-location {spath}"
    else:
        floc = ""

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
        if(numb == ""):  # no playlist
            print("<Enter> for best quality 1080p + if available (\"bestvideo+bestaudio\"),\n" +
                  "1 for 720 or lower (\"best\")\n" +
                  "2 to choose yourself")
            qual = input("#")
            if (qual == "1"):
                lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(title)s.%(ext)s\" -f best --no-playlist --prefer-ffmpeg {floc} \"{url}\""
            elif(qual == "2"):
                print("starting youtube-dl please wait...")
                os.system(f"youtube-dl -F --no-playlist {url}")
                print("choose video and audio quality by typing numb+numb")
                numb = input("#")
                lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(title)s.%(ext)s\" -f \"{numb}\" --no-playlist --prefer-ffmpeg {floc} \"{url}\""
            else:
                lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(title)s.%(ext)s\" -f bestvideo+bestaudio --no-playlist --prefer-ffmpeg {floc} \"{url}\""
        else:  # playlist
            print("<Enter> for the best quality 1080p + if available, \n" +
                  "1 for 720p or lower")
            qual = input("#")
            if(qual == "1"):
                if(numb == "1"):
                    lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --prefer-ffmpeg {floc} \"{url}\""
                else:
                    lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --playlist-items {numb} --prefer-ffmpeg {floc} \"{url}\""
            else:
                if(numb == "1"):
                    lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --prefer-ffmpeg {floc} \"{url}\""
                else:
                    lnk = f"-o \"{call.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --playlist-items {numb} --prefer-ffmpeg {floc} \"{url}\""
        print("starting youtube-dl please wait...")
        os.system("youtube-dl  " + lnk)
        print("\a")
