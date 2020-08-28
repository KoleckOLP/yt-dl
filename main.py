import os
try:
    from getch import getch #py-getch
    from colorama import init, Fore, Back, Style
except ModuleNotFoundError:
    print("You are missing dependencies do you want to install them with pip? [Y/n]")
    cmd = input("#")
    if(cmd == "y" or cmd == "Y"):
        print("Do you with to update pip first? If yes type the name of you python exectable.")
        cmd = input("#")
        if (cmd != ""):
            py = cmd
            print("updating pip...")
            os.system(f"{py} -m pip install -U pip")
        print("installing dependecies...")
        os.system("pip install -r requirements.txt")
        print("\n\nif all went well, restart yt-dl and it will work\nIf not run \"pip install -r requirements.txt\"\nYou should also install ffmpeg and add it to PATH")
        input("press any key to quit")
        exit()
    else:
        print("install them before you can use yt-dl\nYou should also install ffmpeg and add it to PATH")
        input("press any key to quit")
        exit()

from kolreq import clear, readchar
from call import settings, name, loadpath, autoupdt, firstrun, audiod, videod, subd, vidhevc, update, slpath, about, debug

clear()

if(os.path.exists(settings)):
    name()
    loadpath()
    autoupdt()
else:
    firstrun()

while(True):
    print("1. Audio\t5. Re-encode\n2. Video\t6. Update\n3. Exit\t\t7. Download path\n4. Subtitles\t8. About, Changelog")
    cmd = readchar("#")

    if(cmd == "1"): #audio
        audiod()
    elif(cmd == "2"): #video
        videod()
    elif(cmd == "3"): #exit
        print("See you later aligator.")
        break
    elif(cmd == "4"): #subtitles
        subd()
    elif(cmd == "5"): #vid to hevc
        vidhevc()
    elif(cmd == "6"): #update
        update()
    elif(cmd == "7"): #save load path
        clear()
        slpath()
    elif(cmd == "8"): #about
        about()
    elif(cmd == "`"): #debug
        debug()
    else:
        clear()
        print(f"\"{cmd}\" is not an option.")