from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import os, sys, glob, platform

if (platform.system().lower() == "windows"):
    if (int(platform.version().split(".")[0]) < 10):
        from PyQt5 import QtWidgets, uic, QtGui
        from PyQt5.QtWidgets import QMessageBox
        from PyQt5.QtCore import QT_VERSION_STR  #, Qt

try:
    from PyQt6 import QtWidgets, uic, QtGui
    from PyQt6.QtWidgets import QMessageBox
    from PyQt6.QtCore import QT_VERSION_STR  #, Qt
except Exception as e:
    from PyQt5 import QtWidgets, uic, QtGui
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtCore import QT_VERSION_STR  #, Qt
        
# Imports from this project
from release import year, lstupdt, spath, curb, ver, settingsPath, audioDirDefault, videoDirDefault
from gui.Audio import audio, aud_playlist_bar_toggle
from gui.Video import video, vid_quality, vid_playlist_bar_toggle, vid_quality_bar_toggle
from gui.Subs import subs, sub_lang, sub_playlist_bar_toggle
from gui.ReEncode import reencode, ree_settings, ree_settings_save, ree_choose
from gui.Update import update, upd_auto_toggle, upd_button_change
from gui.Settings import set_save, set_load, set_make_script, write_default_json
from shared.ReEncode import reencode_shared_settings
from shared.Config import Settings

# changing python working directory to script location to fix most path issues
os.chdir(os.path.dirname(__file__))

try:
    if (sys.platform.startswith("win")):  # win, linux, darwin, freebsd
        import ctypes
        myappid = 'HorseArmored.yt-dl.gui.'+ver  # Program Sting
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception as e:
    print(e)


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
        self.settings.window_settings.window_width = self.geometry().width()
        self.settings.window_settings.window_height = self.geometry().height()
        self.settings.window_settings.window_pos_x = self.pos().x()
        self.settings.window_settings.window_pos_y = self.pos().y()
        self.settings.to_json(settingsPath)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(f"gui{os.path.sep}gui.ui", self)

        if platform.system().lower() == "windows":
            is_windows_11 = int(platform.version().split('.')[2]) > 20000
            is_qt6 = QT_VERSION_STR[0] == '6'
            color = "#ffffff" if (is_windows_11 and is_qt6) or not is_windows_11 else "#000000"
        else:
            color = "#ffffff"

        self.tabWidget.setStyleSheet(f"""
            QTabBar::tab:selected {{
                background-color: #121212; /* Change to your desired color */
                color: {color}
            }}
            QTabBar::tab {{
                background-color: #383838; /* Color for unselected tabs */
                color: {color}
            }}
        """)

        # !!! show was here before !!!

        self.setAcceptDrops(True)

        # region ===== startup =====

        # ffmpeg detection
        pffmpeg = glob.glob(f"{spath}ffmpeg*")
        pffprobe = glob.glob(f"{spath}ffprobe*")
        if (not pffmpeg and not pffprobe):
            self.floc = False
        else:
            directorySplit = pffmpeg[0]
            directorySplit = directorySplit.split("\\")
            directorySplit = directorySplit[:-1]
            directorySplit = "\\".join(directorySplit)
            self.floc = directorySplit

        # deno detection
        pdeno = glob.glob(f"{spath}deno*")
        if not pdeno:
            self.deno = False
        else:
            self.deno = pdeno[0]

        pgit = glob.glob(f"{spath}git{os.path.sep}bin{os.path.sep}git*")
        if pgit:  # using portable git
            self.gloc = True
        else:  # using non portable git
            self.gloc = False

        if (os.path.exists(settingsPath)):
            try:
                self.settings = Settings.from_json(settingsPath)
            except KeyError as e:
                #print(e)
                if QT_VERSION_STR[0] == '6':
                    self.messagePopup("Settings error", QMessageBox.Icon.Critical, "Your config file is not up to date,\nPress OK to load default config.", self.save_default_config)
                else:
                    self.messagePopup("Settings error", QMessageBox.Critical, "Your config file is not up to date,\nPress OK to load default config.", self.save_default_config)
        else:
            if QT_VERSION_STR[0] == '6':
                self.messagePopup("Settings error", QMessageBox.Icon.Critical, "You are missing a config file,\nPress OK to load default config.", self.save_default_config)
            else:
                self.messagePopup("Settings error", QMessageBox.Critical, "You are missing a config file,\nPress OK to load default config.", self.save_default_config)

        self.setWindowTitle(f"yt-dl {ver}")

        # this code is probably Windows only, and it's ugly af
        python = os.path.dirname(sys.executable)+os.path.sep  # location of the python yt-dl was started from
        ytdlp = glob.glob(f"{python}Scripts{os.path.sep}yt-dlp*")  # check if python that launch yt-dl has yt-dlp
        if (not ytdlp):
            ytdlp = glob.glob(f"{self.settings.python_settings.python[:-6]}Scripts{os.path.sep}yt-dlp*")  # check if user configured python has yt-dlp, specific to Vista build
            if (not ytdlp):
                self.ytex = False
            else:
                self.ytex = [self.settings.python_settings.python, ytdlp[0]]
        else:
            self.ytex = [python+"python", ytdlp[0]]

        # changing size and position of the window
        if self.settings.window_settings.window_width != 0 or self.settings.window_settings.window_height != 0:
            self.resize(self.settings.window_settings.window_width, self.settings.window_settings.window_height)

        if self.settings.window_settings.window_pos_x != 0 or self.settings.window_settings.window_pos_y != 0:
            self.move(self.settings.window_settings.window_pos_x, self.settings.window_settings.window_pos_y)

        self.tabWidget.setCurrentIndex(self.settings.default_tab)  # the code will not get here if settings is undefined.

        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()
        self.activateWindow()

        self.running = False
        self.status("Ready.")
        self.process = ""
        # endregion

        # set fixed width font for consoles.
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
        font.setPointSize(11)      

        # region =====aud_controls=====
        self.aud_folder_button.clicked.connect(lambda: self.openFolder(self.settings.ytdlp_settings.audio_dir))
        self.aud_download_button.clicked.connect(lambda: audio(self))
        self.aud_playlist_checkbox.clicked.connect(lambda: aud_playlist_bar_toggle(self))
        self.aud_cookie_checkbox.setChecked(self.settings.ytdlp_settings.cookie)
        self.aud_output_console.setFont(font)
        self.aud_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Audio) paste a link and hit download.")
        # endregion

        # region =====vid_controls=====
        self.vid_folder_button.clicked.connect(lambda: self.openFolder(self.settings.ytdlp_settings.video_dir))
        self.vid_download_button.clicked.connect(lambda: video(self))
        self.vid_quality_button.clicked.connect(lambda: vid_quality(self))
        self.vid_playlist_checkbox.clicked.connect(lambda: vid_playlist_bar_toggle(self))
        self.vid_custom_radio.toggled.connect(lambda: vid_quality_bar_toggle(self))
        self.vid_cookie_checkbox.setChecked(self.settings.ytdlp_settings.cookie)
        if self.settings.ytdlp_settings.quality == "best":
            self.vid_best_radio.setChecked(True)
        elif self.settings.ytdlp_settings.quality == "normal":
            self.vid_normal_radio.setChecked(True)
        elif self.settings.ytdlp_settings.quality == "custom":
            self.vid_custom_radio.setChecked(True)
        self.vid_best_radio.toggled.connect(lambda: set_save(self))
        self.vid_normal_radio.toggled.connect(lambda: set_save(self))
        self.vid_custom_radio.toggled.connect(lambda: set_save(self))
        self.vid_output_console.setFont(font)
        self.vid_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Video) paste a link and hit download.")
        # endregion

        # region =====sub_controls=====
        self.sub_folder_button.clicked.connect(lambda: self.openFolder(self.settings.ytdlp_settings.video_dir))
        self.sub_download_button.clicked.connect(lambda: subs(self))
        self.sub_lang_button.clicked.connect(lambda: sub_lang(self))
        self.sub_playlist_checkbox.toggled.connect(lambda: sub_playlist_bar_toggle(self))
        self.sub_cookie_checkbox.setChecked(self.settings.ytdlp_settings.cookie)
        self.sub_output_console.setFont(font)
        self.sub_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Subtitles) paste a link and hit download.")
        # endregion

        # region =====ree_controls=====
        for i in range(0, int(reencode_shared_settings(self, "len"))):
            setting = reencode_shared_settings(self, i)
            if setting:
                self.ree_settings_combobox.addItem(setting[5])  # writes name of the setting

        ree_settings(self)  # load option on startup
        self.ree_choose_button.clicked.connect(lambda: ree_choose(self))
        def ree_reencode_action():
            if hasattr(self, 'process') and getattr(self, 'running', False):
                # If running, stop the process
                if hasattr(self, 'process_worker') and hasattr(self.process_worker, 'terminate_process'):
                    self.process_worker.terminate_process()
                self.running = False
                self.ree_reencode_button.setText("Re-encode")
            else:
                reencode(self)
        self.ree_reencode_button.clicked.connect(ree_reencode_action)
        self.ree_folder_button.clicked.connect(lambda: self.openFolder(self.ree_location_bar.text()))
        self.ree_settings_combobox.activated.connect(lambda: ree_settings(self))
        self.ree_settings_button.clicked.connect(lambda: ree_settings_save(self))
        self.ree_output_console.setFont(font)
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
        if self.settings.auto_update:
            self.tabWidget.setCurrentIndex(4)
            update(self)

        self.upd_update_combobox.currentIndexChanged.connect(lambda: upd_button_change(self))
        self.upd_update_button.clicked.connect(lambda: update(self))
        self.upd_auto_button.setText(f"Autoupdate=\"{self.settings.auto_update}\"")
        self.upd_auto_button.clicked.connect(lambda: upd_auto_toggle(self))
        self.upd_output_console.setFont(font)
        self.upd_output_console.append("#yt-dl# Welcome to yt-dl-gui (Update) pick and option and click Update.")
        # endregion

        # region =====set_controls=====
        self.set_loaddef_button.clicked.connect(lambda: write_default_json(self))
        self.set_loadcur_button.clicked.connect(lambda: set_load(self, self.settings.ytdlp_settings.audio_dir, self.settings.ytdlp_settings.video_dir, self.settings.python_settings.python, self.settings.python_settings.pip, self.settings.ytdlp_settings.from_pip, self.settings.auto_update, self.settings.ffmpeg_settings.audio_codec, self.settings.ffmpeg_settings.video_codec, self.settings.ffmpeg_settings.audio_bitrate, self.settings.ffmpeg_settings.video_quality, self.settings.ffmpeg_settings.append, self.settings.default_tab, self.settings.auto_close))
        self.set_folder_button.clicked.connect(lambda: self.openFolder(spath))
        self.set_launch_button.clicked.connect(lambda: set_make_script(self))
        self.set_save_button.clicked.connect(lambda: set_save(self))
        self.set_Tab_combobox.addItem("Audio")  # setting up items in combo list
        self.set_Tab_combobox.addItem("Video")
        self.set_Tab_combobox.addItem("Subs")
        self.set_Tab_combobox.addItem("Re-encode")
        self.set_Tab_combobox.addItem("Update")
        self.set_Tab_combobox.addItem("Settings")
        self.set_Tab_combobox.addItem("About")
        set_load(
            self,
            self.settings.ytdlp_settings.audio_dir,
            self.settings.ytdlp_settings.video_dir,
            self.settings.python_settings.python,
            self.settings.python_settings.pip,
            self.settings.ytdlp_settings.from_pip,
            self.settings.auto_update,
            self.settings.ffmpeg_settings.audio_codec,
            self.settings.ffmpeg_settings.video_codec,
            self.settings.ffmpeg_settings.audio_bitrate,
            self.settings.ffmpeg_settings.video_quality,
            self.settings.ffmpeg_settings.append,
            self.settings.default_tab,
            self.settings.auto_close
        )
        # endregion

        # region ==========🎓ABOUT🎓==========
        self.about_box.setHtml(f"<p style=\"font-size: 18px; white-space: pre\">HorseArmored Inc. (C){year}<br>" +
                               f"Version: {ver} ({curb} branch)<br>" +
                               f"Last updated on: {lstupdt}<br>" +
                               f"My webpage: <a href=\"https://tiny.cc/koleq\">https://tiny.cc/koleq</a><br>" +
                               f"Project page: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://github.com/KoleckOLP/yt-dl</a><br>" +
                               f"need help? ask here: <a href=\"https://discord.gg/W88375j\">https://discord.gg/W88375j</a><br>" +
                               f"yt-dlp (C)2021-{year} yt-dlp contributors<br>"
                               f"ffmpeg (C)2000-{year} FFmpeg team<br>" +
                               f"Thanks to <a href=\"https://github.com/kangalioo\">kangalioo</a> who always helps a ton!<br>" +
                               f"You can read the changelog: <a href=\"https://github.com/KoleckOLP/yt-dl/blob/testing/changelog.md\">here</a></pre></p>")
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
                self.save_default_config("ok")
            else:
                sys.exit()

    def save_default_config(self, i):  # only exists for pyqt5 support, not needed in pyqt6
        if QT_VERSION_STR[0] == '6':
            text = i
        else:
            text: str = i.text().lower()
        if "ok" in text:
            write_default_json(self)
        else:
            sys.exit()

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
        if (sys.platform.startswith("win")):
            os.startfile(loc)  # does not work on macOS, and codefactor is mad about this.
        elif (sys.platform.startswith("darwin") or sys.platform.startswith("haiku")):
            os.system(f"open {loc}")  # codefactor is also mad about this.
        elif ((sys.platform.startswith("linux")) ("bsd" in sys.platform)):
            os.system(f"xdg-open {loc}")  # I was lead astray by Ubuntu having open command Fedora and other distros doesn't
        else:  # platforms that are not haiku linux macOS or Windows
            print(f"sorry this platform is not supported yet. {sys.platform}")
    # endregion


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec()
