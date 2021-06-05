from shared.Shared import shared

def video_shared(url: str, playlist: bool, numb: str, qualityChoice: str, qual: str, floc: str, directory):
    cmd = shared(playlist, numb, floc, directory)

    # the parts special to Video
    if qualityChoice == "1":  # best and or the bad pick of 360p/720p
        cmd = cmd + ["-f", "best"]
    elif qualityChoice == "2":  # let's you choose, should not be possible for playlist
        cmd = cmd + ["-f", qual]
    else:  # the default option will give the best quality
        cmd = cmd + ["-f", "bestvideo+bestaudio"]

    cmd = cmd + [url]

    return cmd
