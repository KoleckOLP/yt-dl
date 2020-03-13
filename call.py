from getch import getch #py-getch
from datetime import datetime
from time import sleep
import subprocess
import tempfile
import sys, os
import glob
import json

year = datetime.now().year
ver = "2.1.3"
lstupdt = "13.03.2020"
spath = sys.path[0]+os.path.sep
settings = spath+"settings.json"

def name():
    print(f"yt-dl {ver} by KoleckOLP (C){year}\n")

def clear():
    if(os.name == 'nt'):
        os.system('cls')
    elif(os.name == 'posix'):
        os.system('clear')
    else:
        print('####If you see this please contact the dev. 0x2020####')

def readchar(o): #multiplatform readchar
    print(o, end="", flush=True) #writes text before the getch, no new line, flush output
    x = getch()
    if isinstance(x, bytes): #fix if returned in bytes, need to fix when input is arrowkeys
         x = x.decode("UTF-8")
    x = x.lower()
    return x  

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
    print("Have you installed youtube-dl with pip? [Y/n]]")
    cmd = readchar("#")
    print()
    if (cmd == "y"):
        ydpip = True
    else:
        ydpip = False
    savepath(py,pip,ydpip)
    loadpath("hid")
    about()   

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

def savepath(x="", y="", z=""):
    print("Type path were you want to store audio,"
             +"\n<Enter> a default subdir 0. GoBack")
    aud = input("#")
    if(aud == "0"):
        clear()
        name()
    else:
        if(aud == ""):
            aud = spath+"audio"
        print("Type path were you want to store videos,"
             +"\n<Enter> a default subdir 0. GoBack")
        vid = input("#")
        if(vid == "0"):
            clear()
            name()
        else:
            if(vid == ""):
                vid = spath+"videos"
            if(x == "" and y == "" and z == ""):
                loadpath("hid")
                x = py
                y = pip
                z = ydpip
            fh = open(settings, "w")
            json.dump({"audio": aud+os.path.sep,"videos": vid+os.path.sep,"py": x,"pip": y,"ydpip": z}, fh)
            fh.close()

def loadpath(s="show"):
    global audio
    global videos
    global py
    global pip
    global ydpip
    fh = open(settings, "r")
    path = json.loads(fh.read())
    fh.close()
    try:
        path["audio"]
        path["videos"]
        path["py"]
        path["pip"]
        path["ydpip"]
    except KeyError:
        firstrun()
    else:
        audio = path["audio"]
        videos = path["videos"]
        py = path["py"]
        pip = path["pip"]
        ydpip = path["ydpip"]
    if(s == "show"):
        print(f"audio is saved to: {audio}\nvideo is saved to: {videos}\n")

def slpath():
    loadpath()
    print("1. change download path\n2. delete settings\nor any key to continue...")
    cmd = readchar("#")
    if (cmd == "1"):
        savepath()
        clear()
        loadpath()
    elif (cmd == "2"):
        os.remove(settings)
        firstrun()
    else:
        clear()
        name()

def upytdl():
    print("Updating yt-dl...")
    if(os.path.exists(spath+".git")):
        os.system("cd "+spath)
        os.system("git pull")
    else:
        print("yt-dl wasn't installed trought git.\n"
        +"delete yt-dl and install it with \"git clone https://github.com/KoleckOLP/yt-dl.git\"")    

def upyd():
    print("Updating youtube-dl...")
    subprocess.call([pip, 'install', '--upgrade', 'youtube-dl'])

def update():
    clear()
    if(ydpip == True):
        print("What do you want to update?\n1. All(yt-dl & youtube-dl)\n2. yt-dl\n3. youtube-dl\n0. GoBack")
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
        else:
            clear()
            name()
    else:
        upytdl()

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
        if(numb == ""):
            lnk = f"-o \"{audio}%(title)s.%(ext)s\" --no-playlist -x --prefer-ffmpeg --audio-format mp3 \"{url}\""
        elif(numb == "1"):
            lnk = f"-o \"{audio}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i -x --prefer-ffmpeg --audio-format mp3 \"{url}\""
        else:
            lnk = f"-o \"{audio}%(playlist_index)s. %(title)s.%(ext)s\" --yes-playlist -i --playlist-items {numb} -x --prefer-ffmpeg --audio-format mp3 \"{url}\""
        os.system("youtube-dl "+lnk)
        print("\a")

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
            print(f"audio is saved to: {audio}\nvideo is saved to: {videos}\npython executable name: {py}\npip executable name: {pip}\nyoutube-dl from pip: {ydpip}\nyt-dl from git: {git}")
        elif(cmd == "all"):
            print("Paths:")
            for p in sys.path: print(p)
            print("Saves:")
            if(os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0]))+os.path.sep+".git")):
                git = True
            else:
                git = False
            print(f"audio is saved to: {audio}\nvideo is saved to: {videos}\npython executable name: {py}\npip executable name: {pip}\nyoutube-dl from pip: {ydpip}\nyt-dl from git: {git}")
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