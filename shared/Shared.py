import os
from release import spath


def shared(playlist: bool, numb: str, floc: str, ytex: str, directory: str):
    if ytex:
        cmd = ytex
    else:
        cmd = ["youtube-dl"]

    if floc:
        cmd = cmd + ["--prefer-ffmpeg", "--ffmpeg-location", floc]

    if playlist:  # yes playlist
        cmd = cmd + ["-o", f"{directory}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i"]
        if numb:
            cmd = cmd + ["--playlist-items", numb]
    else:  # no playlist
        cmd = cmd + ["-o", f"{directory}%(title)s.%(ext)s", "--no-playlist"]
    return cmd


def hasCookie(checkbox: bool, cmd: list):
    if checkbox:
        if os.path.exists(spath + "cookies.txt"):
            cmd = cmd + ["--cookies", spath + "cookies.txt"]
    return cmd
