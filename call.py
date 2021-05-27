import os
import sys
import glob
import tempfile
from colorama import init, Fore, Style  # Back
# Imports from this projects
from kolreq.kolreq import clear, readchar
from release import year, lstupdt, spath, curb, ver, settingsPath
from Config import Settings

init()  # initialises colorama


def is_venv():  # reports if user is in Virtual Environment or not
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


# ==========NAME========== #
def name(newline=True):
    BC("yt-dl {ver} cli ({curb} branch) by KoleckOLP (C){year}\n", newline) 


# ==========FIRST TIME SETUP MENU========== #
def firstrun():
    clear()
    global settings
    settings = Settings.loadDefault()
    print("this program requires ffmpeg and ffprobe, please put them into the yt-dl directory")
    print("What's the name of your python executable.\n<enter> for python (apologise fo inconvenience)")
    settings.Python.python = input("#")
    if (settings.Python.python == ""):
        settings.Python.python = "python"
    print("What's the name of your pip executable.\n<Enter> for pip")
    settings.Python.pip = input("#")
    if (settings.Python.pip == ""):
        settings.Python.pip = "pip"
    print("Have you installed youtube-dl with pip? (yes if you installed requirements) [Y/n]")
    cmd = readchar("#")
    if (cmd == "y"):
        settings.Youtubedl.fromPip = True
    else:
        settings.Youtubedl.fromPip = False
    print("\nDo you want autoudate on launch? [Y/n]")
    cmd = readchar("#")
    if (cmd == "y"):
        settings.autoUpdate = True
    else:
        settings.autoUpdate = False
    print()
    settings.Ffmpeg.videoCodec = "libx265"  # libx265, h264_nvenc
    settings.Ffmpeg.audioCodec = "opus"  # opus, acc
    settings.Ffmpeg.videoQuality = "24,24,24"  # 24
    settings.Ffmpeg.audioBitrate = "190k"  # 190
    savepath()
    loadpath()
    print("Do you want a Launch script? [Y/n] or p=" + Fore.BLUE + "Powershell" + Style.RESET_ALL)
    cmd = readchar("#")
    if (cmd == "y"):
        launchs()
    elif(cmd == "p"):
        launchs(True)
    else:
        pass
    loadpath("hid")
    about()


# ==========MAKE LAUNCH SCRIPT========== #
def launchs(p=False):
    if is_venv:
        print("type name of your venv")
        cmd = input("#")
    else:
        cmd = ""

    if p:
        if(cmd != ""):
            f = open("yt-dl.ps1", "w")
            f.write(f"Set-Location {spath}{cmd}{os.path.sep}Scripts\n.{os.path.sep}Activate.ps1\nSet-Location {spath}\n{settings.Python.python} main.py")
            f.close()
        else:
            f = open("yt-dl.ps1", "w")
            f.write(f"Set-Location {spath}\n{settings.Python.python} main.py")
            f.close()
    else:
        if(cmd != ""):
            if(os.name == 'nt'):
                f = open("yt-dl.bat", "w")
                f.write(f"@echo off\n\ncmd /c \"cd /d {spath}{cmd}{os.path.sep}Scripts & activate & cd /d {spath} & {settings.Python.python} main.py\"")
                f.close()
            elif(os.name == 'posix'):
                f = open("yt-dl", "w")
                f.write(f"#!/bin/sh\n\ncd {spath}{cmd}{os.path.sep}bin && source activate && cd {spath} && {settings.Python.python} main.py")
                f.close()
            else:
                print('####If you see this please contact the dev. 0x1015####')
        else:
            if(os.name == 'nt'):
                f = open("yt-dl.bat", "w")
                f.write(f"@echo off\n\ncmd /c \"cd /d {spath} & {settings.Python.python} main.py\"")
                f.close()
            elif(os.name == 'posix'):
                f = open("yt-dl", "w")
                f.write(f"#!/bin/sh\n\ncd {spath} && {settings.Python.python} main.py")
                f.close()
            else:
                print('####If you see this please contact the dev. 0x1005####')


# ==========ABOUT========== #
def about():
    clear()
    name(False)
    print(f"HorseArmored inc (C){year}\n" +
          f"Version: {ver} cli ({curb} branch)\n" +
          f"Last updated on: {lstupdt}\n" +
          f"My webpage: https://koleckolp.comli.com/\n" +
          f"Project page: https://github.com/KoleckOLP/yt-dl\n" +
          f"need help? ask here: https://discord.gg/W88375j\n" +
          f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez\n" +
          f"           (C)2011-{year} youtube-dl developers\n" +
          f"ffmpeg (C)2000-{year} FFmpeg team\n" +
          f"Thanks to kangalioo who always helps a ton!\n" +
          f"Thanks to siscode for featuring my project\n" +
          f"and helping me improve it.\n" +
          f"You can find them both on github.")
    print(Style.BRIGHT + "Do you want to see whats new? [Y/n]" + Style.RESET_ALL)
    cmd = readchar("#")
    if (cmd == "y"): 
        clear()
        fh = open("whatsnew.md", "r")
        print(fh.read()+"\n")
        fh.close()
    else:
        clear()
        name()


# ==========SAVE PATH========== #
def savepath():
    settings.toJson(settingsPath)


# ==========LOAD PATH========== #
def loadpath(s="show"):
    # old mess
    global settings, fdir
    pffmpeg = glob.glob(f"{spath}/ffmpeg*")
    pffprobe = glob.glob(f"{spath}/ffprobe*")
    if (not pffmpeg and not pffprobe):
        fdir = False
    else:
        fdir = True
    # new stuff
    if (os.path.exists(settingsPath)):
        settings = Settings.fromJson(settingsPath)
    else:
        firstrun()

    if(s == "show"):
        print(Style.BRIGHT + "audio is saved to: " + Style.RESET_ALL, end="")
        print(settings.Youtubedl.audioDir)
        print(Style.BRIGHT + "video is saved to: " + Style.RESET_ALL, end="")
        print(settings.Youtubedl.videoDir + "\n")


# ==========SAVE MENU========== #
def slpath():
    loadpath()
    print("1. change download path\n2. delete settings\n3. generate Launch script\n0. GoBack")
    cmd = readchar("#")
    if (cmd == "1"):
        savepath()
        clear()
        loadpath()
    elif (cmd == "2"):
        os.remove(settings)
        firstrun()
    elif (cmd == "3"):
        print("press p=" + Fore.BLUE + "PowerShell" + Style.RESET_ALL + " or <Enter>")
        cmd = input("#")
        if(cmd == "p"):
            launchs(True)
        else:
            launchs()
        clear()
        name()
    else:
        clear()
        name()


# ==========UPDATE YTDL========== #
def upytdl():
    print("Updating yt-dl...")
    if(os.path.exists(spath+".git")):
        os.system("cd "+spath)
        os.system("git pull --recurse-submodules")
    else:
        print("yt-dl wasn't installed trough git.\n" +
              "delete yt-dl and install it with \"git clone https://github.com/KoleckOLP/yt-dl.git\"")


# ==========UPDATE DEPEND========== #
def upyd():
    print("updating pip...")
    os.system(f"{settings.Python.python} -m {settings.Python.pip} install --upgrade {settings.Python.pip}")
    print("Updating dependencies...")
    os.system(f"{settings.Python.pip} install -U -r req-cli.txt")


# ==========UPDATE MENU========== #
def update():
    clear()
    if settings.Youtubedl.fromPip:
        print(Style.BRIGHT + f"What do you want to update?" + Style.RESET_ALL + "\n1. All\n2. yt-dl\n3. dependencies\n4. change autoupdate=", end="")
        TF(settings.autoUpdate, False)
        print(f"\n5. change branch=", end="")
        BC(curb)
        print("\n0. GoBack")
        cmd = readchar("#")
        if(cmd == "1"):  # All
            clear()
            upytdl()
            upyd()
            print(Fore.RED, "\n!!!restart for changes to take effect!!!\n", Style.RESET_ALL)
        elif(cmd == "2"):  # yt-dl
            clear()
            upytdl()
            print(Fore.RED, "\n!!!restart for changes to take effect!!!\n", Style.RESET_ALL)
        elif(cmd == "3"):  # youtube-dl
            clear()
            upyd()
            print("")
        elif (cmd == "4"):
            settings.autoUpdate = not settings.autoUpdate
            savepath()
            loadpath("hid")
            clear()
            print(f"autoupdate={settings.autoUpdate}\n")
        elif(cmd == '5'):
            clear()
            print(f"What branch do you wat to change to? You are in a {curb}")
            if (curb == "master"):
                otherb = "testing"
            else:
                otherb = "master"
            print(f"do you want to switch to ")
            BC(otherb, False, True)
            print(" [Y/n]")
            cmd = readchar("#")
            if (cmd == "y"):
                os.system("git pull --recurse-submodules")
                os.system(f"git checkout {otherb}")
                print(Fore.RED, "\n!!!restart for changes to take effect!!!\n", Style.RESET_ALL)
            else:
                clear()
                name()
        else:
            clear()
            name()
    else:
        upytdl()


# ==========AUTO UPDATE========== #
def autoupdt():
    print(f"autoupdate=", end="")
    TF(settings.autoUpdate)
    if settings.autoUpdate:
        upytdl()
        upyd()
        print()
    else:
        print()


# ==========AUDIO DOWNLOAD========== #
def audiod():
    global fdir
    if fdir:
        floc = f"--ffmpeg-location {spath}"
    else:
        floc = ""

    clear()
    print("link to audio, playlist, 0. GoBack")
    url = input("#")
    if(url == "0"):
        clear()
        name()
    else:
        print("<Enter> a single audio, \n" +
              "1. to download full playlist or follow example 1-3,7,9")
        numb = input("#")
        if(numb == ""):
            lnk = f"-o \"{settings.Youtubedl.audioDir}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg {floc} --audio-format mp3 \"{url}\""
        elif(numb == "1"):
            lnk = f"-o \"{settings.Youtubedl.audioDir}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i -x --prefer-ffmpeg {floc} --audio-format mp3 \"{url}\""
        else:
            lnk = f"-o \"{settings.Youtubedl.audioDir}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i --playlist-items {numb} -x --prefer-ffmpeg {floc} --audio-format mp3 \"{url}\""
        print("starting youtube-dl please wait...")
        os.system("youtube-dl "+lnk)
        print("\a")


# ==========VIDEO DOWNLOAD========== #
def videod():
    global fdir
    if fdir:
        floc = f"--ffmpeg-location {spath}"
    else:
        floc = ""

    clear()
    print("link to video, playlist, 0. GoBack")
    url = input("#")
    if (url == "0"):
        clear()
        name()
    else:
        print("<Enter> a single video, \n" +
              "1. to download full playlist or follow example 1-3,7,9")
        numb = input("#")
        if(numb == ""):  # no playlist
            print("<Enter> for best quality 1080p + if available (\"bestvideo+bestaudio\"),\n" +
                  "1 for 720 or lower (\"best\")\n" +
                  "2 to choose yourself")
            qual = input("#")
            if (qual == "1"):
                lnk = f"-o \"{settings.Youtubedl.videoDir}%(title)s.%(ext)s\" -f best --no-playlist --prefer-ffmpeg {floc} \"{url}\""
            elif(qual == "2"):
                print("starting youtube-dl please wait...")
                os.system(f"youtube-dl -F --no-playlist {url}")
                print("choose video and audio quality by typing numb+numb")
                numb = input("#")
                lnk = f"-o \"{settings.Youtubedl.videoDir}%(title)s.%(ext)s\" -f \"{numb}\" --no-playlist --prefer-ffmpeg {floc} \"{url}\""
            else:
                lnk = f"-o \"{settings.Youtubedl.videoDir}%(title)s.%(ext)s\" -f bestvideo+bestaudio --no-playlist --prefer-ffmpeg {floc} \"{url}\""
        else:  # playlist
            print("<Enter> for the best quality 1080p + if available, \n" +
                  "1 for 720p or lower")
            qual = input("#")
            if(qual == "1"): 
                if(numb == "1"):
                    lnk = f"-o \"{settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --prefer-ffmpeg {floc} \"{url}\""
                else:
                    lnk = f"-o \"{settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --playlist-items {numb} --prefer-ffmpeg {floc} \"{url}\""
            else:
                if(numb == "1"):
                    lnk = f"-o \"{settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --prefer-ffmpeg {floc} \"{url}\""
                else:
                    lnk = f"-o \"{settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --playlist-items {numb} --prefer-ffmpeg {floc} \"{url}\""
        print("starting youtube-dl please wait...")
        os.system("youtube-dl "+lnk)
        print("\a")


# ==========SUBTITLE DOWNLOAD========== #
def subd():
    global fdir
    if fdir:
        floc = f"--ffmpeg-location {spath}"
    else:
        floc = ""

    clear()
    temp = tempfile.mkdtemp()+os.path.sep
    print("link to video with subs or 0. GoBack")
    url = input("#")
    if (url == "0"):
        clear()
        name()
    else:
        print("<Enter> to download default sub (en),\n" +
              "1 to choose language")
        numb = input("#")
        if(numb == ""):
            lnk = f"-o \"{temp}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-format vtt --skip-download --prefer-ffmpeg {floc} \"{url}\""
        else:
            print("starting youtube-dl please wait...")
            os.system(f"youtube-dl --list-subs --noplaylist {url}")
            print("choose sub language")
            numb = input("#")
            lnk = f"-o \"{temp}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-lang \"{numb}\" --sub-format vtt --skip-download --prefer-ffmpeg {floc} \"{url}\""
        print("starting youtube-dl please wait...")
        os.system("youtube-dl "+lnk)
        pie = glob.glob(f"{temp}*.vtt")
        cream = os.path.basename(pie[0])
        cream = cream[:-3]
        lick = f"{settings.Youtubedl.videoDir}{cream}srt"  # I don't like this fix to a complain about var type
        os.makedirs(settings.Youtubedl.videoDir, exist_ok=True)
        print("starting youtube-dl please wait...")
        os.system(f"ffmpeg -i \"{pie[0]}\" \"{lick}\"")
        print("\a")


# ==========VID TO HEVC========== #
def reencode():
    global fdir
    if (fdir is True):
        floc = f"{spath}"
    else:
        floc = ""

    clear()
    print(Fore.RED + "Files with special characters in the path may not work, also keep filenames short" + Style.RESET_ALL)
    print("(video codec=\"", end="")
    if (settings.Ffmpeg == "none"):
        print(Fore.RED + settings.Ffmpeg.videoCodec + Style.RESET_ALL, end="")
    else:
        print(Fore.YELLOW + settings.Ffmpeg.videoCodec + Style.RESET_ALL, end="")
    print("\", audio codec=\"" + Fore.CYAN + settings.Ffmpeg.audioCodec + Style.RESET_ALL + "\", video q,qmin,qmax=\"", end="")
    if (settings.Ffmpeg.videoCodec == "none"):
        print(Fore.RED + settings.Ffmpeg.videoQuality + Style.RESET_ALL, end="")
    else:
        print(Fore.YELLOW + settings.Ffmpeg.videoQuality + Style.RESET_ALL, end="")
    print("\", audio bitrate=\"" + Fore.CYAN + settings.Ffmpeg.audioBitrate + Style.RESET_ALL + "\")\n" +
          "<Enter> single video\n" +
          "1. whole folder\n" +
          "2. change settings\n" +
          "0. GoBack")
    cmd = input("#")
    if(cmd == ""):  # ====================SINGLE==================== #
        if(settings.Ffmpeg.videoCodec == "remove" and settings.Ffmpeg.audioCodec == "remove"):
            print("I mean you can delete the file yourself. :)")
        else:
            print("write path to the file you want to reencode")
            url = input("#")
            if(url[0:3] == "& \'"):  # powershell (& ' ')
                url = url[3:-1]
            elif(url[0:1] == '\"'):  # cmd (" ")
                url = url[1:-1]
            elif(url[0:1] == "'"):  # posix (' ' )
                url = url[1:-2]
            # //append\\ #
            if(settings.Ffmpeg.videoCodec == "remove"):
                print("re-encoded file will get \".mp3\" appended, or type a different one")
                append = input("#")
                if(append == ""):
                    append = ".mp3"
            else:
                print("re-encoded file will get \"_hevcopus.mkv\" appended, 1. \"_nvenc.mov\" or type a different one")
                append = input("#")
                if(append == ""):
                    append = "_hevcopus.mkv"
                elif(append == "1"):
                    append = "_nvenc.mov"
            # //Video Quality\\ #
            if "," in settings.Ffmpeg.videoQuality:
                VQsplit = settings.Ffmpeg.videoQuality.split(",")
            else:
                VQsplit = [settings.Ffmpeg.videoQuality, settings.Ffmpeg.videoQuality, settings.Ffmpeg.videoQuality]
            # //Video Codec\\ #
            if(settings.Ffmpeg.videoCodec == "libx265"):
                VideoCodec = f"-c:v {settings.Ffmpeg.videoCodec}"
                quality = f"-crf {int(VQsplit[0])-1} -qmin {int(VQsplit[1])-1} -qmax {int(VQsplit[2])-1}"
                Vformat = "-vf format=yuv420p"
            elif(settings.Ffmpeg.videoCodec == "copy"):
                VideoCodec = f"-c:v {settings.Ffmpeg.videoCodec}"
                quality = ""
                Vformat = ""
            elif(settings.Ffmpeg.videoCodec == "remove"):
                VideoCodec = "-vn"
                quality = ""
                Vformat = ""
            else:
                VideoCodec = f"-c:v {settings.Ffmpeg.videoCodec}"
                quality = f"-cq {VQsplit[0]} -qmin {VQsplit[1]} -qmax {VQsplit[2]}"
                Vformat = "-vf format=yuv420p"
            # //Audio\\ #
            if(settings.Ffmpeg.audioCodec == "remove"):
                AudioEverything = "-an"
            else:
                AudioEverything = f"-c:a {settings.Ffmpeg.audioCodec} -strict -2 -b:a {settings.Ffmpeg.audioBitrate}"
            # //Subtitles\\ #
            if(settings.Ffmpeg.videoCodec == "remove"):
                SubsC = ""
            else:
                SubsC = "-c:s copy"
            os.system(f"{floc}ffmpeg -hwaccel auto -i \"{url}\" -map 0:v? -map 0:a? -map 0:s? {VideoCodec} {quality} -max_muxing_queue_size 9999 -b:v 0K {Vformat} {AudioEverything} {SubsC} \"{os.path.splitext(url)[0]+append}\"")
        print("\a")
    elif(cmd == '1'):  # ====================WHOLE FOLDER==================== #
        if(settings.Ffmpeg.videoCodec == "remove" and settings.Ffmpeg.audioCodec == "remove"):
            print("I'm not gonna delete the folder for you. hmpf")
        else:
            print("write path to the folder with videos")
            url = input("#")
            # //append\\ #
            if(settings.Ffmpeg.videoCodec == "remove"):
                print("re-encoded file will get \".mp3\" appended, or type a different one")
                append = input("#")
                if(append == ""):
                    append = ".mp3"
            else:
                print("re-encoded file will get \"_hevcopus.mkv\" appended, 1. \"_nvenc.mov\" or type a different one")
                append = input("#")
                if(append == ""):
                    append = "_hevcopus.mkv"
                elif(append == "1"):
                    append = "_nvenc.mov"
            # //Video Quality\\ #
            if "," in settings.Ffmpeg.videoQuality:
                VQsplit = settings.Ffmpeg.videoQuality.split(",")
            else:
                VQsplit = [settings.Ffmpeg.videoQuality, settings.Ffmpeg.videoQuality, settings.Ffmpeg.videoQuality]
            # //Video Codec\\ #
            if(settings.Ffmpeg.videoCodec == "libx265"):
                VideoCodec = f"-c:v {settings.Ffmpeg.videoCodec}"
                quality = f"-crf {int(VQsplit[0])-1} -qmin {int(VQsplit[1])-1} -qmax {int(VQsplit[2])-1}"
                Vformat = "-vf format=yuv420p"
            elif(settings.Ffmpeg.videoCodec == "copy"):
                VideoCodec = f"-c:v {settings.Ffmpeg.videoCodec}"
                quality = ""
                Vformat = ""
            elif(settings.Ffmpeg.videoCodec == "remove"):
                VideoCodec = "-vn"
                quality = ""
                Vformat = ""
            else:
                VideoCodec = f"-c:v {settings.Ffmpeg.videoCodec}"
                quality = f"-cq {VQsplit[0]} -qmin {VQsplit[1]} -qmax {VQsplit[2]}"
                Vformat = "-vf format=yuv420p"
            # //Audio\\ #
            if(settings.Ffmpeg.audioCodec == "remove"):
                AudioEverything = "-an"
            else:
                AudioEverything = f"-c:a {settings.Ffmpeg.audioCodec} -strict -2 -b:a {settings.Ffmpeg.audioBitrate}"
            # //Subtitles\\ #
            if(settings.Ffmpeg.videoCodec == "remove"):
                SubsC = ""
            else:
                SubsC = "-c:s copy"
            url = url.replace('[', '[[]')
            videos = glob.glob(url+os.path.sep+"*.*")
            for video in videos:
                os.system(f"{floc}ffmpeg -hwaccel auto -i \"{video}\" -map 0:v? -map 0:a? -map 0:s? {VideoCodec} -max_muxing_queue_size 9999 {quality} -b:v 0K {Vformat} {AudioEverything} {SubsC} \"{video[:-4]+append}\"")
        print("\a")
    elif(cmd == '2'):
        print(f"VideoCodec = {settings.Ffmpeg.videoCodec}, <Enter> keep, 1. libx265, 2. h264_nvenc, 3. copy, 4. remove or write your own")
        cmd = input("#")
        if (cmd == ""):
            pass
        elif(cmd == "1"):
            settings.Ffmpeg.videoCodec = "libx265"
        elif(cmd == "2"):
            settings.Ffmpeg.videoCodec = "h264_nvenc"
        elif(cmd == "3"):
            settings.Ffmpeg.videoCodec = "copy"
        elif(cmd == "4"):
            settings.Ffmpeg.videoCodec = "remove"
        else:
            settings.Ffmpeg.videoCodec = cmd
        print(f"AudioCodec = {settings.Ffmpeg.audioCodec}, <Enter> keep, 1. Opus, 2. AAC, 3. copy, 4. remove or write your own")
        cmd = input("#")
        if (cmd == ""):
            pass
        elif(cmd == "1"):
            settings.Ffmpeg.audioCodec = "opus"
        elif(cmd == "2"):
            settings.Ffmpeg.audioCodec = "aac"
        elif(cmd == "3"):
            settings.Ffmpeg.audioCodec = "copy"
        elif(cmd == "4"):
            settings.Ffmpeg.audioCodec = "remove"
        else:
            settings.Ffmpeg.audioCodec = cmd
        if (settings.Ffmpeg.videoCodec not in ("copy", "remove")):
            print(f"VideoQuality = {settings.Ffmpeg.videoQuality}, <Enter> keep, 1. 24,24,24; or write your own q,qmin,qmax, or just q")
            cmd = input("#")
            if (cmd == ""):
                pass
            elif(cmd == "1"):
                settings.Ffmpeg.videoQuality = "24,24,24"
            else:
                settings.Ffmpeg.videoQuality = cmd
        else:
            settings.Ffmpeg.videoQuality = "none"
        if(settings.Ffmpeg.audioCodec not in ("copy", "remove")):
            print(f"AudioBitrate = {settings.Ffmpeg.audioBitrate}, <Enter> keep, 1. 190k, or write your own")
            cmd = input("#")
            if (cmd == ""):
                pass
            elif(cmd == "1"):
                settings.Ffmpeg.audioBitrate = "190k"
            else:
                settings.Ffmpeg.audioBitrate = cmd
        else:
            settings.Ffmpeg.audioBitrate = "none"
        savepath()
        loadpath("hid")
    else:
        clear()
        name()


# ==========DEBUG CONSOLE========== #
def debug():
    print(Fore.MAGENTA + "Welcome to debug menu:", Style.RESET_ALL)
    while(True):
        cmd = input(">")
        if(cmd == "all"):
            print("Paths:")
            for p in sys.path:
                print(p)
            print("\nSaves:")
            if(os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0]))+os.path.sep+".git")):
                git = True
            else:
                git = False
            loadpath()
            print("Variables:")
            print(f"python executable name: {settings.Python.python}\npip executable name: {settings.Python.pip}")
            print("youtube-dl from pip: ", end="")
            TF(settings.Youtubedl.fromPip)
            print("ffmpeg in yt-dl dir: ", end="")
            TF(fdir)
            print("yt-dl from git: ", end="")
            TF(git)
            print("autoupdate: ", end="")
            TF(settings.autoUpdate)
            print(f"videoCodec: {settings.Ffmpeg.videoCodec}\naudioCodec: {settings.Ffmpeg.audioCodec}\nvideoQuality: {settings.Ffmpeg.videoQuality}\naudioBitrate: {settings.Ffmpeg.audioBitrate}")
            if is_venv():
                venv = True
            else:
                venv = False
            print("in venv: ", end="")
            TF(venv)
        elif(cmd == "deldown"):
            print("Are you sure you want to delete all audio and videos [Y/n]")
            cmd = readchar("")
            if(cmd == "y"):
                if(os.name == 'nt'):
                    os.system('del '+settings.Youtubedl.audioDir)
                    os.system('del '+settings.Youtubedl.videoDir)
                elif(os.name == 'posix'):
                    os.system('rm '+settings.Youtubedl.audioDir+os.pathsep)
                    os.system('rm '+settings.Youtubedl.videoDir+os.pathsep)
            else:
                print("no than lol.")
        elif(cmd == "help"):
            print("You are not supposed to be here, this place is for debugging.\nall - shows program variables\ndeldown - deletes your specific video and audio download folders\n<Enter> - return back to main menu")
        else:
            clear()
            name()
            break


# region ==========COLOR FUNCTIONS==========
def TF(var, newline=True):
    if newline:
        end = "\n"
    else:
        end = ""
  
    if (var):
        print(Fore.GREEN + str(var) + Style.RESET_ALL, end=end)
    elif (not var):
        print(Fore.RED + str(var) + Style.RESET_ALL, end=end)
    else:
        print("Not a boolean", end=end)


def BC(stri="no input", newline=True, reverse=False):
    if newline is True:
        end = "\n"
    else:
        end = ""

    if reverse:
        if(curb == "master"):
            branch = "testing"
        else:
            branch = "master"
    else:
        branch = curb  

    if(branch == "master"):
        print(Fore.CYAN + eval(f'f"""{stri}"""') + Style.RESET_ALL, end=end)
    else:
        print(Fore.MAGENTA + eval(f'f"""{stri}"""') + Style.RESET_ALL, end=end)
# endregion
