from shared.Shared import shared, hasCookie


def audio_shared(url: str, playlist: bool, numb: str, floc: str, ytex: str, directory: str, cookie: bool):
    cmd = shared(playlist, numb, floc, ytex, directory)

    cmd = cmd + ["-x", "--audio-format", "mp3", url]  # the only part that is like special to Audio

    cmd = hasCookie(cookie, cmd)
        
    return cmd
