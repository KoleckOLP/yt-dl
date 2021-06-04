# Imports from this project
from release import spath
from kolreq.kolreq import clear
from shared.Audio import audio_shared


def Audio(call):
    if call.fdir:
        floc = spath
    else:
        floc = False

    clear()
    print("link to audio, playlist, 0. GoBack")
    url = input("#")
    if(url == "0"):
        clear()
        call.name()
    else:
        print("<Enter> a single audio, \n" +
              "1. to download full playlist or follow example 1-3,7,9")
        numb = input("#")

        cmd = audio_shared(url, bool(numb), numb, floc, call.settings.Youtubedl.audioDir)

        call.process_start(cmd)

        print("\a")
