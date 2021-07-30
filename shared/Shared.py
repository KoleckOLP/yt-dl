def shared(playlist: bool, numb: str, floc: str, directory:str):
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
