from shared.Shared import shared, hasCookie


def video_list_shared(url: str, ytex):
    if ytex:
        cmd = ytex+["-F", "--no-playlist", f"{url}"]
    else:
        cmd = ["yt-dlp", "-F", "--no-playlist", f"{url}"]
    return cmd


def video_shared(url: str, playlist: bool, numb: str, qualityChoice: str, qual: str, floc: str, ytex: str, directory, cookie: bool):
    cmd = shared(playlist, numb, floc, ytex, directory)

    # the parts special to Video
    if qualityChoice == "1":  # best quality possible
        cmd = cmd + ["-f", "bestvideo+bestaudio"]
    elif qualityChoice == "2":  # let's you choose, should not be possible for playlist
        cmd = cmd + ["-f", qual]
    else:  # the default option will give the best quality
        cmd = cmd + ["-f", "best[ext=mp4]"]  # default is set to normal mp4

    cmd = hasCookie(cookie, cmd)

    cmd = cmd + [url]

    return cmd
