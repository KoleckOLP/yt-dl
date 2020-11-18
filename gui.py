import os, sys
import glob, json
import subprocess
import shlex
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

        def Audio():
            loadpath()
            print(f"{audio}, {fdir}")
            if (fdir == True):
                floc = f"--ffmpeg-location {spath}"
            else:
                floc = ""

            url = self.url_box.text()
            if self.playlist_checkbox.isChecked():
                numb = self.playlist_bar.text()
            else:
                numb = ""

            if(numb == ""):
                lnk = f"-o \"{audio}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg {floc} --audio-format mp3 \"{url}\""
            elif(numb == "1"):
                lnk = f"-o \"{audio}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i -x --prefer-ffmpeg {floc} --audio-format mp3 \"{url}\""
            else:
                lnk = f"-o \"{audio}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i --playlist-items {numb} -x --prefer-ffmpeg {floc} --audio-format mp3 \"{url}\""

            #########################################################
            #   THIS IS THE REAL ISSUE WHY I CAN'T MAKE YT-DL GUI   #
            #########################################################
            '''
            #self.output_console.setHtml("starting youtube-dl please wait...")
            command = shlex.split("youtube-dl "+lnk)
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            output, err = process.communicate()
            self.output_console.setHtml(output.decode("utf-8"))
            print("\a")
            '''

        def playlist_bar_enable():
            self.playlist_bar.setEnabled(self.playlist_checkbox.isChecked())

        #=====AUDIO=====#
        self.download_button.clicked.connect(Audio)
        self.playlist_checkbox.clicked.connect(playlist_bar_enable)

        #=====ABOUT=====#
        self.about_box.setHtml(f"<p style=\"font-size: 20px; white-space: pre\">HorseArmored inc (C){year}<br>"
                              +f"Last updated on: {lstupdt}<br>"
                              +f"My webpage: <a href=\"https://koleckolp.comli.com\">https://koleckolp.comli.com</a><br>"
                              +f"Project page: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://github.com/KoleckOLP/yt-dl</a><br>"
                              +f"need help? ask here: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://discord.gg/W88375j</a><br>"
                              +f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez<br>"
                              +f"                 (C)2011-{year} youtube-dl developers<br>"
                              +f"ffmpeg (C)2000-{year} FFmpeg team</pre></p>")  

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