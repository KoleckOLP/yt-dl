import os  # importing os so I can os.system to install dependencies
try:
    import getch  # testing if dependencies are installed, not used in main.py
    import colorama  # point sf this is preventing crashes on missing dependencies in kolreq submodule and call.py
except ModuleNotFoundError:
    print("You are missing dependencies, we'll try to install them with pip.")
    input("press any key to continue")
    print("Do you with to update pip first? If yes type the name of you python executable.")
    cmd = input("#")
    if (cmd != ""):
        py = cmd
        print("updating pip...")
        os.system(f"{py} -m pip install -U pip")
    print("installing dependencies...")
    os.system("pip install -r req-cli.txt")

try:
    from kolreq.kolreq import clear, readchar  # testing if submodule is installed and importing it
except ModuleNotFoundError:
    print("this program requires a submodule that will download now.")
    input("press any key to continue")
    os.system("git submodule init")
    os.system("git pull --recurse-submodules")
    print("If the submodule installed correctly restart to get first time setup.")
    input("press any key to continue")
    exit()

from release import settingsPath
from cli.call import main
from cli.Audio import Audio
from cli.Video import Video
from cli.Subs import Subs
from cli.ReEncode import ReEncode
from cli.Debug import Debug  # this comment fixes a warning
from cli.Update import Update, AutoUpdate
from cli.Settings import Load, Save

clear()

call = main()

if(os.path.exists(settingsPath)):
    call.name()
    Load(call)
    AutoUpdate(call)
else:
    call.firstrun()

while(True):
    print("1. Audio\t5. Re-encode\n2. Video\t6. Update\n3. Exit\t\t7. Download path\n4. Subtitles\t8. About, Changelog")
    cmd = readchar("#")

    if(cmd == "1"):  # audio
        Audio(call)
    elif(cmd == "2"):  # video
        Video(call)
    elif(cmd == "3"):  # exit
        print("See you later alligator.")
        break
    elif(cmd == "4"):  # subtitles
        Subs(call)
    elif(cmd == "5"):  # re-encode
        ReEncode(call)
    elif(cmd == "6"):  # update
        Update(call)
    elif(cmd == "7"):  # save load path
        clear()
        Save(call)
    elif(cmd == "8"):  # about
        call.about()
    elif(cmd == ";"):  # debug (usually '`' but I don't have that key on my czech work laptop keyboard)
        Debug(call)
    else:
        clear()
        print(f"\"{cmd}\" is not an option.")
