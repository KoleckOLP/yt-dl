from shared.Shared import shared, has_cookie


def audio_shared(url: str, playlist: bool, numb: str, floc: str, ytex: str, directory: str, cookie: bool, deno: str = False):
    cmd = shared(playlist, numb, floc, ytex, directory, deno)

    cmd = cmd + ["-x", "--audio-format", "mp3", url]  # the only part that is like special to Audio

    cmd = has_cookie(cookie, cmd)
        
    return cmd
