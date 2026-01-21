import json, sys, os, subprocess, platform
# Imports from this projects
from release import videoDirDefault, audioDirDefault, spath


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class PythonSettings:
    def __init__(self, python: str, pip: str):
        self.python = python
        self.pip = pip


class YtdlpSettings:
    def __init__(self, audio_dir: str, video_dir: str, from_pip: bool, cookie: bool, quality: str):
        self.audio_dir = audio_dir
        self.video_dir = video_dir
        self.from_pip = from_pip
        self.cookie = cookie
        self.quality = quality


class FfmpegSettings:
    def __init__(self, video_codec: str, audio_codec: str, video_quality: str, audio_bitrate: str, append: str):
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.video_quality = video_quality
        self.audio_bitrate = audio_bitrate
        self.append = append

class WindowSettings:
    def __init__(self, window_width: int, window_height: int, window_pos_x: int, window_pos_y: int):
        self.window_width = window_width
        self.window_height = window_height
        self.window_pos_x = window_pos_x
        self.window_pos_y = window_pos_y

class Settings:
    def __init__(self, python_settings: PythonSettings, ytdlp_settings: YtdlpSettings, ffmpeg_settings: FfmpegSettings, window_settings: WindowSettings, auto_update: bool, default_tab: int, default_codec: int, auto_close: bool, clipboard: bool):
        self.python_settings = python_settings
        self.ytdlp_settings = ytdlp_settings
        self.ffmpeg_settings = ffmpeg_settings
        self.window_settings = window_settings
        self.auto_update = auto_update
        self.default_tab = default_tab
        self.default_codec = default_codec
        self.auto_close = auto_close
        self.clipboard = clipboard

    def to_json(self, path):
        with open(path, "w") as fh:
            x = json.dumps(self, indent=4, cls=Encoder)
            fh.writelines(x)

    @staticmethod
    def from_json(path):
        with open(path, "r") as fh:
            x = json.loads(fh.read())
        return Settings(PythonSettings(x["python_settings"]["python"],
                                       x["python_settings"]["pip"]),
                        YtdlpSettings(x["ytdlp_settings"]["audio_dir"],
                                      x["ytdlp_settings"]["video_dir"],
                                      x["ytdlp_settings"]["from_pip"],
                                      x["ytdlp_settings"]["cookie"],
                                      x["ytdlp_settings"]["quality"]),
                        FfmpegSettings(x["ffmpeg_settings"]["video_codec"],
                                       x["ffmpeg_settings"]["audio_codec"],
                                       x["ffmpeg_settings"]["video_quality"],
                                       x["ffmpeg_settings"]["audio_bitrate"],
                                       x["ffmpeg_settings"]["append"]),
                        WindowSettings(x["window_settings"]["window_width"],
                                       x["window_settings"]["window_height"],
                                       x["window_settings"]["window_pos_x"],
                                       x["window_settings"]["window_pos_y"]),
                        x["auto_update"],
                        x["default_tab"],
                        x["default_codec"],
                        x["auto_close"],
                        x["clipboard"])

    @staticmethod
    def load_default():
        if "portable" in os.path.basename(os.path.normpath(spath)):
            if platform.release().lower() == "vista":
                defpython = "..\\python-3119\\python.exe"
                defpip = "..\\python-3119\\python.exe -m pip"
            else:
                defpython = "..\\python\\python.exe"
                defpip = "..\\python\\python.exe -m pip"
        else:
            defpython = os.path.basename(sys.executable)
            defpip = os.path.basename(sys.executable) + " -m pip"

        try:
            result = subprocess.run(['pip', 'show', 'yt-dlp'], capture_output=True, text=True)
            if result.returncode == 0:
                ytdlppip = True
            else:
                ytdlppip = False
        except Exception as e:
            print(f"Error checking with pip: {e}")
            ytdlppip = False

        return Settings(PythonSettings(defpython, defpip),
                        YtdlpSettings(audioDirDefault, videoDirDefault, ytdlppip, False, "best"),
                        FfmpegSettings("libx265", "opus", "24,24,24", "190k", "_custom.mkv"),
                        WindowSettings(0, 0, 0, 0),
                        False,
                        0,
                        0,
                        False,
                        False)
