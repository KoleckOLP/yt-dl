import sys
# Imports from this project
from release import spath, settingsPath
from gui.ReEncode import ree_settings_save
from shared.Config import Settings


def set_save(window):
    window.settings.Youtubedl.audioDir = window.set_audio_bar.text()
    window.settings.Youtubedl.videoDir = window.set_videos_bar.text()
    window.settings.Python.python = window.set_py_bar.text()
    window.settings.Python.pip = window.set_pip_bar.text()
    window.settings.Youtubedl.fromPip = window.set_ydpip_checkbox.isChecked()
    window.settings.autoUpdate = window.set_aup_checkbox.isChecked()
    window.settings.defaultTab = window.set_Tab_combobox.currentIndex()
    ree_settings_save(window)


def set_load(window, audio, video, py, pip, ydpip, aup, acodec, vcodec, abit, vqual, append, tab):
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


def set_makeScript(window):  # I had an issue getting the venv working with gui
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

def WriteDefaultJson(window):
    window.settings = Settings.loadDefault()
    window.settings.toJson(settingsPath)
    set_load(window, window.settings.Youtubedl.audioDir, window.settings.Youtubedl.videoDir, window.settings.Python.python, window.settings.Python.pip, window.settings.Youtubedl.fromPip, window.settings.autoUpdate, window.settings.Ffmpeg.audioCodec, window.settings.Ffmpeg.videoCodec, window.settings.Ffmpeg.audioBitrate, window.settings.Ffmpeg.videoQuality, window.settings.Ffmpeg.append, window.settings.defaultTab)
