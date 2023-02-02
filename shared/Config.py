import json
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
    def __init__(self, Python: PythonSettings, Youtubedl: YoutubedlSettings, Ffmpeg: FfmpegSettings, Window: WindowSettings, autoUpdate: bool, defaultTab: int, defaultCodec: int):
        self.Python = Python
        self.Youtubedl = Youtubedl
        self.Ffmpeg = Ffmpeg
        self.Window = Window
        self.autoUpdate = autoUpdate
        self.defaultTab = defaultTab
        self.defaultCodec = defaultCodec

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
                        x["defaultCodec"])

    @staticmethod
    def loadDefault():
        if(spath.find("yt-dl_portable")):
            defpython = "..\python\python"
            defpip = "..\python\python -m pip"
        else:
            defpython = "python"
            defpip = "pip"

        return Settings(PythonSettings(defpython,  # I don't like this because some systems need python3 or python3.x here
                                       defpip),  # some systems might have pip3.x here
                        YoutubedlSettings(audioDirDefault,  # audio folder inside of yt-dl
                                          videoDirDefault,  # video folder inside of yt-dl
                                          True,
                                          False),  # only true if youtube-dl is from pip which this just assumes
                        FfmpegSettings("libx265",  # This is just fine
                                       "opus",  # same as above
                                       "24,24,24",  # same as above
                                       "190k",  # same as above
                                       "_custom.mkv"),  # same as above
                        WindowSettings(0,
                                       0,
                                       0,
                                       0),
                        False,  # I would recommend not having auto update on, it's annoying.
                        0,  # audio tab
                        0)  # hevc_opus
