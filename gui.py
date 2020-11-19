import sys
import glob, json
import subprocess
import itertools
from PyQt5 import QtWidgets, uic

from call import year, lstupdt, spath, settings

#==========LOAD PATH==========#
def loadpath(s="show"):
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
        print("issues")
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
        loadpath()
        print(audio)

        def Audio():
            self.output_console.setHtml("") #clearing the output_console
            loadpath()

            floc = []
            if (fdir == True):
                floc = [f"--ffmpeg-location", f"{spath}"]
            else:
                floc = ["", ""]

            url = self.url_box.text()
            if self.playlist_checkbox.isChecked():
                numb = self.playlist_bar.text()
            else:
                numb = None

            if(numb == None):
                cmd = ["youtube-dl", "-o", f"{audio}\%(title)s.%(ext)s", "--no-playlist", "-x", "--prefer-ffmpeg", f"{floc[0]}", f"{floc[1]}", "--audio-format", "mp3", f"{url}"]
                print("0")
            elif(numb == ""):
                cmd = ["youtube-dl", "-o", f"{audio}\%(title)s.%(ext)s", "--yes-playlist", "-i", "-x", "--prefer-ffmpeg", f"{floc[0]}", f"{floc[1]}", "--audio-format", "mp3", f"{url}"]
                print("1")
            else:
                cmd = ["youtube-dl", "-o", f"{audio}\%(title)s.%(ext)s", "--yes-playlist", "-i", "--playlist-items", f"{numb}", "-x", "--prefer-ffmpeg", f"{floc[0]}", f"{floc[1]}", "--audio-format", "mp3", f"{url}"]
                print("2")

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in itertools.chain(process.stdout, process.stderr): 
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
                self.output_console.insertPlainText(line)
                QtWidgets.QApplication.processEvents()
                self.scrollbar = self.output_console.verticalScrollBar()
                self.scrollbar.setValue(self.scrollbar.maximum())
                QtWidgets.QApplication.processEvents()
            
            print("\a")
            self.output_console.insertPlainText("Command Execution ended.")
            QtWidgets.QApplication.processEvents()
            self.scrollbar = self.output_console.verticalScrollBar()
            self.scrollbar.setValue(self.scrollbar.maximum())
            QtWidgets.QApplication.processEvents()
                
                    


        def playlist_bar_enable():
            self.playlist_bar.setEnabled(self.playlist_checkbox.isChecked())
            if(self.playlist_checkbox.isChecked()):
                self.playlist_bar.setStyleSheet("background-color: #909090;")
            else:
                self.playlist_bar.setStyleSheet("background-color: #707070;")

        #=====AUDIO=====#
        self.download_button.clicked.connect(Audio)
        self.playlist_checkbox.clicked.connect(playlist_bar_enable)
        #self.output_console.setHtml("Welcome to yt-dl-gui paste a link and hit download.")

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

'''
app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("gui.ui")
window.show()
app.exec()
'''