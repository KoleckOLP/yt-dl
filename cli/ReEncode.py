from colorama import init, Fore, Style  # Back
# Imports from this project
from release import settingsPath
from kolreq.kolreq import clear
from shared.ReEncode import reencode_shared, reencode_shared_settings

init()  # initialises colorama


def current_codec_print(name, videoc, videoq, audioc, audiob, append):
    print(Style.BRIGHT + f"{name}:" + Style.RESET_ALL)
    print("(video codec=\"", end="")
    print(Fore.YELLOW + videoc + Style.RESET_ALL, end="")
    print("\" video quality=\"", end="")
    print(Fore.YELLOW + videoq + Style.RESET_ALL, end="")
    print("\")")
    print("(audio codec=\"", end="")
    print(Fore.CYAN + audioc + Style.RESET_ALL, end="")
    print("\", video quality=\"", end="")
    print(Fore.CYAN + audiob + Style.RESET_ALL, end="")
    print("\")")
    print("(append=\"", end="")
    print(Fore.GREEN + append + Style.RESET_ALL, end="")
    print("\")")


def ReEncode(call):
    clear()
    current_codec_print("currently selected settings", call.settings.Ffmpeg.videoCodec, call.settings.Ffmpeg.videoQuality, call.settings.Ffmpeg.audioCodec, call.settings.Ffmpeg.audioBitrate, call.settings.Ffmpeg.append)
    print("\n<Enter> single video\n" +
            "1. whole folder\n" +
            "2. change settings\n" +
            "0. GoBack")
    cmd = input("#")
    # ========== THE ACTUAL REENCODE ========== #
    if (cmd == "" or cmd == "1"):
        print("write path to the file you want to reencode")
        url = input("#")
        if (url[0:3] == "& \'"):  # powershell (& ' ')
            url = url[3:-1]
        elif (url[0:1] == '\"'):  # cmd (" ")
            url = url[1:-1]
        elif (url[0:1] == "'"):  # posix (' ' )
            url = url[1:-2]

        result = reencode_shared(call, url, call.settings.Ffmpeg.videoCodec, call.settings.Ffmpeg.videoQuality, call.settings.Ffmpeg.audioCodec, call.settings.Ffmpeg.audioBitrate, call.settings.Ffmpeg.append)

        if isinstance(result, str):
            print(result)
        else:
            for line in result:
                print("#yt-dl# starting ffmpeg please wait...\n")

                call.process_start(line)

                print("\a")

    # ========== CHANGE SETTINGS ========== #
    elif (cmd == '2'):
        print("========== Options ==========")
        for i in range(0, 6):
            setting = reencode_shared_settings(call, i)
            current_codec_print(f"{i}, {setting[5]}", setting[0], setting[1], setting[2], setting[3], setting[4])
        print("========== Pick an Option ==========")
        print("0 - 4 to pick setting\n5 to keep current\n6 to edit custom")
        cmd = input("#")
        if cmd == "5":  # this is dumb lol
            pass
        if cmd == "6":
            print(f"type a video codec, current=\"{call.settings.Ffmpeg.videoCodec}\" <Enter> to keep")  # FIXME duplicite code
            cmd = input("#")
            if cmd == "":
                pass
            else:
                call.settings.Ffmpeg.videoCodec = cmd
            print(f"type a video quality, current=\"{ call.settings.Ffmpeg.videoQuality}\" <Enter> to keep")
            cmd = input("#")
            if cmd == "":
                pass
            else:
                call.settings.Ffmpeg.videoQuality = cmd
            print(f"type a audio codec, current=\"{call.settings.Ffmpeg.audioCodec}\" <Enter> to keep")
            cmd = input("#")
            if cmd == "":
                pass
            else:
                call.settings.Ffmpeg.audioCodec = cmd
            print(f"type a audio bitrate, current=\"{call.settings.Ffmpeg.audioBitrate}\" <Enter> to keep")
            cmd = input("#")
            if cmd == "":
                pass
            else:
                call.settings.Ffmpeg.audioBitrate = cmd
            print(f"type append, current=\"{call.settings.Ffmpeg.append}\" <Enter> to keep")
            cmd = input("#")
            if cmd == "":
                pass
            else:
                call.settings.Ffmpeg.append = cmd
        else:
            setting = reencode_shared_settings(call, int(cmd))
            call.settings.Ffmpeg.videoCodec = setting[0]
            call.settings.Ffmpeg.videoQuality = setting[1]
            call.settings.Ffmpeg.audioCodec = setting[2]
            call.settings.Ffmpeg.audioBitrate = setting[3]
            call.settings.Ffmpeg.append = setting[4]
        call.settings.toJson(settingsPath)
    else:
        clear()
        call.name()
