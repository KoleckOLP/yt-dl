import sys
import subprocess
from typing import List
from colorama import init, Fore, Style  # Back
# Imports from this projects
from kolreq.kolreq import clear, readchar
from release import year, lstupdt, curb, ver, settingsPath
from shared.Config import Settings
from cli.Settings import Load, MakeScript

init()  # initialises colorama


class main:
    @staticmethod
    def is_venv():  # reports if user is in Virtual Environment or not
        return (hasattr(sys, 'real_prefix') or
                (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

    # ==========NAME========== #
    @staticmethod
    def name(newline=True):
        if newline:
            endWith = "\n"
        else:
            endWith = ""
        print(f"yt-dl {ver} cli ({curb} branch) by KoleckOLP (C){year}\n", end=endWith)

    # ==========FIRST TIME SETUP MENU========== #
    def firstrun(self):
        clear()
        self.settings = Settings.loadDefault()  # There is nothing wrong with this
        print("this program requires ffmpeg and ffprobe, please put them into the yt-dl directory")
        print("What's the name of your python executable.\n<enter> for python (apologise fo inconvenience)")
        self.settings.Python.python = input("#")
        if (self.settings.Python.python == ""):
            self.settings.Python.python = "python"
        print("What's the name of your pip executable.\n<Enter> for pip")
        self.settings.Python.pip = input("#")
        if (self.settings.Python.pip == ""):
            self.settings.Python.pip = "pip"
        print("Have you installed youtube-dl with pip? (yes if you installed requirements) [Y/n]")
        cmd = readchar("#")
        if (cmd == "y"):
            self.settings.Youtubedl.fromPip = True
        else:
            self.settings.Youtubedl.fromPip = False
        print("\nDo you want autoupdate on launch? [Y/n]")
        cmd = readchar("#")
        if (cmd == "y"):
            self.settings.autoUpdate = True
        else:
            self.settings.autoUpdate = False
        print()
        self.settings.Ffmpeg.videoCodec = "libx265"  # libx265, h264_nvenc
        self.settings.Ffmpeg.audioCodec = "opus"  # opus, acc
        self.settings.Ffmpeg.videoQuality = "24,24,24"  # 24
        self.settings.Ffmpeg.audioBitrate = "190k"  # 190
        self.settings.toJson(settingsPath)
        Load(self)
        print("Do you want a Launch script? [Y/n] or p=" + Fore.BLUE + "Powershell" + Style.RESET_ALL)
        cmd = readchar("#")
        if (cmd == "y"):
            MakeScript(self)
        elif(cmd == "p"):
            MakeScript(self, True)
        else:
            pass
        Load(self, "hid")
        self.about()

    # ==========ABOUT========== #
    def about(self):
        clear()
        self.name(False)
        print(f"HorseArmored inc (C){year}\n" +
              f"Version: {ver} cli ({curb} branch)\n" +
              f"Last updated on: {lstupdt}\n" +
              f"My webpage: https://koleckolp.comli.com/\n" +
              f"Project page: https://github.com/KoleckOLP/yt-dl\n" +
              f"need help? ask here: https://discord.gg/W88375j\n" +
              f"youtube-dl (C)2008-2011 Ricardo Garcia Gonzalez\n" +
              f"           (C)2011-{year} youtube-dl developers\n" +
              f"ffmpeg (C)2000-{year} FFmpeg team\n" +
              f"Thanks to kangalioo who always helps a ton!")
        print(Style.BRIGHT + "Do you want to see whats new? [Y/n]" + Style.RESET_ALL)
        cmd = readchar("#")
        if (cmd == "y"):
            clear()
            fh = open("changelog.md", "r")
            print(fh.read()+"\n")
            fh.close()
        else:
            clear()
            self.name()

    @staticmethod
    def process_start(cmd: List[str]):  # FIXME when calling update the screen cleans and you can't read how the update went.
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                                   errors="ignore")
        while True:
            test = process.stdout.readline()
            if not test:
                break
            if "\n" in test:
                test = test.replace("\n", "")
            print(test)

    @staticmethod
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
