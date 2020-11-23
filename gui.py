import sys
import glob, json
import subprocess
import itertools
from PyQt5 import QtWidgets, uic

from call import year, lstupdt, spath, settings

#==========LOAD PATH==========#
def loadpath(s="show"): # Taken directly from call.py, only used to load path, fail miserably if config missing or corrupted.
    global audio
    global videos
    global py
    global pip
    global ydpip
    global aup
    global Vcodec
    global Acodec
    global Vqual
    global Abit
    global fdir
    fh = open(settings, "r")
    try:
        path = json.loads(fh.read())
    except ValueError:
        path = json.loads(fh.read())
    fh.close()
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
    except KeyError:
        print("Oopsie please launch cli to fix") #if a key is not loaded from the current settings there is nothing we can do in the gui for now, lauch cli to fix
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Settings error")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Your setting files is not correct, please run CLI version to fix")
        msg.exec_()
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

class MainWindow(QtWidgets.QMainWindow):    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)

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
                    cmd = [["youtube-dl", "-o", f"{audio}%(title)s.%(ext)s", "--yes-playlist", "-i", "-x", "--prefer-ffmpeg"],["--audio-format", "mp3", f"{url}"]]
                else:
                    cmd = [["youtube-dl", "-o", f"{audio}%(title)s.%(ext)s", "--yes-playlist", "-i", "--playlist-items", f"{numb}", "-x", "--prefer-ffmpeg"],["--audio-format", "mp3", f"{url}"]]

                floc = [f"--ffmpeg-location", f"{spath}"]
                if (fdir == True):
                    cmd = cmd[0]+floc+cmd[1]
                else:
                    cmd = cmd[0]+cmd[1]

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000)
                for line in itertools.chain(process.stdout, process.stderr): 
                    gui = window.isVisible()
                    if gui == False: #if window of the app was closed kill the subrocess.
                        process.terminate()
                    else:
                        line = str(line)
                        line = line[2:-1]
                        if "\\n" in line:
                            line = line.replace("\\n", "\n")
                        if "\\r" in line:
                            line = line.replace("\\r", "\n")
                        if "\\\\" in line:
                            line = line.replace("\\\\","\\")
                        if "\\'" in line:
                            line = line.replace("\\'","'")
                        self.aud_output_console.insertPlainText(line)
                        QtWidgets.QApplication.processEvents()
                        self.scrollbar = self.aud_output_console.verticalScrollBar()
                        self.scrollbar.setValue(self.scrollbar.maximum())
                
                print("\a")
                self.aud_output_console.insertPlainText("Process has finished.")
                QtWidgets.QApplication.processEvents()
                self.scrollbar = self.aud_output_console.verticalScrollBar()
                self.scrollbar.setValue(self.scrollbar.maximum())
                running = False
                status("Ready.")
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Process warning")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("One process already running!")
                msg.exec_()
                
        def playlist_bar_enable():
            self.aud_playlist_bar.setEnabled(self.aud_playlist_checkbox.isChecked())
            if(self.aud_playlist_checkbox.isChecked()):
                self.aud_playlist_bar.setStyleSheet("background-color: #909090;")
            else:
                self.aud_playlist_bar.setStyleSheet("background-color: #707070;")

        #=====AUDIO=====#
        self.aud_download_button.clicked.connect(Audio)
        self.aud_playlist_checkbox.clicked.connect(playlist_bar_enable)
        self.aud_output_console.setHtml("Welcome to yt-dl-gui paste a link and hit download.")

        #=====ABOUT=====#
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