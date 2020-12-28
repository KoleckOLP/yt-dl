import sys, os
import glob, json
import subprocess
import tempfile
from datetime import datetime
from PySide6 import QtWidgets, QtUiTools, QtGui
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
if(os.name == 'nt'):
    import ctypes
    myappid = 'ArmoredMobilePony.yt-dl.gui.2.1.8' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainWindow(QtWidgets.QMainWindow):    
    def init(self):
        year = datetime.now().year
        lstupdt = "2020-12-28" #I keep forgetting to update this, in C# there was build date.
        spath = sys.path[0]+os.path.sep #path of the yt-dl dir
        settings = spath+"settings.json"

        def MessagePopup(title, icon, text, callf=None):
            msg = QMessageBox() #Pylance is being stupid, I had to disable Type checking.
            msg.setWindowTitle(title)
            msg.setIcon(icon)
            msg.setText(text)
            if callf != None:
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) #Fuck pylance it says that this line is wrong anf that int can't bd a button, there is not int.
                msg.buttonClicked.connect(callf)
            msg.exec_()

        def loadpath(s="show"): # Fixed version from call.py display's mesage boxes
            global audio, videos, py, pip, ydpip, aup, Vcodec, Acodec, Vqual, Abit, Append, fdir #exposing all settings to the rest of the program.
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
                        path["Append"]
                    except KeyError: #if keys are missing
                        MessagePopup("Settings error", QMessageBox.Critical, "Your config file is not compatible with this version.\nPress OK to load defaut config.", SaveDefaultConfig)
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
                        Append = path["Append"]

                    pffmpeg = glob.glob(f"{spath}/ffmpeg*")
                    pffprobe = glob.glob(f"{spath}/ffprobe*")
                    if (not pffmpeg and not pffprobe):
                        fdir = False
                    else:
                        fdir = True
                except ValueError: #if json not valid
                    pass
                    MessagePopup("Settings error", QMessageBox.Critical, "Your config file is corrupted.\nPress OK to load defaut config.", SaveDefaultConfig)
                fh.close()
            except FileNotFoundError: #if file does not exist
                MessagePopup("Settings error", QMessageBox.Critical, "You are missing a config file,\nPress OK to load defaut config.", SaveDefaultConfig)
                exit(0)

        self.tabWidget.setCurrentIndex(0)

        def savepath(audp="a", vidp="a", pyth="a", pipd="a", ytpip="a", autup="a", vidc="a", audc="a", vidq="a", audb="a", appe="a"): #a is the default value because I dunno
            if audp == "a":
                global audio
                audp = audio
            elif audp == "":
                audp = spath+"audio"
            if vidp == "a":
                global videos
                vidp = videos
            elif vidp == "":
                vidp = spath+"videos"
            if pyth == "a":
                global py
                pyth = py
            if pipd == "a":
                global pip
                pipd = pip
            if ytpip == "a":
                global ydpip
                ytpip = ydpip
            if autup == "a":
                global aup
                autup = aup
            if vidc == "a":
                global Vcodec
                vidc = Vcodec
            if audc == "a":
                global Acodec
                audc = Acodec
            if vidq == "a":
                global Vqual
                vidq = Vqual
            if audb == "a":
                global Abit
                audb = Abit
            if appe == "a":
                global Append
                appe = Append

            audp = audp+os.path.sep
            vidp = vidp+os.path.sep

            fh = open(settings, "w")
            json.dump({"audio": audp,"videos": vidp,"py": pyth,"pip": pipd,"ydpip": ytpip,"aup": autup,"Vcodec": vidc,"Acodec": audc,"Vqual": vidq,"Abit": audb, "Append": appe}, fh, indent=2)
            fh.close()   

        def SaveDefaultConfig(i):
            if i.text() == "OK":
                savepath("", "", "python", "pip", True, False, "libx265", "opus", "24,24,24", "190k", "_custom.mkv")
            
        def status( s=""): #shows status message and changes color of the status bar.
            self.statusBar().showMessage(s)
            if s == "Ready.":
                self.statusBar().setStyleSheet("background-color: #00BB00")
            elif s == "Busy.":
                self.statusBar().setStyleSheet("background-color: #FF6600")
            else:
                self.statusBar().setStyleSheet("background-color: #A9A9A9")

        def process_start(cmd="", output_console=""):
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000) #this one does not check if another process is running
            for c in iter(lambda: process.stdout.read(1), b''):
                gui = self.isVisible()
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
                    output_console.insertPlainText(c)
                    self.scrollbar = output_console.verticalScrollBar()
                    self.scrollbar.setValue(self.scrollbar.maximum())
                    QtWidgets.QApplication.processEvents()
            print("\a")
            output_console.insertPlainText("#yt-dl# Process has finished.\n\n")
            QtWidgets.QApplication.processEvents()
            self.scrollbar = output_console.verticalScrollBar()
            self.scrollbar.setValue(self.scrollbar.maximum())

        def openFolder(loc=""):
            if (os.name == "nt"):
                os.system(f"start {loc}")
            elif (os.name == "posix"):
                os.system(f"xdg-open {loc}")

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
                self.tabWidget.setTabText(0, "*Audio")

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

                self.sub_output_console.insertPlainText("#yt-dl# starting youtube-dl please wait...\n")

                process_start(cmd, self.aud_output_console)

                running = False
                status("Ready.")
                self.tabWidget.setTabText(0, "Audio")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")
                
        def aud_playlist_bar_toggle():
            self.aud_playlist_bar.setEnabled(self.aud_playlist_checkbox.isChecked())
            if(self.aud_playlist_checkbox.isChecked()):
                self.aud_playlist_bar.setStyleSheet("background-color: #909090;")
            else:
                self.aud_playlist_bar.setStyleSheet("background-color: #707070;")

        def aud_open():
            openFolder(audio)

        #=====aud_controls=====#
        self.aud_folder_button.clicked.connect(aud_open)
        self.aud_download_button.clicked.connect(Audio)
        self.aud_playlist_checkbox.clicked.connect(aud_playlist_bar_toggle)
        self.aud_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Audio) paste a link and hit download.")

        #==========📼VIDEO📼==========#
        def Video():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.tabWidget.setTabText(1, "*Video")

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

                self.sub_output_console.insertPlainText("#yt-dl# starting youtube-dl please wait...\n")

                process_start(cmd, self.vid_output_console)
                
                running = False
                status("Ready.")
                self.tabWidget.setTabText(1, "Video")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")

        def vid_quality():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.vid_output_console.setHtml("") #clearing the output_console

                url = self.vid_url_bar.text()
                cmd = ["youtube-dl", "-F", "--no-playlist", f"{url}"]

                self.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

                process_start(cmd, self.vid_output_console)

                running = False
                status("Ready.")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")

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

        def vid_open():
            openFolder(videos)

        #=====vid_controls=====#
        self.vid_folder_button.clicked.connect(vid_open)
        self.vid_download_button.clicked.connect(Video)
        self.vid_quality_button.clicked.connect(vid_quality)
        self.vid_playlist_checkbox.clicked.connect(vid_playlist_bar_toggle)
        self.vid_custom_radio.toggled.connect(vid_quality_bar_toggle)
        self.vid_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Video) paste a link and hit download.")

        #==========📑SUBS📑==========#
        def Subs():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.tabWidget.setTabText(2, "*Subs")

                temp = tempfile.mkdtemp()+os.path.sep

                self.sub_output_console.setHtml("") #clearing the output_console.

                url = self.sub_url_bar.text()

                cmd = [[],[]]

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
                if (fdir == True):
                    if lang != None:
                        cmd = cmd[0]+lang+floc+cmd[1]
                    else:
                        cmd = cmd[0]+floc+cmd[1]
                else:
                    if lang != None:
                        cmd = cmd[0]+lang+cmd[1]
                    else:
                        cmd = cmd[0]+cmd[1]

                self.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

                print(cmd)
                
                process_start(cmd, self.sub_output_console)
                
                subpath = glob.glob(f"{temp}*.vtt")
                os.makedirs(videos, exist_ok=True)
                
                for item in subpath:
                    namei = os.path.basename(item)
                    namei = namei[:-3]
                    newsubpath = videos+namei+"srt"
                    if os.path.isfile(newsubpath):
                        self.sub_output_console.insertPlainText(f"#yt-dl# file {item} already exists skipping...\n")
                    else:                        
                        cmd = ["-i", f"{item}", f"{newsubpath}"]

                        floc = [f"{spath+os.path.sep+'ffmpeg'}", "-hide_banner"]
                        if (fdir == True):
                            cmd = floc+cmd
                        else:
                            cmd = ["ffmpeg", "-hide_banner"]+cmd

                        self.sub_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")

                        process_start(cmd, self.sub_output_console)

                running = False
                status("Ready.")
                self.tabWidget.setTabText(2, "Subs")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")

        def sub_lang():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.sub_output_console.setHtml("") #clearing the output_console

                url = self.sub_url_bar.text()
                cmd = ["youtube-dl", "--list-subs", "--no-playlist", f"{url}"]

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
                        self.sub_output_console.insertPlainText(c)
                        self.scrollbar = self.sub_output_console.verticalScrollBar()
                        self.scrollbar.setValue(self.scrollbar.maximum())
                        QApplication.processEvents()
                
                print("\a")
                self.sub_output_console.insertPlainText("#yt-dl# Process has finished.")
                QApplication.processEvents()
                self.scrollbar = self.sub_output_console.verticalScrollBar()
                self.scrollbar.setValue(self.scrollbar.maximum())
                running = False
                status("Ready.")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")

        def sub_playlist_bar_toggle():
            self.sub_lang_button.setEnabled(not self.sub_playlist_checkbox.isChecked())
            self.sub_playlist_bar.setEnabled(self.sub_playlist_checkbox.isChecked())
            if(self.sub_playlist_checkbox.isChecked()):
                self.sub_playlist_bar.setStyleSheet("background-color: #909090;")
            else:
                self.sub_playlist_bar.setStyleSheet("background-color: #707070;")

        def sub_lang_bar_toggle():
            self.sub_lang_bar.setEnabled(self.sub_lang_checkbox.isChecked())
            if(self.sub_lang_checkbox.isChecked()):
                self.sub_lang_bar.setStyleSheet("background-color: #909090;")
            else:
                self.sub_lang_bar.setStyleSheet("background-color: #707070;")

        #=====sub_controls=====#
        self.sub_folder_button.clicked.connect(vid_open)
        self.sub_download_button.clicked.connect(Subs)
        self.sub_lang_button.clicked.connect(sub_lang)
        self.sub_playlist_checkbox.toggled.connect(sub_playlist_bar_toggle)
        self.sub_lang_checkbox.toggled.connect(sub_lang_bar_toggle)
        self.sub_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Subtites) paste a link and hit download.")

        #==========💿REENCODE💿==========#
        def Reencode():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.tabWidget.setTabText(3, "*Re-encode")

                self.ree_output_console.setHtml("") #clearing the output_console

                location = self.ree_location_bar.text()
                videoc = self.ree_videoc_bar.text()
                videoq = self.ree_videoq_bar.text()
                audioc = self.ree_audioc_bar.text()
                audiob = self.ree_audiob_bar.text()
                append = self.ree_append_bar.text()

                if location[-2:] == "\*": #whole folder
                    VidsToRender = glob.glob(location)
                else:
                    VidsToRender = [f"{location}"]
                for video in VidsToRender:
                    if os.path.isfile(os.path.splitext(video)[0]+append):
                        self.ree_output_console.insertPlainText(f"#yt-dl# file {video} already exists skipping...\n")
                    else:
                        cmd = [["-hwaccel", "auto", "-i", f"{video}", "-map", "0:v?", "-map", "0:a?", "-map", "0:s?"],["-max_muxing_queue_size", "9999", "-b:v", "0K"],[f"{os.path.splitext(video)[0]+append}"]]

                        #//Video Quality\\#
                        if "," in videoq:
                            VQsplit = Vqual.split(",")
                        else:
                            VQsplit = [Vqual,Vqual,Vqual]
                        #//Videeo Codec\\#
                        if(videoc == "libx265"):
                            VideoCodec = ["-c:v", f"{videoc}"]
                            quality = ["-crf", f"{int(VQsplit[0])-1}", "-qmin", f"{int(VQsplit[1])-1}", "-qmax", f"{int(VQsplit[2])-1}"]
                            Vformat = ["-vf", "format=yuv420p"]
                            cmd = [cmd[0]+VideoCodec+quality+cmd[1]+Vformat,cmd[2]]
                        elif(videoc == "copy"):
                            VideoCodec = [f"-c:v", f"{videoc}"]
                            cmd = [cmd[0]+VideoCodec+cmd[1],cmd[2]]
                        elif(videoc == "remove"):
                            VideoCodec = ["-vn"]
                            cmd = [cmd[0]+VideoCodec+cmd[1],cmd[2]]
                        else:
                            VideoCodec = ["-c:v", f"{videoc}"]
                            quality = ["-cq", f"{int(VQsplit[0])-1}", "-qmin", f"{int(VQsplit[1])-1}", "-qmax", f"{int(VQsplit[2])-1}"]
                            Vformat = ["-vf", "format=yuv420p"]
                            cmd = [cmd[0]+VideoCodec+quality+cmd[1]+Vformat,cmd[2]]
                        #//Audio\\#
                        if(audioc == "remove"):
                            AudioEverything = ["-an"]
                            cmd = [cmd[0]+AudioEverything,cmd[1]]
                        else:
                            AudioEverything = ["-c:a", f"{audioc}", "-strict", "-2", "-b:a", f"{audiob}"]
                            cmd = [cmd[0]+AudioEverything,cmd[1]]
                        #//Subtitles\\#
                        if(videoc == "remove"):
                            SubsC = ""
                            cmd = cmd[0]+cmd[1]
                        else:
                            SubsC = ["-c:s", "copy"]
                            cmd = cmd[0]+SubsC+cmd[1]

                        floc = [f"{spath+os.path.sep+'ffmpeg'}", "-hide_banner"]
                        if (fdir == True):
                            cmd = floc+cmd
                        else:
                            cmd = ["ffmpeg", "-hide_banner"]+cmd

                        process_start(cmd, self.ree_output_console)

                running = False
                status("Ready.")
                self.tabWidget.setTabText(3, "Re-encode")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")
        
        def ree_settings():
            if self.ree_settings_combobox.currentIndex() == 2: #custom
                self.ree_videoc_bar.setText(Vcodec)
                self.ree_videoq_bar.setText(Vqual)
                self.ree_audioc_bar.setText(Acodec)
                self.ree_audiob_bar.setText(Abit)
                self.ree_append_bar.setText(Append)
                self.ree_settings_button.setEnabled(True)
            elif self.ree_settings_combobox.currentIndex() == 0: #hevc_opus
                self.ree_videoc_bar.setText("libx265")
                self.ree_videoq_bar.setText("24,24,24")
                self.ree_audioc_bar.setText("opus")
                self.ree_audiob_bar.setText("190k")
                self.ree_append_bar.setText("_hevcopus.mkv")
                self.ree_settings_button.setEnabled(False)
            elif self.ree_settings_combobox.currentIndex() == 1: #h264_nvenc
                self.ree_videoc_bar.setText("h264_nvenc")
                self.ree_videoq_bar.setText("24,24,24")
                self.ree_audioc_bar.setText("aac")
                self.ree_audiob_bar.setText("190k")
                self.ree_append_bar.setText("_nvenc.mov")
                self.ree_settings_button.setEnabled(False)

        def ree_settings_save():
            if self.ree_settings_combobox.currentIndex() == 2: #custom
                vidc = self.ree_videoc_bar.text()
                audc = self.ree_audioc_bar.text()
                vidq = self.ree_videoq_bar.text()
                audb = self.ree_audiob_bar.text()
                appe = self.ree_append_bar.text()
                savepath(vidc=vidc, audc=audc, vidq=vidq, audb=audb, appe=appe)

        def ree_choose():
            self.ree_location_bar.setText(QFileDialog.getOpenFileName()[0])

        def ree_open():
            location = self.ree_location_bar.text()
            openFolder(os.path.dirname(location))

        #=====ree_controls=====#
        self.ree_settings_combobox.addItem("hevc_opus") # setting up items in combo list
        self.ree_settings_combobox.addItem("h264_nvenc")
        self.ree_settings_combobox.addItem("custom")
        ree_settings() # load option on startup
        self.ree_choose_button.clicked.connect(ree_choose)
        self.ree_reencode_button.clicked.connect(Reencode)
        self.ree_folder_button.clicked.connect(ree_open)
        self.ree_settings_combobox.activated.connect(ree_settings)
        self.ree_settings_button.clicked.connect(ree_settings_save)
        self.ree_output_console.setHtml("#yt-dl# Welcome to yt-dl-gui (Re-encode) paste a link and hit download.")

        #==========🔄UPDATE🔄==========#
        def update_yt_dl():
            cmd = ["git", "pull", "--recurse-submodules"]
            process_start(cmd, self.upd_output_console)

        def update_depend():
            cmd = [f"{py}", "-m", f"{pip}", "install", "-U", f"{pip}"] #this shit will not work if pip="pip" but pretend
            process_start(cmd, self.upd_output_console)
            cmd = [f"{pip}", "install", "-U", "-r", "requirements.txt"]
            process_start(cmd, self.upd_output_console)

        def Update():
            global running
            if running == False:
                running = True
                status("Busy.")

                self.tabWidget.setTabText(4, "*Update")

                self.upd_output_console.setHtml("") #clearing the output_console

                if self.upd_update_combobox.currentIndex() == 1:
                    update_yt_dl()
                elif self.upd_update_combobox.currentIndex() == 2:
                    update_depend()
                else:
                    update_yt_dl()
                    update_depend()

                running = False
                status("Ready.")
                self.tabWidget.setTabText(4, "Update")
            else:
                MessagePopup("Process warning", QMessageBox.Warning, "One process already running!")

        def upd_auto_toggle(): #autoupdate is not a thing tho
            loadpath()
            global aup
            aupl = not aup
            savepath(autup=aupl)
            self.upd_auto_button.setText(f"Autoupdate=\"{aupl}\"")

        #======upd_controls======#
        self.upd_update_combobox.addItem("All") # setting up items in combo list
        self.upd_update_combobox.addItem("yt-dl")
        self.upd_update_combobox.addItem("dependencies")
        '''
        branches = os.listdir(spath+".git/refs/heads")
        for branch in branches:
            self.upd_branch_combobox.addItem(branch)
        
        process = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE)
        gcurb = str(process.stdout.read())
        curb = "Current branch: "+curb[2:-3]
        self.upd_branch_label.setText(curb)
        '''

        QtWidgets.QApplication.processEvents()
        if aup:
            self.tabWidget.setCurrentIndex(4)
            Update()

        self.upd_update_button.clicked.connect(Update)
        #self.upd_branch_button.clicked.connect(upd_branch)
        self.upd_auto_button.setText(f"Autoupdate=\"{aup}\"")
        self.upd_auto_button.clicked.connect(upd_auto_toggle)

        #==========📈SETTINGS📈==========#
        def set_save():
            a = self.set_audio_bar.text()
            b = self.set_videos_bar.text()
            c = self.set_py_bar.text()
            d = self.set_pip_bar.text()
            e = self.set_ydpip_checkbox.isChecked()
            f = self.set_aup_checkbox.isChecked()
            g = self.set_Acodec_bar.text()
            h = self.set_Vcodec_bar.text()
            i = self.set_Abit_bar.text()
            j = self.set_Vqual_bar.text()
            k = self.set_Append_bar.text()

            savepath(a,b,c,d,e,f,h,g,j,i,k)
            loadpath()

        def set_load(a,b,c,d,e,f,g,h,i,j,k):
            self.set_audio_bar.setText(a[:-1])
            self.set_videos_bar.setText(b[:-1])
            self.set_py_bar.setText(c)
            self.set_pip_bar.setText(d)
            self.set_ydpip_checkbox.setChecked(e)
            self.set_aup_checkbox.setChecked(f)
            self.set_Acodec_bar.setText(g)
            self.set_Vcodec_bar.setText(h)
            self.set_Abit_bar.setText(i)
            self.set_Vqual_bar.setText(j)
            self.set_Append_bar.setText(k)

        def set_makeScript():  #I had an issue getting the venv working with gui
            if(os.name == 'nt'):
                f=open("yt-dl_gui.vbs","w")
                f.write(f"Set WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run \"cmd /c cd /d {spath} & pythonw.exe gui.py\", 0\nSet WshShell = Nothing")
                f.close()
                f=open("yt-dl_gui.bat","w")
                f.write(f"@echo off\n\nstart /b pythonw.exe gui.py")
                f.close()
            elif(os.name == 'posix'):
                f=open("yt-dl","w")
                f.write(f"#!/bin/sh\n\ncd {spath}{cmd}{os.path.sep}bin && source activate && cd {spath} && {py} main.py")
                f.close()
        
        def set_open():
            print(spath)
            openFolder(spath)

        #=====set_controls=====#
        set_load(audio, videos, py, pip, True, True, Acodec, Vcodec, Abit, Vqual, Append)
        self.set_loadcur_button.clicked.connect(lambda:set_load(audio, videos, py, pip, True, True, Acodec, Vcodec, Abit, Vqual, Append))
        self.set_loaddef_button.clicked.connect(lambda:set_load(spath+"audio"+os.path.sep, spath+"videos"+os.path.sep, "python", "pip", True, False, "opus", "libx265", "190k", "24,24,24", "_custom.mkv"))
        self.set_folder_button.clicked.connect(set_open)
        self.set_launch_button.clicked.connect(set_makeScript)
        self.set_save_button.clicked.connect(set_save)
        
        
        #==========🎓ABOUT🎓==========#
        self.about_box.setHtml(f"<p style=\"font-size: 20px; white-space: pre\">ArmoredMobilePony Inc. (C){year}<br>"
                              +f"Last updated on: {lstupdt}<br>"
                              +f"My webpage: <a href=\"https://koleckolp.comli.com\">https://koleckolp.comli.com</a><br>"
                              +f"Project page: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://github.com/KoleckOLP/yt-dl</a><br>"
                              +f"need help? ask here: <a href=\"https://github.com/KoleckOLP/yt-dl\">https://discord.gg/W88375j</a><br>"
                              +f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez<br>"
                              +f"                 (C)2011-{year} youtube-dl developers<br>"
                              +f"ffmpeg (C)2000-{year} FFmpeg team<br>"
                              +f"Big thanks to <a href=\"https://github.com/kangalioo\">kangalioo</a> who always helps a ton!<br>"
                              +f"You can read the changelog: <a href=\"https://github.com/KoleckOLP/yt-dl/blob/master/whatsnew.md\">here</a></pre></p>")  

app = QtWidgets.QApplication(sys.argv)
loader = QtUiTools.QUiLoader() # load the gui file into a new instance of the "cls" Python class
loader.registerCustomWidget(MainWindow)
window = loader.load("gui.ui")
window.show()
window.init()
app.exec_()