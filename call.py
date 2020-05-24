from getch import getch #py-getch
from datetime import datetime
from time import sleep
import tempfile
import sys, os
import glob
import json

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

year = datetime.now().year
curb = "testing"
ver = f"2.1.5RC1-{curb}" #lang(2python3) #featureset #patch/bugfix pre, RC
lstupdt = "2020-05-24"
spath = sys.path[0]+os.path.sep
settings = spath+"settings.json"

#==========NAME==========#
def name():
    print(f"yt-dl {ver} by KoleckOLP (C){year}\n")

#==========MUSTYPLAT CLEAR==========#
def clear():
    if(os.name == 'nt'):
        os.system('cls')
    elif(os.name == 'posix'):
        os.system('clear')
    else:
        print('####If you see this please contact the dev. 0x2020####')

#==========MULTYPLAT READKEY==========#
def readchar(o): #multiplatform readchar
    print(o, end="", flush=True) #writes text before the getch, no new line, flush output
    x = getch()
    if isinstance(x, bytes): #fix if returned in bytes, need to fix when input is arrowkeys
         x = x.decode("UTF-8")
    x = x.lower()
    return x  

#==========FIRST RUN MENU==========#
def firstrun():
    clear()
    print("What's the name of your python executable.\n<enter> for python")
    py = input("#")
    if (py == ""):
        py = "python"
    print("What's the name of your pip executable.\n<Enter> for pip")
    pip = input("#")
    if (pip == ""):
        pip = "pip"
    print("Have you installed youtube-dl with pip? [Y/n]")
    cmd = readchar("#")
    if (cmd == "y"):
        ydpip = True
    else:
        ydpip = False
    print("\nDo you want autoudate on launch? [Y/n]")
    cmd = readchar("#")
    if (cmd == "y"):
        aup = True
    else:
        pass
    print()
    savepath("chp",py,pip,ydpip,aup)
    loadpath()
    print("Do you want a Launch script? [Y/n] or p=Powershell")
    cmd = readchar("#")
    if (cmd == "y"):
        launchs()
    elif(cmd== "p"):
        launchs(True)
    else:
        pass
    loadpath("hid")
    about()

#==========MAKE LAUNCH SCRIPT==========#
def launchs(p=""):
    print(f"Do you have venv set up if yes type name of the venv")
    cmd = input("#")
    if(p==True):
        if(cmd != ""):
            f=open("yt-dl.ps1","w")
            f.write(f"Set-Location {spath}{cmd}{os.path.sep}Scripts\n.{os.path.sep}Activate.ps1\nSet-Location {spath}\n{py} main.py")
            f.close()
        else:
            f=open("yt-dl.bat","w")
            f.write(f"Set-Location {spath}\n{py} main.py")
            f.close()
    else:
        if(cmd != ""):
            if(os.name == 'nt'):
                f=open("yt-dl.bat","w")
                f.write(f"@echo off\n\ncmd /c \"cd /d {spath}{cmd}{os.path.sep}Scripts & activate & cd /d {spath} & {py} main.py\"")
                f.close()
            elif(os.name == 'posix'):
                f=open("yt-dl","w")
                f.write(f"#!/bin/bash\n\ncd {spath}{cmd}{os.path.sep}bin && source activate && cd {spath} && {py} main.py")
                f.close()
            else:
                print('####If you see this please contact the dev. 0x1015####')
        else:
            if(os.name == 'nt'):
                f=open("yt-dl.bat","w")
                f.write(f"@echo off\n\ncmd /c \"cd /d {spath} & {py} main.py\"")
                f.close()
            elif(os.name == 'posix'):
                f=open("yt-dl","w")
                f.write(f"#!/bin/bash\n\ncd {spath} && {py} main.py")
                f.close()
            else:
                print('####If you see this please contact the dev. 0x1005####')

#==========ABOUT==========#
def about():
    clear()
    print(f"yt-dl version: {ver} by KoleckOLP,\n"
         +f"HorseArmored inc (C){year}\n"
         +f"Last updated on: {lstupdt}\n"
         +f"My webpage: https://koleckolp.comli.com/\n"
         +f"Project page: https://github.com/KoleckOLP/yt-dl\n"
         +f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez\n"
         +f"           (C)2011-{year} youtube-dl developers\n"
         +f"ffmpeg (C)2000-{year} FFmpeg team")
    print("Do you want to see whats new? [Y/n]")
    cmd = readchar("#")
    if (cmd == "y"): 
        clear()
        fh = open("whatsnew.md", "r")
        print(fh.read()+"\n")
        fh.close()
    else:
        clear()
        name()

#==========SAVE PATH==========#
def savepath(a="chp", x="", y="", z="", q=""):
    if (a == "chp"):
        print("Type path were you want to store audio,"
                  +"\n<Enter> a default subdir 0. GoBack")
        aud = input("#")
        if (aud == "0"):
            clear()
            name()
        else:
            if (aud == ""):
                aud = spath+"audio"
            print("Type path were you want to store videos,"
                 +"\n<Enter> a default subdir 0. GoBack")
            vid = input("#")
            if (vid == "0"):
                clear()
                name()
            else:
                if (vid == ""):
                    vid = spath+"videos"
                    fh = open(settings, "w")
                    json.dump({"audio": aud+os.path.sep,"videos": vid+os.path.sep,"py": x,"pip": y,"ydpip": z,"aup": q}, fh)
                    fh.close()
                else:
                    fh = open(settings, "w")
                    json.dump({"audio": aud+os.path.sep,"videos": vid+os.path.sep,"py": x,"pip": y,"ydpip": z,"aup": q}, fh)
                    fh.close()
    if (a != "chp"):
        loadpath("hid")
        fh = open(settings, "w")
        json.dump({"audio": audio,"videos": videos,"py": x,"pip": y,"ydpip": z,"aup": q}, fh)
        fh.close()
    
        
#==========LOAD PATH==========#
def loadpath(s="show"):
    global audio
    global videos
    global py
    global pip
    global ydpip
    global aup
    fh = open(settings, "r")
    try:
        path = json.loads(fh.read())
    except ValueError:
        firstrun()
        path = json.loads(fh.read())
    fh.close()
    try:
        path["audio"]
        path["videos"]
        path["py"]
        path["pip"]
        path["ydpip"]
        path["aup"]
    except KeyError:
        firstrun()
    else:
        audio = path["audio"]
        videos = path["videos"]
        py = path["py"]
        pip = path["pip"]
        ydpip = path["ydpip"]
        aup = path["aup"]
    if(s == "show"):
        print(f"audio is saved to: {audio}\nvideo is saved to: {videos}\n")

#==========SAVE MENU==========#
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
        print("press p=Powershell or <Enter>")
        cmd=input("#")
        if(cmd=="p"):
            launchs(True)
        else:
            launchs()
        clear()
        name()
    else:
        clear()
        name()

#==========UPDATE YTDL==========#
def upytdl():
    print("Updating yt-dl...")
    if(os.path.exists(spath+".git")):
        os.system("cd "+spath)
        os.system("git pull")
    else:
        print("yt-dl wasn't installed trought git.\n"
        +"delete yt-dl and install it with \"git clone https://github.com/KoleckOLP/yt-dl.git\"")    

#==========UPDATE DEPEND==========#
def upyd():
    print("updating pip...")
    os.system(f"{py} -m {pip} install --upgrade {pip}")
    print("Updating dependencies...")
    os.system(f"{pip} install -U -r requirements.txt")

#==========UPDATE MENU==========#
def update():
    clear()
    global aup
    if(ydpip == True):
        print(f"What do you want to update?\n1. All\n2. yt-dl\n3. dependencies\n4. change autoupdate={aup}\n5. change branch\n0. GoBack")
        cmd = readchar("#")
        if(cmd == "1"): #All
            clear()
            upytdl()
            upyd()
            print("\n!!!restart for chanes to take effect!!!\n")
        elif(cmd == "2"): #yt-dl
            clear()
            upytdl()
            print("\n!!!restart for chanes to take effect!!!\n")
        elif(cmd == "3"): #youtube-dl
            clear()
            upyd()
            print("")
        elif (cmd == "4"):
            aup = not aup
            savepath("",py,pip,ydpip,aup)
            loadpath("hid")
            clear()
            print(f"autoupdate={aup}\n")
        elif(cmd == '5'):
            clear()
            print(f"What branch do you wat to change to? You are in a {curb}")
            if (curb == "master"):
                otherb = "testing"
            else:
                otherb = "master"
            print(f"do you want to switch to {otherb} [Y/n]")
            cmd = readchar("#")
            if (cmd == "y"):
                os.system(f"git checkout {otherb}")
                print("\n!!!restart for chanes to take effect!!!\n")
            else:
                pass
        else:
            clear()
            name()
    else:
        upytdl()

#==========AUTO UPDATE==========#
def autoupdt():
    print(f"autoupdate={aup}")
    if (aup == True):
        upytdl()
        upyd()
        print()
    else:
        print()

#==========AUDIO DOWNLOAD==========#
def audiod():
    clear()
    print("link to audio, playlist, 0. GoBack")
    url = input("#")
    if(url == "0"):
        clear()
        name()
    else:
        print("<Enter> a single audio, \n"
             +"1. to download full playlist or follow example 1-3,7,9")
        numb = input("#")
        print("starting youtube-dl please wait...")
        if(numb == ""):
            lnk = f"-o \"{audio}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg --audio-format mp3 \"{url}\""
        elif(numb == "1"):
            lnk = f"-o \"{audio}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i -x --prefer-ffmpeg --audio-format mp3 \"{url}\""
        else:
            lnk = f"-o \"{audio}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i --playlist-items {numb} -x --prefer-ffmpeg --audio-format mp3 \"{url}\""
        os.system("youtube-dl "+lnk)
        print("\a")

#==========VIDEO DOWNLOAD==========#
def videod():
    clear()
    print("link to video, playlist, 0. GoBack")
    url = input("#")
    if (url == "0"):
        clear()
        name()
    else:
        print("<Enter> a single video, \n"
             +"1. to download full playlist or follow example 1-3,7,9")
        numb = input("#")
        print("starting youtube-dl please wait...")
        if(numb == ""): #no playlist
            print("<Enter> for best quality 1080p + if availeble,\n"
                 +"1 for 720 or lower\n"
                 +"2 to choose yourself")
            qual = input("#")
            if (qual == "1"):
                lnk = f"-o \"{videos}%(title)s.%(ext)s\" -f best --no-playlist --prefer-ffmpeg \"{url}\""
            elif(qual == "2"):
                os.system(f"youtube-dl -F --no-playlist {url}")
                print("choose video and audio quality by typing numb+numb")
                numb = input("#")
                lnk = f"-o \"{videos}%(title)s.%(ext)s\" -f \"{numb}\" --no-playlist --prefer-ffmpeg \"{url}\""
            else:
                lnk = f"-o \"{videos}%(title)s.%(ext)s\" -f bestvideo+bestaudio --no-playlist --prefer-ffmpeg \"{url}\""
        else: #playlist
            print("<Enter> for the best quality 1080p + if available, \n"
                 +"1 for 720p or lower")
            qual = input("#")
            if(qual == "1"): 
                if(numb == "1"):
                    lnk = f"-o \"{videos}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --prefer-ffmpeg \"{url}\""
                else:
                    lnk = f"-o \"{videos}%(playlist_index)s. %(title)s.%(ext)s\" -f best --yes-playlist --playlist-items {numb} --prefer-ffmpeg \"{url}\""
            else:
                if(numb == "1"):
                    lnk = f"-o \"{videos}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --prefer-ffmpeg \"{url}\""
                else:
                    lnk = f"-o \"{videos}%(playlist_index)s. %(title)s.%(ext)s\" -f bestvideo+bestaudio --yes-playlist --playlist-items {numb} --prefer-ffmpeg \"{url}\""
        os.system("youtube-dl "+lnk)
        print("\a")

#==========SUBTITILE DOWNLOAD==========#
def subd():
    clear()
    temp = tempfile.mkdtemp()+os.path.sep
    print("link to video with subs or 0. GoBack")
    url = input("#")
    if (url == "0"):
        clear()
        name()
    else:
        print("<Enter> to download default sub (en),\n"
             +"1 to choose language")
        numb = input("#")
        if(numb == ""):
            lnk = f"-o \"{temp}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-format vtt --skip-download --prefer-ffmpeg \"{url}\""
        else:
            os.system(f"youtube-dl --list-subs --noplaylist {url}")
            print("choose sub language")
            numb = input("#")
            lnk = f"-o \"{temp}%(title)s.%(ext)s\" --no-playlist --write-sub --write-auto-sub --sub-lang \"{numb}\" --sub-format vtt --skip-download --prefer-ffmpeg \"{url}\""
        os.system("youtube-dl "+lnk)
        pie = glob.glob(f"{temp}*.vtt")
        cream = os.path.basename(pie[0])
        cream = cream[:-3]
        lick = videos+cream+"srt"
        os.makedirs(videos, exist_ok=True)
        os.system(f"ffmpeg -i \"{pie[0]}\" \"{lick}\"")
        print("\a")

#==========VID TO HEVC==========#
def vidhevc():
    clear()
    print("<Enter> single video 1. numbered series")
    cmd = input("#")
    if(cmd == ""): #single
        print("write path to the file you want to reencode")
        url = input("#")
        print("reenceded file will get \"_lib265.mkv\" appended, or type a different one")
        append = input("#")
        if(append == ""):
            append = "_lib265.mkv"
        os.system(f"ffmpeg -hwaccel auto -i \"{url}\" -map 0:v -map 0:a -map 0:s? -c:v libx265 -rc constqp -qp 24 -b:v 0K -c:a aac -b:a 384k -c:s copy \"{os.path.splitext(url)[0]+append}\"")
        print("\a")
    elif(cmd == "1"): #numbered
        print("write path to the folder with videos don't forget to add \\*.extencion")
        url = input("#")
        print("type a short path of the episode name just before the number")
        common_name = input("#")
        print("Write the highest number of the video")
        numb_last = input("#")
        try:
            numb_last = int(numb_last)
        except ValueError:
            clear()
            print("That's not a number")
            name()
        print("Write the number you want to start from <Enter> for 1")
        numb = input("#")
        if(numb == ""):
            numb = 1
        else:
            try:
                numb = int(numb)
            except ValueError:
                clear()
                print("That's not a number")
                name()
        print("does the numbers use zero padding [Y/n]")
        zero = readchar("#")
        print("\nreenceded file will get \"_lib265\" appended, or type a different one")
        append = input("#")
        if(append == ""):
            append = "_lib265"
        episodes = glob.glob(url)
        for numb in range(numb, numb_last+1):
            if(zero == "y"):
                if(numb < 10):
                        numb_final = "0"+str(numb)
                        numb_final = common_name+str(numb_final)
                else:
                    numb_final = numb
                    numb_final = common_name+str(numb_final)
            for i in episodes:
                if str(numb_final) in i:
                    filename = os.path.basename(i)
                    file_split = filename.split(".", 1)
                    path = os.path.dirname(i)
                    finali = path+os.path.sep+file_split[0]+append+".mkv"
                    os.system(f"ffmpeg -hwaccel auto -i \"{i}\" -map 0:v -map 0:a -map 0:s? -c:v libx265 -rc constqp -qp 24 -b:v 0K -c:a aac -b:a 384k -c:s copy \"{finali}\"")
    else:
        clear()
        name()

#==========DEBUG CONSOLE==========#
def debug():
    print("Welcome to debug menu:")
    while(True):
        cmd = input(">")
        if (cmd == "paths"):
            print("Paths:")
            for p in sys.path: print(p)
        elif(cmd == "saves"):
            print("Saves:")
            if(os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0]))+os.path.sep+".git")):
                git = True
            else:
                git = False
            print(f"audio is saved to: {audio}\nvideo is saved to: {videos}\npython executable name: {py}\npip executable name: {pip}\nyoutube-dl from pip: {ydpip}\nyt-dl from git: {git}\nautoupdate: {aup}")
        elif(cmd == "all"):
            print("Paths:")
            for p in sys.path: print(p)
            print("Saves:")
            if(os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0]))+os.path.sep+".git")):
                git = True
            else:
                git = False
            print(f"audio is saved to: {audio}\nvideo is saved to: {videos}\npython executable name: {py}\npip executable name: {pip}\nyoutube-dl from pip: {ydpip}\nyt-dl from git: {git}\nautoupdate: {aup}")
            if is_venv():
                venv = True
            else:
                venv = False
            print(f"in venv: {venv}")
        elif(cmd == "deldown"):
            print("Are you sure you want to delete all audio and videos [Y/n]")
            cmd = readchar("")
            if(cmd == "y"):
                if(os.name == 'nt'):
                    os.system('del '+audio)
                    os.system('del '+videos)
                elif(os.name == 'posix'):
                    os.system('rm '+audio+os.pathsep)
                    os.system('rm '+videos+os.pathsep)
            else:
                print("no than lol.")
        else:
            clear()
            name()
            break    