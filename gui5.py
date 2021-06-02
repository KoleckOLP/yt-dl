import os
import sys
import glob
import subprocess
from typing import List
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from release import year, lstupdt, spath, curb, ver, settingsPath, audioDirDefault, videoDirDefault
from Audio import Audio, aud_playlist_bar_toggle
from Video import Video, vid_quality, vid_playlist_bar_toggle, vid_quality_bar_toggle
from Subs import Subs, sub_lang, sub_playlist_bar_toggle, sub_lang_bar_toggle
from ReEncode import Reencode, ree_settings, ree_settings_save, ree_choose
from Update import Update, update_yt_dl, update_depend, upd_auto_toggle
from Config import Settings

if (sys.platform.startswith("win")):  # win, linux, darwin, freebsd
    import ctypes
    myappid = 'HorseArmored.yt-dl.gui5.'+ver  # Program Sting
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainWindow(QtWidgets.QMainWindow):
    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):  # this thing is absolutely awful, I have no clue how could it work before
        drag = ""  # fixes a crash
        if "file:///" in e.mimeData().text():
            drag = e.mimeData().text().replace("file:///", "")

        self.ree_location_bar.setText(drag)  # dropping anywhere on the main window drops into ree_location_bar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(f"gui{os.path.sep}gui5.ui", self)

        self.show()

        self.setAcceptDrops(True)

        # region ===== startup =====
        pffmpeg = glob.glob(f"{spath}/ffmpeg*")
        pffprobe = glob.glob(f"{spath}/ffprobe*")
        if (not pffmpeg and not pffprobe):
            self.fdir = False
        else:
            self.fdir = True

        if (os.path.exists(settingsPath)):
            self.settings = Settings.fromJson(settingsPath)
        else:
            self.messagePopup("Settings error", QMessageBox.Critical, "You are missing a config file,\nPress OK to load default config.", self.SaveDefaultConfig)

        self.setWindowTitle(f"yt-dl {ver}")

        self.tabWidget.setCurrentIndex(self.settings.defaultTab)  # the code will not get here if settings is undefined.

        self.running = False
        self.status("Ready.")
        # endregion

        # =====aud_controls=====#
        self.aud_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.audioDir))
        self.aud_download_button.clicked.connect(lambda: Audio(self))
        self.aud_playlist_checkbox.clicked.connect(lambda: aud_playlist_bar_toggle(self))
        self.aud_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Audio) paste a link and hit download.")
        # endregion

        # =====vid_controls=====#
        self.vid_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.vid_download_button.clicked.connect(lambda: Video(self))
        self.vid_quality_button.clicked.connect(lambda: vid_quality(self))
        self.vid_playlist_checkbox.clicked.connect(lambda: vid_playlist_bar_toggle(self))
        self.vid_custom_radio.toggled.connect(lambda: vid_quality_bar_toggle(self))
        self.vid_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Video) paste a link and hit download.")
        # endregion

        # =====sub_controls=====#
        self.sub_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.sub_download_button.clicked.connect(lambda: Subs(self))
        self.sub_lang_button.clicked.connect(lambda: sub_lang(self))
        self.sub_playlist_checkbox.toggled.connect(lambda: sub_playlist_bar_toggle(self))
        self.sub_lang_checkbox.toggled.connect(lambda: sub_lang_bar_toggle(self))
        self.sub_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Subtitles) paste a link and hit download.")
        # endregion

        # =====ree_controls=====#
        self.ree_settings_combobox.addItem("hevc_opus")  # setting up items in combo list
        self.ree_settings_combobox.addItem("h264_nvenc")
        self.ree_settings_combobox.addItem("hevc_nvenc")
        self.ree_settings_combobox.addItem("mp3")
        self.ree_settings_combobox.addItem("custom")
        self.ree_settings_combobox.setCurrentIndex(self.settings.defaultCodec)
        ree_settings(self)  # load option on startup
        self.ree_choose_button.clicked.connect(lambda: ree_choose(self))
        self.ree_reencode_button.clicked.connect(lambda: Reencode(self))
        self.ree_folder_button.clicked.connect(lambda: self.openFolder(self.ree_location_bar.text()))
        self.ree_settings_combobox.activated.connect(lambda: ree_settings(self))
        self.ree_settings_button.clicked.connect(lambda: ree_settings_save(self))
        self.ree_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Re-encode) paste a link and hit download.")
        # self.ree_location_bar.setDragEnabled(True)
        self.ree_location_bar.setAcceptDrops(True)
        # endregion

        # ======upd_controls======#
        self.upd_update_combobox.addItem("All")  # setting up items in combo list
        self.upd_update_combobox.addItem("yt-dl")
        self.upd_update_combobox.addItem("dependencies")
        if (sys.platform.startswith("haiku")):
            self.upd_update_combobox.setCurrentIndex(1)

        QtWidgets.QApplication.processEvents()
        if self.settings.autoUpdate:
            self.tabWidget.setCurrentIndex(4)
            Update(self)

        self.upd_update_button.clicked.connect(lambda: Update(self))
        # self.upd_branch_button.clicked.connect(upd_branch)
        self.upd_auto_button.setText(f"Autoupdate=\"{self.settings.autoUpdate}\"")
        self.upd_auto_button.clicked.connect(lambda: upd_auto_toggle(self))
        # endregion

        # =====set_controls=====#
        self.set_loadcur_button.clicked.connect(lambda: self.set_load(self.settings.Youtubedl.audioDir, self.settings.Youtubedl.videoDir, self.settings.Python.python, self.settings.Python.pip, self.settings.Youtubedl.fromPip, self.settings.autoUpdate, self.settings.Ffmpeg.audioCodec, self.settings.Ffmpeg.videoCodec, self.settings.Ffmpeg.audioBitrate, self.settings.Ffmpeg.videoQuality, self.settings.Ffmpeg.append, self.settings.defaultTab))
        self.set_loaddef_button.clicked.connect(lambda: self.set_load(audioDirDefault, videoDirDefault, "python", "pip", True, False, "opus", "libx265", "190k", "24,24,24", "_custom.mkv", 0))
        self.set_folder_button.clicked.connect(lambda: self.openFolder(spath))
        self.set_launch_button.clicked.connect(self.set_makeScript)
        self.set_save_button.clicked.connect(self.set_save)
        self.set_Tab_combobox.addItem("Audio")  # setting up items in combo list
        self.set_Tab_combobox.addItem("Video")
        self.set_Tab_combobox.addItem("Subs")
        self.set_Tab_combobox.addItem("Re-encode")
        self.set_Tab_combobox.addItem("Update")
        self.set_Tab_combobox.addItem("Settings")
        self.set_Tab_combobox.addItem("About")
        self.set_load(self.settings.Youtubedl.audioDir, self.settings.Youtubedl.videoDir, self.settings.Python.python, self.settings.Python.pip, self.settings.Youtubedl.fromPip, self.settings.autoUpdate, self.settings.Ffmpeg.audioCodec, self.settings.Ffmpeg.videoCodec, self.settings.Ffmpeg.audioBitrate, self.settings.Ffmpeg.videoQuality, self.settings.Ffmpeg.append, self.settings.defaultTab)
        # endregion

        # region ==========🎓ABOUT🎓==========
        self.about_box.setHtml(f"<p style=\"font-size: 20px; white-space: pre\">HorseArmored Inc. (C){year}<br>" +
                               f"Version: {ver} gui5 ({curb} branch)<br>" +
                               f"Last updated on: {lstupdt}<br>" +
                               f"My webpage: <a href=\"https://koleckolp.comli.com\">https://koleckolp.comli.com</a><br>" +
                               f"Project page: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://github.com/KoleckOLP/yt-dl</a><br>" +
                               f"need help? ask here: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://discord.gg/W88375j</a><br>" +
                               f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez<br>" +
                               f"                 (C)2011-{year} youtube-dl developers<br>" +
                               f"ffmpeg (C)2000-{year} FFmpeg team<br>" +
                               f"Thanks to <a href=\"https://github.com/kangalioo\">kangalioo</a> who always helps a ton!<br>" +
                               f"Thanks to <a href=\"https://github.com/siscodeorg\">siscode</a> for featuring my project<br>" +
                               f"and helping me improve it.<br>" +
                               f"You can read the changelog: <a href=\"https://github.com/KoleckOLP/yt-dl/blob/master/changelog.md\">here</a></pre></p>")
        # endregion

    @staticmethod
    def messagePopup(title, icon, text, callf=None):
        msg = QMessageBox()  # Pylance is being stupid, I had to disable Type checking.
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(text)
        if callf is not None:
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # Fuck pylance it says that this line is wrong anf that int can't bd a button, there is not int.
            msg.buttonClicked.connect(callf)
        msg.exec_()

    def SaveDefaultConfig(self, i):
        text: str = i.text().lower()
        if "ok" in text:
            self.settings = Settings.loadDefault()
            self.settings.toJson(settingsPath)
        else:
            exit()

    def status(self, s=""):  # shows status message and changes color of the status bar.
        self.statusBar().showMessage(s)
        if s == "Ready.":
            self.statusBar().setStyleSheet("background-color: #00BB00")
        elif s == "Busy.":
            self.statusBar().setStyleSheet("background-color: #FF6600")
        else:
            self.statusBar().setStyleSheet("background-color: #A9A9A9")

    @staticmethod
    def process_start(cmd: List[str], output_console):
        if (sys.platform.startswith("win")):  # (os.name == "nt"):
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000, universal_newlines=True, encoding="utf8")  # this one does not check if another process is running
        else:  # (sys.platform.startswith(("linux", "darwin", "freebsd"))): #(os.name == "posix"): #other oeses should be fine with this
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, errors="ignore")
        while True:
            test = process.stdout.readline()
            if not test:
                break
            test = str(test)
            if "\\n" in test:
                test = test.replace("\\n", "\n")
            output_console.insertPlainText(test)
            scrollbar = output_console.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            QtWidgets.QApplication.processEvents()
        print("\a")
        output_console.insertPlainText("#yt-dl# Process has finished.\n\n")
        QtWidgets.QApplication.processEvents()
        scrollbar = output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @staticmethod
    def openFolder(loc: str):
        if not os.path.exists(loc):
            os.makedirs(loc)
        if (sys.platform.startswith("win")):
            os.system(f"start {loc}")
        elif (sys.platform.startswith(("darwin", "haiku"))):  # haiku support :3
            os.system(f"open {loc}")
        else:  # (sys.platform.startswith(("linux", "freebsd"))): #hoping that other OSes use xdg-open
            os.system(f"xdg-open {loc}")

    @staticmethod
    def hasCookie(checkbox: bool, cmd: list):
        if checkbox:
            if os.path.exists(spath + "cookies.txt"):
                cmd = cmd + ["--cookies", spath + "cookies.txt"]
                return cmd

    # region ==========📈SETTINGS📈==========
    def set_save(self):
        self.settings.Youtubedl.audioDir = self.set_audio_bar.text()
        self.settings.Youtubedl.videoDir = self.set_videos_bar.text()
        self.settings.Python.python = self.set_py_bar.text()
        self.settings.Python.pip = self.set_pip_bar.text()
        self.settings.Youtubedl.fromPip = self.set_ydpip_checkbox.isChecked()
        self.settings.autoUpdate = self.set_aup_checkbox.isChecked()
        self.ree_settings_save()

    def set_load(self, audio, video, py, pip, ydpip, aup, acodec, vcodec, abit, vqual, append, tab):
        self.set_audio_bar.setText(audio)
        self.set_videos_bar.setText(video)
        self.set_py_bar.setText(py)
        self.set_pip_bar.setText(pip)
        self.set_ydpip_checkbox.setChecked(ydpip)
        self.set_aup_checkbox.setChecked(aup)
        self.set_Acodec_bar.setText(acodec)
        self.set_Vcodec_bar.setText(vcodec)
        self.set_Abit_bar.setText(abit)
        self.set_Vqual_bar.setText(vqual)
        self.set_Append_bar.setText(append)
        self.set_Tab_combobox.setCurrentIndex(tab)

    def set_makeScript(self):  # I had an issue getting the venv working with gui
        if(sys.platform.startswith("win")):
            f = open("yt-dl_gui.vbs", "w")
            f.write(f"Set WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run \"cmd /c cd /d {spath} & pythonw.exe gui.py\", 0\nSet WshShell = Nothing")
            f.close()
            f = open("yt-dl_gui.bat", "w")
            f.write(f"@echo off\n\nstart /b pythonw.exe gui5.py")
            f.close()
        else:  # (sys.platform.startswith(("linux", "darwin", "freebsd"))):
            f = open("yt-dl", "w")
            f.write(f"#!/bin/sh\n\ncd {spath} && {self.settings.Python.python} gui5.py")
            f.close()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
