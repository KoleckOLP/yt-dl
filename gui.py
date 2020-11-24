import sys
import glob, json
import subprocess
import itertools
from PyQt5 import QtWidgets, uic

from call import year, lstupdt, spath, settings  

class MainWindow(QtWidgets.QMainWindow):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)

        def MessagePopup(title, icon, text):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(title)
            msg.setIcon(icon)
            msg.setText(text)
            msg.exec_()

        #==========LOAD PATH==========#
        def loadpath(s="show"): # Fixed version from call.py display's mesage boxes
            global audio, videos, py, pip, ydpip, aup, Vcodec, Acodec, Vqual, Abit, fdir #exposing all settings to the rest of the program.
            try:
                fh = open(settings, "r") #opens file if there is any
                try:
                    path = json.loads(fh.read()) #loads json values if it's a valid json
                    try:
                        path["audio"]
                        path["videos"]
                        path["py"]
                        path["pip"]
                        path["ydpip"]
                        path["aup"]
                        path["Vcodec"]
                        path["Acodec"]
                        path["Vqual"]
                        path["Abit"]
                    except KeyError: #if keys are missing
                        MessagePopup("Settings error", QtWidgets.QMessageBox.Critical, "Your config file is not compatible with this version.\n(run cli to fix)")
                        exit(0)
                    else:
                        audio = path["audio"]
                        videos = path["videos"]
                        py = path["py"]
                        pip = path["pip"]
                        ydpip = path["ydpip"]
                        aup = path["aup"]
                        Vcodec = path["Vcodec"]
                        Acodec = path["Acodec"]
                        Vqual = path["Vqual"]
                        Abit = path["Abit"]

                    pffmpeg = glob.glob(f"{spath}/ffmpeg*")
                    pffprobe = glob.glob(f"{spath}/ffprobe*")
                    if (not pffmpeg and not pffprobe):
                        fdir = False
                    else:
                        fdir = True
                except ValueError: #if json not valid
                    MessagePopup("Settings error", QtWidgets.QMessageBox.Critical, "Your config file is corrupted.\n(run cli to fix)")
                fh.close()
            except FileNotFoundError: #if file does not exist
                MessagePopup("Settings error", QtWidgets.QMessageBox.Critical, "You are missing a config file,\n(run cli to fix)")
                exit(0)

        def status( s=""): #shows status message and changes color of the status bar.
            self.statusBar().showMessage(s)
            if s == "Ready.":
                self.statusBar().setStyleSheet("background-color: #00BB00")
            elif s == "Busy.":
                self.statusBar().setStyleSheet("background-color: #FF6600")
            else:
                self.statusBar().setStyleSheet("background-color: #A9A9A9")

        loadpath()

        global running
        running = False
        status("Ready.")

        #==========🎶AUDIO🎶==========#
        def Audio():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.aud_output_console.setHtml("") #clearing the output_console

                url = self.aud_url_bar.text()
                if self.aud_playlist_checkbox.isChecked():
                    numb = self.aud_playlist_bar.text()
                else:
                    numb = None

                if(numb == None):
                    cmd = [["youtube-dl", "-o", f"{audio}%(title)s.%(ext)s", "--no-playlist", "-x", "--prefer-ffmpeg"],["--audio-format", "mp3", f"{url}"]]
                elif(numb == ""):
                    cmd = [["youtube-dl", "-o", f"{audio}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i", "-x", "--prefer-ffmpeg"],["--audio-format", "mp3", f"{url}"]]
                else:
                    cmd = [["youtube-dl", "-o", f"{audio}%(playlist_index)s. %(title)s.%(ext)s", "--yes-playlist", "-i", "--playlist-items", f"{numb}", "-x", "--prefer-ffmpeg"],["--audio-format", "mp3", f"{url}"]]

                floc = [f"--ffmpeg-location", f"{spath}"]
                if (fdir == True):
                    cmd = cmd[0]+floc+cmd[1]
                else:
                    cmd = cmd[0]+cmd[1]

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000)
                for c in iter(lambda: process.stdout.read(1), b''):
                    gui = window.isVisible()
                    if gui == False: #if window of the app was closed kill the subrocess.
                        process.terminate()
                    else:
                        c = str(c)
                        c = c[2:-1]
                        if "\\n" in c:
                            c = c.replace("\\n", "\n")
                        if "\\r" in c:
                            c = c.replace("\\r", "\n")
                        if "\\\\" in c:
                            c = c.replace("\\\\","\\")
                        if "\\'" in c:
                            c = c.replace("\\'","'")
                        self.aud_output_console.insertPlainText(c)
                        self.scrollbar = self.aud_output_console.verticalScrollBar()
                        self.scrollbar.setValue(self.scrollbar.maximum())
                        QtWidgets.QApplication.processEvents()
                
                print("\a")
                self.aud_output_console.insertPlainText("Process has finished.")
                QtWidgets.QApplication.processEvents()
                self.scrollbar = self.aud_output_console.verticalScrollBar()
                self.scrollbar.setValue(self.scrollbar.maximum())
                running = False
                status("Ready.")
            else:
                MessagePopup("Process warning", QtWidgets.QMessageBox.Warning, "One process already running!")
                
        def aud_playlist_bar_toggle():
            self.aud_playlist_bar.setEnabled(self.aud_playlist_checkbox.isChecked())
            if(self.aud_playlist_checkbox.isChecked()):
                self.aud_playlist_bar.setStyleSheet("background-color: #909090;")
            else:
                self.aud_playlist_bar.setStyleSheet("background-color: #707070;")

        #=====aud_controlls=====#
        self.aud_download_button.clicked.connect(Audio)
        self.aud_playlist_checkbox.clicked.connect(aud_playlist_bar_toggle)
        self.aud_output_console.setHtml("Welcome to yt-dl-gui (Audio) paste a link and hit download.")

        #==========📼VIDEO📼==========#
        def Video():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.vid_output_console.setHtml("") #clearing the output_console.

                url = self.vid_url_bar.text()
                if self.vid_playlist_checkbox.isChecked():
                    numb = self.vid_playlist_bar.text()
                else:
                    numb = None

                if(numb == None):
                    cmd = [["youtube-dl", "-o", f"{videos}%(title)s.%(ext)s", "-f"],["--no-playlist", f"{url}"]]
                elif(numb == ""):
                    cmd = [["youtube-dl", "-o", f"{videos}%(playlist_index)s. %(title)s.%(ext)s", "-f"],["--yes-playlist", f"{url}"]]
                else:
                    cmd = [["youtube-dl", "-o", f"{videos}%(playlist_index)s. %(title)s.%(ext)s", "-f"],["--yes-playlist", "--playlist-items", f"{numb}", f"{url}"]]

                if self.vid_best_radio.isChecked():
                    qual = ["bestvideo+bestaudio"]
                elif self.vid_custom_radio.isChecked():
                    qual = [self.vid_quality_bar.text()]
                else:
                    qual = ["best"]

                floc = [f"--ffmpeg-location", f"{spath}"]
                if (fdir == True):
                    cmd = cmd[0]+qual+floc+cmd[1]
                else:
                    cmd = cmd[0]+qual+cmd[1]

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000)
                for c in iter(lambda: process.stdout.read(1), b''):
                    gui = window.isVisible()
                    if gui == False: #if window of the app was closed kill the subrocess.
                        process.terminate()
                    else:
                        c = str(c)
                        c = c[2:-1]
                        if "\\n" in c:
                            c = c.replace("\\n", "\n")
                        if "\\r" in c:
                            c = c.replace("\\r", "\n")
                        if "\\\\" in c:
                            c = c.replace("\\\\","\\")
                        if "\\'" in c:
                            c = c.replace("\\'","'")
                        self.vid_output_console.insertPlainText(c)
                        self.scrollbar = self.vid_output_console.verticalScrollBar()
                        self.scrollbar.setValue(self.scrollbar.maximum())
                        QtWidgets.QApplication.processEvents()
                
                print("\a")
                self.vid_output_console.insertPlainText("Process has finished.")
                QtWidgets.QApplication.processEvents()
                self.scrollbar = self.vid_output_console.verticalScrollBar()
                self.scrollbar.setValue(self.scrollbar.maximum())
                running = False
                status("Ready.")
            else:
                MessagePopup("Process warning", QtWidgets.QMessageBox.Warning, "One process already running!")

        def vid_quality():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.vid_output_console.setHtml("") #clearing the output_console

                url = self.vid_url_bar.text()
                cmd = ["youtube-dl", "-F", "--no-playlist", f"{url}"]

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000)
                for c in iter(lambda: process.stdout.read(1), b''):
                    gui = window.isVisible()
                    if gui == False: #if window of the app was closed kill the subrocess.
                        process.terminate()
                    else:
                        c = str(c)
                        c = c[2:-1]
                        if "\\n" in c:
                            c = c.replace("\\n", "\n")
                        if "\\r" in c:
                            c = c.replace("\\r", "\n")
                        if "\\\\" in c:
                            c = c.replace("\\\\","\\")
                        if "\\'" in c:
                            c = c.replace("\\'","'")
                        self.vid_output_console.insertPlainText(c)
                        self.scrollbar = self.vid_output_console.verticalScrollBar()
                        self.scrollbar.setValue(self.scrollbar.maximum())
                        QtWidgets.QApplication.processEvents()
                
                print("\a")
                self.vid_output_console.insertPlainText("Process has finished.")
                QtWidgets.QApplication.processEvents()
                self.scrollbar = self.vid_output_console.verticalScrollBar()
                self.scrollbar.setValue(self.scrollbar.maximum())
                running = False
                status("Ready.")
            else:
                MessagePopup("Process warning", QtWidgets.QMessageBox.Warning, "One process already running!")

        def vid_playlist_bar_toggle():
            self.vid_playlist_bar.setEnabled(self.vid_playlist_checkbox.isChecked())
            if(self.vid_playlist_checkbox.isChecked()):
                self.vid_playlist_bar.setStyleSheet("background-color: #909090;")
            else:
                self.vid_playlist_bar.setStyleSheet("background-color: #707070;")

        def vid_quality_bar_toggle():
            self.vid_quality_bar.setEnabled(self.vid_custom_radio.isChecked())
            if(self.vid_custom_radio.isChecked()):
                self.vid_quality_bar.setStyleSheet("background-color: #909090;")
            else:
                self.vid_quality_bar.setStyleSheet("background-color: #707070;")

        #=====vid_controlls=====#
        self.vid_download_button.clicked.connect(Video)
        self.vid_quality_button.clicked.connect(vid_quality)
        self.vid_playlist_checkbox.clicked.connect(vid_playlist_bar_toggle)
        self.vid_custom_radio.toggled.connect(vid_quality_bar_toggle)
        self.vid_output_console.setHtml("Welcome to yt-dl-gui (Video) paste a link and hit download.")

        #==========🎓ABOUT🎓==========#
        self.about_box.setHtml(f"<p style=\"font-size: 20px; white-space: pre\">HorseArmored inc (C){year}<br>"
                              +f"Last updated on: {lstupdt}<br>"
                              +f"My webpage: <a href=\"https://koleckolp.comli.com\">https://koleckolp.comli.com</a><br>"
                              +f"Project page: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://github.com/KoleckOLP/yt-dl</a><br>"
                              +f"need help? ask here: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://discord.gg/W88375j</a><br>"
                              +f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez<br>"
                              +f"                 (C)2011-{year} youtube-dl developers<br>"
                              +f"ffmpeg (C)2000-{year} FFmpeg team<br>"
                              +f"You can read the changelog: <a href=\"https://github.com/KoleckOLP/yt-dl/blob/master/whatsnew.md\">here</a></pre></p>")  
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()