import os
import sys
import glob
import subprocess
from typing import List
try:
    from PyQt6 import QtWidgets, uic
    from PyQt6.QtWidgets import QMessageBox
    from PyQt6.QtCore import QT_VERSION_STR
except ModuleNotFoundError:
    from PyQt5 import QtWidgets, uic
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtCore import QT_VERSION_STR
# Imports from this project
from release import year, lstupdt, spath, curb, ver, settingsPath, audioDirDefault, videoDirDefault
from gui.Audio import Audio, aud_playlist_bar_toggle
from gui.Video import Video, vid_quality, vid_playlist_bar_toggle, vid_quality_bar_toggle
from gui.Subs import Subs, sub_lang, sub_playlist_bar_toggle
from gui.ReEncode import Reencode, ree_settings, ree_color, ree_settings_save, ree_choose
from gui.Update import Update, upd_auto_toggle
from gui.Settings import set_save, set_load, set_makeScript
from Config import Settings

if (sys.platform.startswith("win")):  # win, linux, darwin, freebsd
    import ctypes
    myappid = 'HorseArmored.yt-dl.gui5.'+ver  # Program Sting
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainWindow(QtWidgets.QMainWindow):
    # region ===== drag & drop =====
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
    # endregion

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(f"gui{os.path.sep}gui5.ui", self)

        self.show()

        self.setAcceptDrops(True)

        # region ===== startup =====
        pffmpeg = glob.glob(f"{spath}/ffmpeg*")
        pffprobe = glob.glob(f"{spath}/ffprobe*")
        if (not pffmpeg and not pffprobe):
            self.floc = False
        else:
            self.floc = spath

        if (os.path.exists(settingsPath)):
            self.settings = Settings.fromJson(settingsPath)
        else:
            if QT_VERSION_STR[0] == '6':
                self.messagePopup("Settings error", QMessageBox.Icon.Critical, "You are missing a config file,\nPress OK to load default config.", self.SaveDefaultConfig)
            else:
                self.messagePopup("Settings error", QMessageBox.Critical, "You are missing a config file,\nPress OK to load default config.", self.SaveDefaultConfig)

        self.setWindowTitle(f"yt-dl {ver}")

        self.tabWidget.setCurrentIndex(self.settings.defaultTab)  # the code will not get here if settings is undefined.

        self.running = False
        self.status("Ready.")
        self.process = ""
        # endregion

        # region =====aud_controls=====
        self.aud_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.audioDir))
        self.aud_download_button.clicked.connect(lambda: Audio(self))
        self.aud_playlist_checkbox.clicked.connect(lambda: aud_playlist_bar_toggle(self))
        self.aud_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Audio) paste a link and hit download.")
        # endregion

        # region =====vid_controls=====
        self.vid_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.vid_download_button.clicked.connect(lambda: Video(self))
        self.vid_quality_button.clicked.connect(lambda: vid_quality(self))
        self.vid_playlist_checkbox.clicked.connect(lambda: vid_playlist_bar_toggle(self))
        self.vid_custom_radio.toggled.connect(lambda: vid_quality_bar_toggle(self))
        self.vid_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Video) paste a link and hit download.")
        # endregion

        # region =====sub_controls=====
        self.sub_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.sub_download_button.clicked.connect(lambda: Subs(self))
        self.sub_lang_button.clicked.connect(lambda: sub_lang(self))
        self.sub_playlist_checkbox.toggled.connect(lambda: sub_playlist_bar_toggle(self))
        self.sub_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Subtitles) paste a link and hit download.")
        # endregion

        # region =====ree_controls=====
        self.ree_settings_combobox.addItem("hevc_opus")  # setting up items in combo list
        self.ree_settings_combobox.addItem("h264_nvenc")
        self.ree_settings_combobox.addItem("hevc_nvenc")
        self.ree_settings_combobox.addItem("mp3")
        self.ree_settings_combobox.addItem("mjpeg_pcm")
        self.ree_settings_combobox.addItem("custom")
        self.ree_settings_combobox.setCurrentIndex(self.settings.defaultCodec)
        self.ree_settings_combobox.currentIndexChanged.connect(lambda: ree_color(self))
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

        # region ======upd_controls======
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
        self.upd_auto_button.setText(f"Autoupdate=\"{self.settings.autoUpdate}\"")
        self.upd_auto_button.clicked.connect(lambda: upd_auto_toggle(self))
        pyVer = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
        self.upd_output_console.setHtml(f"yt-dl {ver}, python {pyVer}, qt {QT_VERSION_STR}")
        # endregion

        # region =====set_controls=====
        self.set_loadcur_button.clicked.connect(lambda: set_load(self, self.settings.Youtubedl.audioDir, self.settings.Youtubedl.videoDir, self.settings.Python.python, self.settings.Python.pip, self.settings.Youtubedl.fromPip, self.settings.autoUpdate, self.settings.Ffmpeg.audioCodec, self.settings.Ffmpeg.videoCodec, self.settings.Ffmpeg.audioBitrate, self.settings.Ffmpeg.videoQuality, self.settings.Ffmpeg.append, self.settings.defaultTab))
        self.set_loaddef_button.clicked.connect(lambda: set_load(self, audioDirDefault, videoDirDefault, "python", "pip", True, False, "opus", "libx265", "190k", "24,24,24", "_custom.mkv", 0))
        self.set_folder_button.clicked.connect(lambda: self.openFolder(spath))
        self.set_launch_button.clicked.connect(lambda: set_makeScript(self))
        self.set_save_button.clicked.connect(lambda: set_save(self))
        self.set_Tab_combobox.addItem("Audio")  # setting up items in combo list
        self.set_Tab_combobox.addItem("Video")
        self.set_Tab_combobox.addItem("Subs")
        self.set_Tab_combobox.addItem("Re-encode")
        self.set_Tab_combobox.addItem("Update")
        self.set_Tab_combobox.addItem("Settings")
        self.set_Tab_combobox.addItem("About")
        set_load(self, self.settings.Youtubedl.audioDir, self.settings.Youtubedl.videoDir, self.settings.Python.python, self.settings.Python.pip, self.settings.Youtubedl.fromPip, self.settings.autoUpdate, self.settings.Ffmpeg.audioCodec, self.settings.Ffmpeg.videoCodec, self.settings.Ffmpeg.audioBitrate, self.settings.Ffmpeg.videoQuality, self.settings.Ffmpeg.append, self.settings.defaultTab)
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

    # region ===== startup =====
    def messagePopup(self, title, icon, text, callf=None):
        msg = QMessageBox()  # Pylance is being stupid, I had to disable Type checking.
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(text)
        if callf is not None:
            if QT_VERSION_STR[0] == '6':
                msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            else:
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.buttonClicked.connect(callf)
        button = msg.exec()

        if QT_VERSION_STR[0] == '6':
            if button == QMessageBox.StandardButton.Ok:
                self.SaveDefaultConfig("ok")
            else:
                exit()

    def SaveDefaultConfig(self, i):  # only exists for pyqt5 support, not needed in pyqt6
        if QT_VERSION_STR[0] == '6':
            text = i
        else:
            text: str = i.text().lower()
        if "ok" in text:
            self.settings = Settings.loadDefault()
            self.settings.toJson(settingsPath)
        else:
            exit()

    enabledColor = "#383838"
    disabledColor = "#242424"
    # endregion

    # region ===== used by most =====
    def status(self, s=""):  # shows status message and changes color of the status bar.
        self.statusBar().showMessage(s)
        if s == "Ready.":
            self.statusBar().setStyleSheet("background-color: #00BB00")
        elif s == "Busy.":
            self.statusBar().setStyleSheet("background-color: #FF6600")
        else:
            self.statusBar().setStyleSheet("background-color: #A9A9A9")

    @staticmethod
    def process_start(cmd: List[str], output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", output_clear: bool = True, process_name: str = "youtube_dl"):
        if not window.running:
            window.running = True
            window.status("Busy.")
            download_button.setText("Stop!")
            tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
            window.tabWidget.setTabText(window.tabWidget.currentIndex(), "*"+tabName)

            if output_clear:
                output_console.setHtml("")  # clearing the output_console
            output_console.insertPlainText(f"#yt-dl# starting {process_name} please wait...\n")

            if (sys.platform.startswith("win")):  # (os.name == "nt"):
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000, universal_newlines=True, encoding="utf8")  # this one does not check if another process is running
            else:  # (sys.platform.startswith(("linux", "darwin", "freebsd"))): #(os.name == "posix"): #other oeses should be fine with this
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, errors="ignore")
            return process
        else:
            process.terminate()
            window.running = False

    @staticmethod
    def process_output(output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", button_text: str = "Download"):
        if window.running:
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
            download_button.setText(button_text)
            window.running = False
            window.status("Ready.")
            tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
            window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
            QtWidgets.QApplication.processEvents()
            scrollbar = output_console.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    @staticmethod
    def openFolder(loc: str):
        loc = os.path.dirname(loc)
        if not os.path.exists(loc):
            os.makedirs(loc, exist_ok=True)
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
    # endregion


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec()
