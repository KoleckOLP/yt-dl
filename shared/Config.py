import json, sys, os, subprocess
# Imports from this projects
from release import videoDirDefault, audioDirDefault, spath


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class PythonSettings:
    def __init__(self, python: str, pip: str):
        self.python = python
        self.pip = pip


class YoutubedlSettings:
    def __init__(self, audioDir: str, videoDir: str, fromPip: bool, cookie: bool):
        self.audioDir = audioDir
        self.videoDir = videoDir
        self.fromPip = fromPip
        self.cookie = cookie


class FfmpegSettings:
    def __init__(self, videoCodec: str, audioCodec: str, videoQuality: str, audioBitrate: str, append: str):
        self.videoCodec = videoCodec
        self.audioCodec = audioCodec
        self.videoQuality = videoQuality
        self.audioBitrate = audioBitrate
        self.append = append

class WindowSettings:
    def __init__(self, windowWidth: int, windowHeight: int, windowPosX: int, windowPosY: int):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.windowPosX = windowPosX
        self.windowPosY = windowPosY

class Settings:
    def __init__(self, Python: PythonSettings, Youtubedl: YoutubedlSettings, Ffmpeg: FfmpegSettings, Window: WindowSettings, autoUpdate: bool, defaultTab: int, defaultCodec: int, autoClose: bool):
        self.Python = Python
        self.Youtubedl = Youtubedl
        self.Ffmpeg = Ffmpeg
        self.Window = Window
        self.autoUpdate = autoUpdate
        self.defaultTab = defaultTab
        self.defaultCodec = defaultCodec
        self.autoClose = autoClose

    def toJson(self, path):
        with open(path, "w") as fh:
            x = json.dumps(self, indent=4, cls=Encoder)
            fh.writelines(x)

    @staticmethod
    def fromJson(path):
        with open(path, "r") as fh:
            x = json.loads(fh.read())
        return Settings(PythonSettings(x["Python"]["python"],
                                       x["Python"]["pip"]),
                        YoutubedlSettings(x["Youtubedl"]["audioDir"],
                                          x["Youtubedl"]["videoDir"],
                                          x["Youtubedl"]["fromPip"],
                                          x["Youtubedl"]["cookie"]),
                        FfmpegSettings(x["Ffmpeg"]["videoCodec"],
                                       x["Ffmpeg"]["audioCodec"],
                                       x["Ffmpeg"]["videoQuality"],
                                       x["Ffmpeg"]["audioBitrate"],
                                       x["Ffmpeg"]["append"]),
                        WindowSettings(x["Window"]["windowWidth"],
                                       x["Window"]["windowHeight"],
                                       x["Window"]["windowPosX"],
                                       x["Window"]["windowPosY"]),
                        x["autoUpdate"],
                        x["defaultTab"],
                        x["defaultCodec"],
                        x["autoClose"])

    @staticmethod
    def loadDefault():
        if "yt-dl_portable" in spath:  # if you are running the portable version of yt-dl, this is the default path for python and pip
            defpython = "..\\python\\python"
            defpip = "..\\python\\python -m pip"
        else:  # if you are not running the portable version of yt-dl, this takes the executable of the current python interpreter and uses that as the default python and pip
            defpython = os.path.basename(sys.executable)
            defpip = os.path.basename(sys.executable) + " -m pip"

        try:
            result = subprocess.run(['pip', 'show', 'yt-dlp'], capture_output=True, text=True)
            if result.returncode == 0:
                # This means pip found yt-dlp, hence it was installed with pip
                ytdlppip = True
            else:
                # yt-dlp is not found in pip
                ytdlppip = False
        except Exception as e:
            print(f"Error checking with pip: {e}")
            ytdlppip = False

        return Settings(PythonSettings(defpython,  # python executable name
                                       defpip),  # pip executable name/command
                        YoutubedlSettings(audioDirDefault,  # audio folder inside of yt-dl
                                          videoDirDefault,  # video folder inside of yt-dl
                                          ytdlppip,  # this is true if yt-dlp was installed with pip, false if it was installed with other package manager or manually
                                          False),  # cookie, is currently not dected, but it is not needed for most users, so it's false by default
                        FfmpegSettings("libx265",  # This is just fine
                                       "opus",  # same as above
                                       "24,24,24",  # same as above
                                       "190k",  # same as above
                                       "_custom.mkv"),  # same as above
                        WindowSettings(0,
                                       0,
                                       0,
                                       0), # defaul window size and position, this is set to 0,0,0,0 so it will be set to the default size and position of the OS
                        False,  # I would recommend not having auto update on, it's annoying.
                        0,  # audio tab
                        0,  # hevc_opus
                        False)  # raf autoClose
