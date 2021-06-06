import os
import glob
import tempfile
from typing import List
# Imports from this project
from shared.Shared import shared

def subs_list_shared(url):
    cmd = ["youtube-dl", "--list-subs", "--no-playlist", f"{url}"]
    return cmd

def subs_shared_part1(url: str, playlist: bool, numb: str, lang: str, floc: str):
    temp = tempfile.mkdtemp() + os.path.sep

    cmd =  shared(playlist, numb, floc, temp)

    cmd = cmd + ["--write-sub", "--write-auto-sub", "--sub-format", "vtt", "--skip-download", f"{url}"]

    if lang:
        '''  # going to implement all subs later
        if lang == "all":
            cmd = cmd + ["--all-subs"]
        else:
        '''
        cmd = cmd + ["--sub-lang", lang]

    return (cmd, temp)

def subs_shared_part2(call_window, temp: List[str], directory: str):
    subpath = glob.glob(f"{temp}*.vtt")

    os.makedirs(directory, exist_ok=True)

    for item in subpath:  # ehh this does not work with all subs
        namei = os.path.basename(item)
        namei = namei[:-3]
        newsubpath = directory + namei + "srt"
        if os.path.isfile(newsubpath):
            return newsubpath
        else:
            if call_window.floc:
                ffmpeg = call_window.floc
            else:
                ffmpeg = "ffmpeg"
            return [ffmpeg, "-i", f"{item}", f"{newsubpath}"]