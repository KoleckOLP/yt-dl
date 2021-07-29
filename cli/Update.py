import os
from colorama import init, Fore, Style  # Back
# Imports from this project
from release import spath, settingsPath
from kolreq.kolreq import clear, readchar
from cli.Settings import Load

init()  # initialises colorama


def upytdl():
    print("Updating yt-dl...")
    if (os.path.exists(spath + ".git")):
        os.system("cd " + spath)
        os.system("git pull --recurse-submodules")
    else:
        print("yt-dl wasn't installed trough git.\n" +
              "delete yt-dl and install it with \"git clone https://github.com/KoleckOLP/yt-dl.git\"")


def upyd(call):
    print("updating pip...")
    os.system(
        f"{call.settings.Python.python} -m {call.settings.Python.pip} install --upgrade {call.settings.Python.pip}")
    print("Updating dependencies...")
    os.system(f"{call.settings.Python.pip} install -U -r req-cli.txt")


def Update(call):
    clear()
    if call.settings.Youtubedl.fromPip:
        print(Style.BRIGHT + f"What do you want to update?" + Style.RESET_ALL + "\n1. All\n2. yt-dl\n3. dependencies\n4. change autoupdate=",end="")
        call.TF(call.settings.autoUpdate, False)
        print("\n0. GoBack")
        cmd = readchar("#")
        if (cmd == "1"):  # All
            clear()
            upytdl()
            upyd(call)
            print(Fore.RED, "\n!!!restart for changes to take effect!!!\n", Style.RESET_ALL)
        elif (cmd == "2"):  # yt-dl
            clear()
            upytdl()
            print(Fore.RED, "\n!!!restart for changes to take effect!!!\n", Style.RESET_ALL)
        elif (cmd == "3"):  # youtube-dl
            clear()
            upyd(call)
            print("")
        elif (cmd == "4"):
            call.settings.autoUpdate = not call.settings.autoUpdate
            call.settings.toJson(settingsPath)
            Load(call)
            clear()
            print(f"autoupdate={call.settings.autoUpdate}\n")
        else:
            clear()
            call.name()
    else:
        upytdl()


def AutoUpdate(call):
    print(f"autoupdate=", end="")
    call.TF(call.settings.autoUpdate)
    if call.settings.autoUpdate:
        upytdl()
        upyd(call)
        print()
    else:
        print()
