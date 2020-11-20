import os #importing os so I can os.system to install dependecies
try:
    import getch #testing if dependecies are installed, not used in main.py
    import colorama #point sf this is preventing crashes on missing dependencies in kolreq submodule and call.py
except ModuleNotFoundError:
    print("You are missing dependencies, we'll try to install them with pip.")
    input("press any key to continue")
    print("Do you with to update pip first? If yes type the name of you python exectable.")
    cmd = input("#")
    if (cmd != ""):
        py = cmd
        print("updating pip...")
        os.system(f"{py} -m pip install -U pip")
    print("installing dependecies...")
    os.system("pip install -r requirements.txt")

try:
    from kolreq.kolreq import clear, readchar #testing if submodule is installed and importing it
except ModuleNotFoundError:
    print("this program requires a submodule that will downlosad now.")
    input("press any key to continue")
    os.system("git submodule init")
    os.system("git pull --recurse-submodules")
    print("If the submodule installed correctly restart to get first time setup.")
    input("press any key to continue")
    exit()

from call import settings, name, loadpath, autoupdt, firstrun, audiod, videod, subd, reencode, update, slpath, about, debug

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
    elif(cmd == "5"): #re-encode
        reencode()
    elif(cmd == "6"): #update
        update()
    elif(cmd == "7"): #save load path
        clear()
        slpath()
    elif(cmd == "8"): #about
        about()
    elif(cmd == ";"): #debug (usually '`' but I don't have that key on my czech work laptop keyboard)
        debug()
    else:
        clear()
        print(f"\"{cmd}\" is not an option.")