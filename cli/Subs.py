import os
import glob
import tempfile
# Imports from this project
from release import spath
from kolreq.kolreq import clear
from shared.Subs import subs_list_shared, subs_shared_part1, subs_shared_part2


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

        else:  # playlist

        cmd = subs_shared_part1(url, bool(numb), items, lang, call.floc)

        print("starting youtube-dl please wait...")

        call.process_start(cmd)

