def audio_shared(url: str, playlist: bool, numb: str, floc: str, audioDir):
    cmd = ["youtube-dl"]

    if floc:
        cmd = cmd + ["--prefer-ffmpeg", "--ffmpeg-location", floc]

    if playlist:  # yes playlist
        cmd = cmd + ["-o", f"{audioDir}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i"]
        if numb:
            cmd = cmd + ["--playlist-items", numb]
    else:  # no playlist
        cmd = cmd + ["-o", f"{audioDir}%(title)s.%(ext)s", "--no-playlist"]

    cmd = cmd + ["-x", "--audio-format", "mp3", url]
        
    return cmd
