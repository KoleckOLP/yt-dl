import os
import sys
from colorama import init, Fore, Style  # Back
# Imports from this project
from kolreq.kolreq import clear, readchar
from cli.Settings import Load

init()  # initialises colorama


def Debug(call):
    print(Fore.MAGENTA + "Welcome to debug menu:", Style.RESET_ALL)
    while(True):
        cmd = input(">")
        if(cmd == "all"):
            print("Paths:")
            for p in sys.path:
                print(p)
            print("\nSaves:")
            if(os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0])) + os.path.sep + ".git")):
                git = True
            else:
                git = False
            Load(call)
            print("Variables:")
            print(f"python executable name: {call.settings.Python.python}\npip executable name: {call.settings.Python.pip}")
            print("youtube-dl from pip: ", end="")
            call.TF(call.settings.Youtubedl.fromPip)
            print(f"ffmpeg in yt-dl dir: {call.floc}")
            print("yt-dl from git: ", end="")
            call.TF(git)
            print("autoupdate: ", end="")
            call.TF(call.settings.autoUpdate)
            print(f"videoCodec: {call.settings.Ffmpeg.videoCodec}\naudioCodec: {call.settings.Ffmpeg.audioCodec}\nvideoQuality: {call.settings.Ffmpeg.videoQuality}\naudioBitrate: {call.settings.Ffmpeg.audioBitrate}")
            if call.is_venv():
                venv = True
            else:
                venv = False
            print("in venv: ", end="")
            call.TF(venv)
        elif(cmd == "deldown"):
            print("Are you sure you want to delete all audio and videos [Y/n]")
            cmd = readchar("")
            if(cmd == "y"):
                if(os.name == 'nt'):
                    os.system('del  ' + call.settings.Youtubedl.audioDir)
                    os.system('del  ' + call.settings.Youtubedl.videoDir)
                elif(os.name == 'posix'):
                    os.system('rm  ' + call.settings.Youtubedl.audioDir + os.pathsep)
                    os.system('rm  ' + call.settings.Youtubedl.videoDir + os.pathsep)
            else:
                print("no than lol.")
        elif(cmd == "help"):
            print("You are not supposed to be here, this place is for debugging.\nall - shows program variables\ndeldown - deletes your specific video and audio download folders\n<Enter> - return back to main menu")
        else:
            clear()
            call.name()
            break
