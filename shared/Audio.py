from shared.Shared import shared

def audio_shared(url: str, playlist: bool, numb: str, floc: str, directory: str):
    cmd = shared(playlist, numb, floc, directory)

    cmd = cmd + ["-x", "--audio-format", "mp3", url]  # the only part that is like special to Audio
        
    return cmd
