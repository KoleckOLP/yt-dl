import os
import glob
import tempfile
from typing import List
# Imports from this project
from shared.Shared import shared, hasCookie


def subs_shared_list(url: str, ytex):
    if ytex:
        cmd = ytex+["--list-subs", "--no-playlist", f"{url}"]
    else:
        cmd = ["youtube-dl", "--list-subs", "--no-playlist", f"{url}"]
    return cmd


def subs_shared_download(url: str, playlist: bool, numb: str, lang: str, floc: str, ytex: str, cookie: bool):
    temp = tempfile.TemporaryDirectory()

    cmd = shared(playlist, numb, floc, ytex, temp.name+os.path.sep)

    cmd = cmd + ["--write-sub", "--write-auto-sub", "--sub-format", "vtt", "--skip-download", f"{url}"]

    if lang:
        if lang == "all":
            cmd = cmd + ["--all-subs"]
        else:
            cmd = cmd + ["--sub-lang", lang]

    cmd = hasCookie(cookie, cmd)

    return (cmd, temp)


def subs_shared_paths_for_ffmpeg(temp, directory: str):
    subpath = glob.glob(f"{temp}*.vtt")

    os.makedirs(directory, exist_ok=True)

    retNewSubsPath = []

    for item in subpath:  # ehh this does not work with all subs
        namei = os.path.basename(item)
        namei = namei[:-3]
        newsubpath = directory + namei + "srt"
        retNewSubsPath = retNewSubsPath + [newsubpath]

    return (subpath, retNewSubsPath)


def subs_shared_lines_for_ffmpeg(call_window, subpath: List[str], newsubpath: List[str]):
    retFfmpegLines = []

    if not subpath or not newsubpath:
        return "error"

    for old, new in zip(subpath, newsubpath):
        if os.path.exists(new):
            return new

        if call_window.floc:
            ffmpeg = call_window.floc+os.path.sep+"ffmpeg"
        else:
            ffmpeg = "ffmpeg"
        retFfmpegLines = retFfmpegLines + [[ffmpeg, "-i", old, new]]

    return retFfmpegLines
