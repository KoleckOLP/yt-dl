import os
import glob
from colorama import init, Fore, Style  # Back
# Imports from this project
from release import spath, settingsPath
from kolreq.kolreq import clear, readchar
from shared.Config import Settings

init()  # initialises colorama


def Load(call, s="show"):
    # old mess
    pffmpeg = glob.glob(f"{spath}/ffmpeg*")
    pffprobe = glob.glob(f"{spath}/ffprobe*")
    if (not pffmpeg and not pffprobe):
        call.floc = False
    else:
        call.floc = spath
    # new stuff
    if (os.path.exists(settingsPath)):
        call.settings = Settings.fromJson(settingsPath)
    else:
        call.firstrun()

    if (s == "show"):
        print(Style.BRIGHT + "audio is saved to: " + Style.RESET_ALL, end="")
        print(call.settings.Youtubedl.audioDir)
        print(Style.BRIGHT + "video is saved to: " + Style.RESET_ALL, end="")
        print(call.settings.Youtubedl.videoDir + "\n")


def Save(call):
    Load(call)
    print("1. change download path\n2. delete settings\n3. generate Launch script\n0. GoBack")
    cmd = readchar("#")
    if (cmd == "1"):
        call.settings.toJson(settingsPath)
        clear()
        Load(call)
    elif (cmd == "2"):  # this is very wrong!
        os.remove(call.settings)
        call.firstrun()
    elif (cmd == "3"):
        print("press p=" + Fore.BLUE + "PowerShell" + Style.RESET_ALL + " or <Enter>")
        cmd = input("#")
        if (cmd == "p"):
            MakeScript(call, True)
        else:
            MakeScript(call)
        clear()
        call.name()
    else:
        clear()
        call.name()


def MakeScript(call, p=False):
    if call.is_venv:
        print("type name of your venv")
        cmd = input("#")
    else:
        cmd = ""

    if p:
        if(cmd != ""):
            f = open("yt-dl.ps1", "w")
            f.write(f"Set-Location {spath}{cmd}{os.path.sep}Scripts\n.{os.path.sep}Activate.ps1\nSet-Location {spath}\n{call.settings.Python.python} main.py")
            f.close()
        else:
            f = open("yt-dl.ps1", "w")
            f.write(f"Set-Location {spath}\n{call.settings.Python.python} main.py")
            f.close()
    else:
        if(cmd != ""):
            if(os.name == 'nt'):
                f = open("yt-dl.bat", "w")
                f.write(f"@echo off\n\ncmd /c \"cd /d {spath}{cmd}{os.path.sep}Scripts & activate & cd /d {spath} & {call.settings.Python.python} main.py\"")
                f.close()
            elif(os.name == 'posix'):
                f = open("yt-dl", "w")
                f.write(f"#!/bin/sh\n\ncd {spath}{cmd}{os.path.sep}bin && source activate && cd {spath} && {call.settings.Python.python} main.py")
                f.close()
            else:
                print('####If you see this please contact the dev. 0x1015####')
        else:
            if(os.name == 'nt'):
                f = open("yt-dl.bat", "w")
                f.write(f"@echo off\n\ncmd /c \"cd /d {spath} & {call.settings.Python.python} main.py\"")
                f.close()
            elif(os.name == 'posix'):
                f = open("yt-dl", "w")
                f.write(f"#!/bin/sh\n\ncd {spath} && {call.settings.Python.python} main.py")
                f.close()
            else:
                print('####If you see this please contact the dev. 0x1005####')
