import sys
# Imports from this project
from release import spath, settingsPath
from gui.ReEncode import ree_settings_save
from shared.Config import Settings


def set_save(window):
    window.settings.ytdlp_settings.audio_dir = window.set_audio_bar.text()
    window.settings.ytdlp_settings.video_dir = window.set_videos_bar.text()
    window.settings.python_settings.python = window.set_py_bar.text()
    window.settings.python_settings.pip = window.set_pip_bar.text()
    window.settings.ytdlp_settings.from_pip = window.set_ydpip_checkbox.isChecked()
    window.settings.auto_update = window.set_aup_checkbox.isChecked()
    window.settings.default_tab = window.set_Tab_combobox.currentIndex()
    window.settings.auto_close = window.set_close_checkbox.isChecked()
    window.settings.clipboard = window.set_clipboard_checkbox.isChecked()
    if window.vid_best_radio.isChecked():
        window.settings.ytdlp_settings.quality = "best"
    elif window.vid_normal_radio.isChecked():
        window.settings.ytdlp_settings.quality = "normal"
    elif window.vid_custom_radio.isChecked():
        window.settings.ytdlp_settings.quality = "custom"
    ree_settings_save(window)


def set_load(window, audio, video, py, pip, ydpip, aup, acodec, vcodec, abit, vqual, append, tab, close):
    window.set_audio_bar.setText(audio)
    window.set_videos_bar.setText(video)
    window.set_py_bar.setText(py)
    window.set_pip_bar.setText(pip)
    window.set_ydpip_checkbox.setChecked(ydpip)
    window.set_aup_checkbox.setChecked(aup)
    window.set_Acodec_bar.setText(acodec)
    window.set_Vcodec_bar.setText(vcodec)
    window.set_Abit_bar.setText(abit)
    window.set_Vqual_bar.setText(vqual)
    window.set_Append_bar.setText(append)
    window.set_Tab_combobox.setCurrentIndex(tab)
    window.set_close_checkbox.setChecked(close)


def set_make_script(window):  # I had an issue getting the venv working with gui
    if (sys.platform.startswith("win")):
        f = open("yt-dl_gui.vbs", "w")
        f.write(f"Set WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run \"cmd /c cd /d {spath} & pythonw.exe gui.py\", 0\nSet WshShell = Nothing")
        f.close()
        f = open("yt-dl_gui.bat", "w")
        f.write(f"@echo off\n\nstart /b pythonw.exe gui.py")
        f.close()
    else:  # (sys.platform.startswith(("linux", "darwin", "freebsd"))):
        f = open("yt-dl", "w")
        f.write(f"#!/bin/sh\n\ncd {spath} && {window.settings.Python.python} gui.py")
        f.close()

def write_default_json(window):
    window.settings = Settings.load_default()
    window.settings.to_json(settingsPath)
    set_load(
        window,
        window.settings.ytdlp_settings.audio_dir,
        window.settings.ytdlp_settings.video_dir,
        window.settings.python_settings.python,
        window.settings.python_settings.pip,
        window.settings.ytdlp_settings.from_pip,
        window.settings.auto_update,
        window.settings.ffmpeg_settings.audio_codec,
        window.settings.ffmpeg_settings.video_codec,
        window.settings.ffmpeg_settings.audio_bitrate,
        window.settings.ffmpeg_settings.video_quality,
        window.settings.ffmpeg_settings.append,
        window.settings.default_tab,
        window.settings.auto_close
    )
