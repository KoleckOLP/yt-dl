from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import os
import sys
import glob

try:
    from PyQt6 import QtWidgets, uic
    from PyQt6.QtWidgets import QMessageBox, QApplication
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
from gui.ReEncode import Reencode, ree_settings, ree_settings_save, ree_choose
from gui.Update import Update, upd_auto_toggle
from gui.Settings import set_save, set_load, set_makeScript, WriteDefaultJson
from shared.ReEncode import reencode_shared_settings
from shared.Config import Settings

# changing python working directory to script location to fix most path issues
os.chdir(os.path.dirname(__file__))

if (sys.platform.startswith("win")):  # win, linux, darwin, freebsd
    import ctypes
    myappid = 'HorseArmored.yt-dl.gui.'+ver  # Program Sting
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

    def closeEvent(self, e):  # when closing the app it's size and position gets saved, there alsoe has to be "e" even if it's not used or it throws an error
        self.settings.Window.windowWidth = self.geometry().width()
        self.settings.Window.windowHeight = self.geometry().height()
        self.settings.Window.windowPosX = self.pos().x()
        self.settings.Window.windowPosY = self.pos().y()
        self.settings.toJson(settingsPath)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(f"gui{os.path.sep}gui.ui", self)

        self.show()

        self.setAcceptDrops(True)

        # region ===== startup =====
        pffmpeg = glob.glob(f"{spath}ffmpeg*")
        pffprobe = glob.glob(f"{spath}ffprobe*")
        if (not pffmpeg and not pffprobe):
            self.floc = False
        else:  # THis code is absolutely terrible :)
            directorySplit = pffmpeg[0]
            directorySplit = directorySplit.split("\\")
            directorySplit = directorySplit[:-1]
            directorySplit = "\\".join(directorySplit)
            self.floc = directorySplit

        # this code is probably Windows only, and it's ugly af
        pytonLoc = os.path.dirname(sys.executable)+os.path.sep
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        youtubedl = glob.glob(f"{pytonLoc}Scripts{os.path.sep}yt-dlp*")
        if (not youtubedl):
            self.ytex = False
        else:
            self.ytex = [f"{pythonw}", f"{pytonLoc}Scripts{os.path.sep}yt-dlp.exe"]

        if (os.path.exists(settingsPath)):
            try:
                self.settings = Settings.fromJson(settingsPath)
            except KeyError:
                if QT_VERSION_STR[0] == '6':
                    self.messagePopup("Settings error", QMessageBox.Icon.Critical, "Your config file is not up to date,\nPress OK to load default config.", self.SaveDefaultConfig)
                else:
                    self.messagePopup("Settings error", QMessageBox.Critical, "YYour config file is not up to date,\nPress OK to load default config.", self.SaveDefaultConfig)
        else:
            if QT_VERSION_STR[0] == '6':
                self.messagePopup("Settings error", QMessageBox.Icon.Critical, "You are missing a config file,\nPress OK to load default config.", self.SaveDefaultConfig)
            else:
                self.messagePopup("Settings error", QMessageBox.Critical, "You are missing a config file,\nPress OK to load default config.", self.SaveDefaultConfig)

        self.setWindowTitle(f"yt-dl {ver}")

        # changing size and position of the window
        if self.settings.Window.windowWidth != 0 or self.settings.Window.windowHeight != 0:
            self.resize(self.settings.Window.windowWidth, self.settings.Window.windowHeight)

        if self.settings.Window.windowPosX != 0 or self.settings.Window.windowPosY != 0:
            self.move(self.settings.Window.windowPosX, self.settings.Window.windowPosY)

        self.tabWidget.setCurrentIndex(self.settings.defaultTab)  # the code will not get here if settings is undefined.

        self.running = False
        self.status("Ready.")
        self.process = ""
        # endregion

        # region =====aud_controls=====
        self.aud_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.audioDir))
        self.aud_download_button.clicked.connect(lambda: Audio(self))
        self.aud_playlist_checkbox.clicked.connect(lambda: aud_playlist_bar_toggle(self))
        self.aud_cookie_checkbox.setChecked(self.settings.Youtubedl.cookie)
        self.aud_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Audio) paste a link and hit download.")
        # endregion

        # region =====vid_controls=====
        self.vid_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.vid_download_button.clicked.connect(lambda: Video(self))
        self.vid_quality_button.clicked.connect(lambda: vid_quality(self))
        self.vid_playlist_checkbox.clicked.connect(lambda: vid_playlist_bar_toggle(self))
        self.vid_custom_radio.toggled.connect(lambda: vid_quality_bar_toggle(self))
        self.vid_cookie_checkbox.setChecked(self.settings.Youtubedl.cookie)
        self.vid_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Video) paste a link and hit download.")
        # endregion

        # region =====sub_controls=====
        self.sub_folder_button.clicked.connect(lambda: self.openFolder(self.settings.Youtubedl.videoDir))
        self.sub_download_button.clicked.connect(lambda: Subs(self))
        self.sub_lang_button.clicked.connect(lambda: sub_lang(self))
        self.sub_playlist_checkbox.toggled.connect(lambda: sub_playlist_bar_toggle(self))
        self.sub_cookie_checkbox.setChecked(self.settings.Youtubedl.cookie)
        self.sub_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Subtitles) paste a link and hit download.")
        # endregion

        # region =====ree_controls=====
        for i in range(0, int(reencode_shared_settings(self, "len"))):
            setting = reencode_shared_settings(self, i)
            if setting:
                self.ree_settings_combobox.addItem(setting[5])  # writes name of the setting

        ree_settings(self)  # load option on startup
        self.ree_choose_button.clicked.connect(lambda: ree_choose(self))
        self.ree_reencode_button.clicked.connect(lambda: Reencode(self))
        self.ree_folder_button.clicked.connect(lambda: self.openFolder(self.ree_location_bar.text()))
        self.ree_settings_combobox.activated.connect(lambda: ree_settings(self))
        self.ree_settings_button.clicked.connect(lambda: ree_settings_save(self))
        self.ree_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Re-encode) paste a link and hit download.")
        self.ree_location_bar.setAcceptDrops(True)
        # endregion

        # region ======upd_controls======
        self.upd_update_combobox.addItem("All")  # setting up items in combo list
        self.upd_update_combobox.addItem("yt-dl")
        self.upd_update_combobox.addItem("Dependencies")
        self.upd_update_combobox.addItem("List versions")
        if (sys.platform.startswith("haiku")):
            self.upd_update_combobox.setCurrentIndex(1)

        QtWidgets.QApplication.processEvents()
        if self.settings.autoUpdate:
            self.tabWidget.setCurrentIndex(4)
            Update(self)

        self.upd_update_button.clicked.connect(lambda: Update(self))
        self.upd_auto_button.setText(f"Autoupdate=\"{self.settings.autoUpdate}\"")
        self.upd_auto_button.clicked.connect(lambda: upd_auto_toggle(self))
        self.upd_output_console.append("#yt-dl# Welcome to yt-dl-gui (Update) pick and option and click Update.")
        # endregion

        # region =====set_controls=====
        self.set_loaddef_button.clicked.connect(lambda: WriteDefaultJson(self))
        self.set_loadcur_button.clicked.connect(lambda: set_load(self, self.settings.Youtubedl.audioDir, self.settings.Youtubedl.videoDir, self.settings.Python.python, self.settings.Python.pip, self.settings.Youtubedl.fromPip, self.settings.autoUpdate, self.settings.Ffmpeg.audioCodec, self.settings.Ffmpeg.videoCodec, self.settings.Ffmpeg.audioBitrate, self.settings.Ffmpeg.videoQuality, self.settings.Ffmpeg.append, self.settings.defaultTab))
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
        self.about_box.setHtml(f"<p style=\"font-size: 18px; white-space: pre\">HorseArmored Inc. (C){year}<br>" +
                               f"Version: {ver} gui ({curb} branch)<br>" +
                               f"Last updated on: {lstupdt}<br>" +
                               f"My webpage: <a href=\"https://koleckolp.comli.com\">https://koleckolp.comli.com</a><br>" +
                               f"Project page: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://github.com/KoleckOLP/yt-dl</a><br>" +
                               f"need help? ask here: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://discord.gg/W88375j</a><br>" +
                               f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez<br>" +
                               f"                 (C)2011-{year} youtube-dl developers<br>" +
                               f"ffmpeg (C)2000-{year} FFmpeg team<br>" +
                               f"Thanks to <a href=\"https://github.com/kangalioo\">kangalioo</a> who always helps a ton!<br>" +
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
            WriteDefaultJson(self)
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
    def openFolder(loc: str):
        loc = os.path.dirname(loc)
        if not os.path.exists(loc):
            loc = "." + os.path.sep  # if path does not exist open installation folder
        os.startfile(loc)  # should open in default application TODO: test on Haiku, MacOS, Linux
    # endregion


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec()
