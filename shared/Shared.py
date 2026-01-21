import os
from release import spath


def shared(playlist: bool, numb: str, floc: str, ytex: str, directory: str, deno: str = False):
    if ytex:
        cmd = ytex
    else:
        cmd = ["yt-dlp"]

    if floc:
        cmd = cmd + ["--ffmpeg-location", floc]

    if deno:
        cmd = cmd + ["--js-runtimes", "deno:" + deno, "--remote-components", "ejs:github"]

    if playlist:  # yes playlist
        cmd = cmd + ["-o", f"{directory}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i"]
        if numb:
            cmd = cmd + ["--playlist-items", numb]
    else:  # no playlist
        cmd = cmd + ["-o", f"{directory}%(title)s.%(ext)s", "--no-playlist"]
    return cmd


def has_cookie(checkbox: bool, cmd: list):
    if checkbox:
        cmd = cmd + ["--cookies-from-browser", "firefox"]
    return cmd
