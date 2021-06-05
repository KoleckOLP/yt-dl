# Imports from this project
from kolreq.kolreq import clear
from shared.Video import video_shared


def Video(call):
    qual = ""

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
            qualityChoice = input("#")
            if qualityChoice == "2":
                qual = input("#")
        else:  # playlist
            print("<Enter> for the best quality 1080p + if available, \n" +
                  "1 for 720p or lower")
            qualityChoice = input("#")

        cmd = video_shared(url, bool(numb), numb, qualityChoice, qual, call.floc, call.settings.Youtubedl.videoDir)

        print("starting youtube-dl please wait...")

        call.process_start(cmd)

        print(qualityChoice)

        print("\a")
