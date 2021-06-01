import os
import sys
import glob
import subprocess
import tempfile
from typing import List
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
# Imports from this project
from release import year, lstupdt, spath, curb, ver, settingsPath, audioDirDefault, videoDirDefault
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
        self.aud_download_button.clicked.connect(self.Audio)
        self.aud_playlist_checkbox.clicked.connect(self.aud_playlist_bar_toggle)
        self.aud_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Audio) paste a link and hit download.")
        # endregion

        # =====vid_controls=====#
        self.vid_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.vid_download_button.clicked.connect(self.Video)
        self.vid_quality_button.clicked.connect(self.vid_quality)
        self.vid_playlist_checkbox.clicked.connect(self.vid_playlist_bar_toggle)
        self.vid_custom_radio.toggled.connect(self.vid_quality_bar_toggle)
        self.vid_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Video) paste a link and hit download.")
        # endregion

        # =====sub_controls=====#
        self.sub_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.sub_download_button.clicked.connect(self.Subs)
        self.sub_lang_button.clicked.connect(self.sub_lang)
        self.sub_playlist_checkbox.toggled.connect(self.sub_playlist_bar_toggle)
        self.sub_lang_checkbox.toggled.connect(self.sub_lang_bar_toggle)
        self.sub_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Subtitles) paste a link and hit download.")
        # endregion

        # =====ree_controls=====#
        self.ree_settings_combobox.addItem("hevc_opus")  # setting up items in combo list
        self.ree_settings_combobox.addItem("h264_nvenc")
        self.ree_settings_combobox.addItem("hevc_nvenc")
        self.ree_settings_combobox.addItem("mp3")
        self.ree_settings_combobox.addItem("custom")
        self.ree_settings_combobox.setCurrentIndex(self.settings.defaultCodec)
        self.ree_settings()  # load option on startup
        self.ree_choose_button.clicked.connect(self.ree_choose)
        self.ree_reencode_button.clicked.connect(self.Reencode)
        self.ree_folder_button.clicked.connect(lambda: self.openFolder(self.ree_location_bar.text()))
        self.ree_settings_combobox.activated.connect(self.ree_settings)
        self.ree_settings_button.clicked.connect(self.ree_settings_save)
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
            self.Update()

        self.upd_update_button.clicked.connect(self.Update)
        # self.upd_branch_button.clicked.connect(upd_branch)
        self.upd_auto_button.setText(f"Autoupdate=\"{self.settings.autoUpdate}\"")
        self.upd_auto_button.clicked.connect(self.upd_auto_toggle)
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

    # region ==========🎶AUDIO🎶==========
    def Audio(self):
        if not self.running:
            self.running = True
            self.status("Busy.")
            self.tabWidget.setTabText(0, "*Audio")

            self.aud_output_console.setHtml("")  # clearing the output_console

            url = self.aud_url_bar.text()
            if self.aud_playlist_checkbox.isChecked():
                numb = self.aud_playlist_bar.text()
            else:
                numb = None

            if(numb is None):
                cmd = [["youtube-dl", "-o", f"{self.settings.Youtubedl.audioDir}%(title)s.%(ext)s", "--no-playlist", "-x", "--prefer-ffmpeg"], ["--audio-format", "mp3", f"{url}"]]
            elif(numb == ""):
                cmd = [["youtube-dl", "-o", f"{self.settings.Youtubedl.audioDir}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i", "-x", "--prefer-ffmpeg"], ["--audio-format", "mp3", f"{url}"]]
            else:
                cmd = [["youtube-dl", "-o", f"{self.settings.Youtubedl.audioDir}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i", "--playlist-items", f"{numb}", "-x", "--prefer-ffmpeg"], ["--audio-format", "mp3", f"{url}"]]

            floc = [f"--ffmpeg-location", f"{spath}"]
            if self.fdir:
                cmd = cmd[0]+floc+cmd[1]
            else:
                cmd = cmd[0]+cmd[1]

            self.hasCookie(self.aud_cookie_checkbox.isChecked(), cmd)

            self.aud_output_console.insertPlainText("#yt-dl# starting youtube-dl please wait...\n")

            self.process_start(cmd, self.aud_output_console)

            self.running = False
            self.status("Ready.")
            self.tabWidget.setTabText(0, "Audio")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def aud_playlist_bar_toggle(self):
        self.aud_playlist_bar.setEnabled(self.aud_playlist_checkbox.isChecked())
        if(self.aud_playlist_checkbox.isChecked()):
            self.aud_playlist_bar.setStyleSheet("background-color: #909090;")
        else:
            self.aud_playlist_bar.setStyleSheet("background-color: #707070;")

    # region ==========📼VIDEO📼==========
    def Video(self):
        if not self.running:
            self.running = True
            self.status("Busy.")

            self.tabWidget.setTabText(1, "*Video")

            self.vid_output_console.setHtml("")  # clearing the output_console.

            url = self.vid_url_bar.text()
            if self.vid_playlist_checkbox.isChecked():
                numb = self.vid_playlist_bar.text()
            else:
                numb = None

            if(numb is None):
                cmd = [["youtube-dl", "-o", f"{self.settings.Youtubedl.videoDir}%(title)s.%(ext)s", "-f"], ["--no-playlist", f"{url}"]]
            elif(numb == ""):
                cmd = [["youtube-dl", "-o", f"{self.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s", "-f"], ["--yes-playlist", f"{url}"]]
            else:
                cmd = [["youtube-dl", "-o", f"{self.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s", "-f"], ["--yes-playlist", "--playlist-items", f"{numb}", f"{url}"]]

            if self.vid_best_radio.isChecked():
                qual = ["bestvideo+bestaudio"]
            elif self.vid_custom_radio.isChecked():
                qual = [self.vid_quality_bar.text()]
            else:
                qual = ["best"]

            floc = [f"--ffmpeg-location", f"{spath}"]
            if self.fdir:
                cmd = cmd[0]+qual+floc+cmd[1]
            else:
                cmd = cmd[0]+qual+cmd[1]

            self.hasCookie(self.vid_cookie_checkbox.isChecked(), cmd)

            self.process_start(cmd, self.vid_output_console)

            self.running = False
            self.status("Ready.")
            self.tabWidget.setTabText(1, "Video")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def vid_quality(self):
        if not self.running:
            self.running = True
            self.status("Busy.")

            self.vid_output_console.setHtml("")  # clearing the output_console

            url = self.vid_url_bar.text()
            cmd = ["youtube-dl", "-F", "--no-playlist", f"{url}"]

            self.hasCookie(self.vid_cookie_checkbox.isChecked(), cmd)

            self.vid_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

            self.process_start(cmd, self.vid_output_console)

            self.running = False
            self.status("Ready.")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def vid_playlist_bar_toggle(self):
        self.vid_playlist_bar.setEnabled(self.vid_playlist_checkbox.isChecked())
        if(self.vid_playlist_checkbox.isChecked()):
            self.vid_playlist_bar.setStyleSheet("background-color: #909090;")
        else:
            self.vid_playlist_bar.setStyleSheet("background-color: #707070;")

    def vid_quality_bar_toggle(self):
        self.vid_quality_bar.setEnabled(self.vid_custom_radio.isChecked())
        if(self.vid_custom_radio.isChecked()):
            self.vid_quality_bar.setStyleSheet("background-color: #909090;")
        else:
            self.vid_quality_bar.setStyleSheet("background-color: #707070;")

    # region ==========📑SUBS📑==========
    def Subs(self):
        if not self.running:
            self.running = True
            self.status("Busy.")

            self.tabWidget.setTabText(2, "*Subs")

            temp = tempfile.mkdtemp()+os.path.sep

            self.sub_output_console.setHtml("")  # clearing the output_console.

            url = self.sub_url_bar.text()

            cmd = [[], []]

            if self.sub_playlist_checkbox.isChecked():
                if self.sub_playlist_bar.text() == "":
                    cmd[0] = ["youtube-dl", "-o", f"{temp}%(title)s.%(ext)s", "--yes-playlist", "--write-sub", "--write-auto-sub"]
                else:
                    numb = self.sub_playlist_bar.text()
                    cmd[0] = ["youtube-dl", "-o", f"{temp}%(title)s.%(ext)s", "--yes-playlist", "--playlist-items", f"{numb}", "--write-sub", "--write-auto-sub"]
            else:
                cmd[0] = ["youtube-dl", "-o", f"{temp}%(title)s.%(ext)s", "--no-playlist", "--write-sub", "--write-auto-sub"]

            cmd[1] = ["--sub-format", "vtt", "--skip-download", f"{url}"]

            lang = None

            if self.sub_lang_checkbox.isChecked():
                lang = self.sub_lang_bar.text()

            floc = [f"--ffmpeg-location", f"{spath}"]
            if self.fdir:
                if lang is not None:
                    cmd = cmd[0]+lang+floc+cmd[1]
                else:
                    cmd = cmd[0]+floc+cmd[1]
            else:
                if lang is not None:
                    cmd = cmd[0]+lang+cmd[1]
                else:
                    cmd = cmd[0]+cmd[1]

            if self.sub_cookie_checkbox.isChecked():
                if os.path.exists(spath+"cookies.txt"):
                    cmd = cmd+["--cookies", spath+"cookies.txt"]

            self.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

            self.process_start(cmd, self.sub_output_console)

            subpath = glob.glob(f"{temp}*.vtt")
            os.makedirs(self.settings.Youtubedl.videoDir, exist_ok=True)

            for item in subpath:
                namei = os.path.basename(item)
                namei = namei[:-3]
                newsubpath = f"{self.settings.Youtubedl.videoDir}{namei}srt"  # I don't like this fix to a complain about var type
                if os.path.isfile(newsubpath):
                    self.sub_output_console.insertPlainText(f"#yt-dl# file {item} already exists skipping...\n")
                else:
                    cmd = ["-i", f"{item}", f"{newsubpath}"]

                    floc = [f"{spath+os.path.sep+'ffmpeg'}", "-hide_banner"]
                    if self.fdir:
                        cmd = floc+cmd
                    else:
                        cmd = ["ffmpeg", "-hide_banner"]+cmd

                    if self.sub_cookie_checkbox.isChecked():
                        if os.path.exists(spath + "cookies.txt"):
                            cmd = cmd + ["--cookies", spath + "cookies.txt"]

                    self.sub_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")

                    self.process_start(cmd, self.sub_output_console)

            self.running = False
            self.status("Ready.")
            self.tabWidget.setTabText(2, "Subs")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def sub_lang(self):
        if not self.running:
            self.running = True
            self.status("Busy.")

            self.sub_output_console.setHtml("")  # clearing the output_console

            url = self.sub_url_bar.text()
            cmd = ["youtube-dl", "--list-subs", "--no-playlist", f"{url}"]

            if self.sub_cookie_checkbox.isChecked():
                if os.path.exists(spath+"cookies.txt"):
                    cmd = cmd+["--cookies", spath+"cookies.txt"]

            self.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

            self.process_start(cmd, self.sub_output_console)

            self.running = False
            self.status("Ready.")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def sub_playlist_bar_toggle(self):
        self.sub_lang_button.setEnabled(not self.sub_playlist_checkbox.isChecked())
        self.sub_playlist_bar.setEnabled(self.sub_playlist_checkbox.isChecked())
        if(self.sub_playlist_checkbox.isChecked()):
            self.sub_playlist_bar.setStyleSheet("background-color: #909090;")
        else:
            self.sub_playlist_bar.setStyleSheet("background-color: #707070;")

    def sub_lang_bar_toggle(self):
        self.sub_lang_bar.setEnabled(self.sub_lang_checkbox.isChecked())
        if(self.sub_lang_checkbox.isChecked()):
            self.sub_lang_bar.setStyleSheet("background-color: #909090;")
        else:
            self.sub_lang_bar.setStyleSheet("background-color: #707070;")

    # region ==========💿RE-ENCODE💿==========
    def Reencode(self):
        if not self.running:
            self.running = True
            self.status("Busy.")

            self.tabWidget.setTabText(3, "*Re-encode")

            self.ree_output_console.setHtml("")  # clearing the output_console

            location = self.ree_location_bar.text()
            videoc = self.ree_videoc_bar.text()
            videoq = self.ree_videoq_bar.text()
            audioc = self.ree_audioc_bar.text()
            audiob = self.ree_audiob_bar.text()
            append = self.ree_append_bar.text()

            if location[-2:] == os.path.sep+"*":  # whole folder
                VidsToRender = glob.glob(location)
            else:
                VidsToRender = [f"{location}"]
            for video in VidsToRender:
                if os.path.isfile(os.path.splitext(video)[0]+append):
                    self.ree_output_console.insertPlainText(f"#yt-dl# file {video} already exists skipping...\n")
                else:
                    cmd = [["-hwaccel", "auto", "-i", f"{video}", "-map", "0:v?", "-map", "0:a?", "-map", "0:s?"], ["-max_muxing_queue_size", "9999", "-b:v", "0K"], [f"{os.path.splitext(video)[0]+append}"]]

                    # //Video Quality\\#
                    if "," in videoq:
                        VQsplit = videoq.split(",")
                    else:
                        VQsplit = [videoq, videoq, videoq]
                    # //Video Codec\\#
                    if(videoc == "libx265"):
                        VideoCodec = ["-c:v", f"{videoc}"]
                        quality = ["-crf", f"{int(VQsplit[0])-1}", "-qmin", f"{int(VQsplit[1])-1}", "-qmax", f"{int(VQsplit[2])-1}"]
                        Vformat = ["-vf", "format=yuv420p"]
                        cmd = [cmd[0]+VideoCodec+quality+cmd[1]+Vformat, cmd[2]]
                    elif(videoc == "copy"):
                        VideoCodec = [f"-c:v", f"{videoc}"]
                        cmd = [cmd[0]+VideoCodec+cmd[1], cmd[2]]
                    elif(videoc == "remove"):
                        VideoCodec = ["-vn"]
                        cmd = [cmd[0]+VideoCodec+cmd[1], cmd[2]]
                    elif(videoc == "hevc_nvenc"):
                        VideoCodec = ["-c:v", f"{videoc}"]
                        quality = ["-rc:v", "vbr", "-qmin", f"{int(VQsplit[1])}", "-qmax", f"{int(VQsplit[2])}", "-bf", "1"]
                        Vformat = ["-vf", "format=yuv420p"]
                        cmd = [cmd[0]+VideoCodec+quality+cmd[1]+Vformat, cmd[2]]
                    elif(videoc == "h264_nvenc"):
                        VideoCodec = ["-c:v", f"{videoc}"]
                        quality = ["-rc:v", "vbr", "-qmin", f"{int(VQsplit[1])}", "-qmax", f"{int(VQsplit[2])}"]
                        Vformat = ["-vf", "format=yuv420p"]
                        cmd = [cmd[0]+VideoCodec+quality+cmd[1]+Vformat, cmd[2]]
                    else:
                        VideoCodec = ["-c:v", f"{videoc}"]
                        quality = ["-cq", f"{int(VQsplit[0])-1}", "-qmin", f"{int(VQsplit[1])-1}", "-qmax", f"{int(VQsplit[2])-1}"]
                        Vformat = ["-vf", "format=yuv420p"]
                        cmd = [cmd[0]+VideoCodec+quality+cmd[1]+Vformat, cmd[2]]
                    # //Audio\\#
                    if(audioc == "remove"):
                        AudioEverything = ["-an"]
                        cmd = [cmd[0]+AudioEverything, cmd[1]]
                    else:
                        AudioEverything = ["-c:a", f"{audioc}", "-strict", "-2", "-b:a", f"{audiob}"]
                        cmd = [cmd[0]+AudioEverything, cmd[1]]
                    # //Subtitles\\#
                    if(videoc == "remove"):
                        cmd = cmd[0]+cmd[1]
                    else:
                        SubsC = ["-c:s", "copy"]
                        cmd = cmd[0]+SubsC+cmd[1]

                    floc = [f"{spath+os.path.sep+'ffmpeg'}", "-hide_banner"]
                    if self.fdir:
                        cmd = floc+cmd
                    else:
                        cmd = ["ffmpeg", "-hide_banner"]+cmd

                    self.process_start(cmd, self.ree_output_console)

            self.running = False
            self.status("Ready.")
            self.tabWidget.setTabText(3, "Re-encode")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def ree_settings(self):
        if self.ree_settings_combobox.currentIndex() == 4:  # custom
            self.ree_videoc_bar.setText(self.settings.Ffmpeg.videoCodec)
            self.ree_videoq_bar.setText(self.settings.Ffmpeg.videoQuality)
            self.ree_audioc_bar.setText(self.settings.Ffmpeg.audioCodec)
            self.ree_audiob_bar.setText(self.settings.Ffmpeg.audioBitrate)
            self.ree_append_bar.setText(self.settings.Ffmpeg.append)
        elif self.ree_settings_combobox.currentIndex() == 0:  # hevc_opus
            self.ree_videoc_bar.setText("libx265")
            self.ree_videoq_bar.setText("24,24,24")
            self.ree_audioc_bar.setText("opus")
            self.ree_audiob_bar.setText("190k")
            self.ree_append_bar.setText("_hevcopus.mkv")
        elif self.ree_settings_combobox.currentIndex() == 1:  # h264_nvenc
            self.ree_videoc_bar.setText("h264_nvenc")
            self.ree_videoq_bar.setText("24,24,24")
            self.ree_audioc_bar.setText("aac")
            self.ree_audiob_bar.setText("190k")
            self.ree_append_bar.setText("_nvenc.mov")
        elif self.ree_settings_combobox.currentIndex() == 2:  # hevc_nvenc
            self.ree_videoc_bar.setText("hevc_nvenc")
            self.ree_videoq_bar.setText("24,24,24")
            self.ree_audioc_bar.setText("opus")
            self.ree_audiob_bar.setText("190k")
            self.ree_append_bar.setText("_henc.mkv")
        elif self.ree_settings_combobox.currentIndex() == 3:  # mp3
            self.ree_videoc_bar.setText("remove")
            self.ree_videoq_bar.setText("none")
            self.ree_audioc_bar.setText("mp3")
            self.ree_audiob_bar.setText("190k")
            self.ree_append_bar.setText(".mp3")

    def ree_settings_save(self):
        self.settings.Ffmpeg.videoCodec = self.ree_videoc_bar.text()
        self.settings.Ffmpeg.audioCodec = self.ree_audioc_bar.text()
        self.settings.Ffmpeg.videoQuality = self.ree_videoq_bar.text()
        self.settings.Ffmpeg.audioBitrate = self.ree_audiob_bar.text()
        self.settings.Ffmpeg.append = self.ree_append_bar.text()
        self.settings.defaultCodec = self.ree_settings_combobox.currentIndex()
        self.settings.toJson(settingsPath)

    def ree_choose(self):
        self.ree_location_bar.setText(QFileDialog.getOpenFileName()[0])

    # region ==========🔄UPDATE🔄==========
    def update_yt_dl(self):
        cmd = ["git", "pull", "--recurse-submodules"]
        self.process_start(cmd, self.upd_output_console)

    def update_depend(self):
        cmd = [self.settings.Python.python, "-V"]
        self.process_start(cmd, self.upd_output_console)
        pips = self.settings.Python.pip.split(" ")
        cmd = [f"{self.settings.Python.python}", "-m", "pip", "install", "-U", "pip"]
        self.process_start(cmd, self.upd_output_console)
        cmd = pips+["install", "-U", "-r", "req-gui5.txt"]
        self.process_start(cmd, self.upd_output_console)

    def Update(self):
        if not self.running:
            self.running = True
            self.status("Busy.")

            self.tabWidget.setTabText(4, "*Update")

            self.upd_output_console.setHtml("")  # clearing the output_console

            if self.upd_update_combobox.currentIndex() == 1:
                self.update_yt_dl()
            elif self.upd_update_combobox.currentIndex() == 2:
                self.update_depend()
            else:
                self.update_yt_dl()
                self.update_depend()

            self.running = False
            self.status("Ready.")
            self.tabWidget.setTabText(4, "Update")
        else:
            self.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")

    def upd_auto_toggle(self):  # autoupdate is not a thing tho
        self.settings.autoUpdate = not self.settings.autoUpdate
        self.settings.toJson(settingsPath)
        self.upd_auto_button.setText(f"Autoupdate=\"{self.settings.autoUpdate}\"")

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
