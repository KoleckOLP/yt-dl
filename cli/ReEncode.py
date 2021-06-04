import os
import glob
from colorama import init, Fore, Style  # Back
# Imports from this project
from release import spath, settingsPath
from kolreq.kolreq import clear

init()  # initialises colorama


def ReEncode(call):
    if call.fdir:
        floc = f"{spath}"
    else:
        floc = ""

    clear()
    print(
        Fore.RED + "Files with special characters in the path may not work, also keep filenames short" + Style.RESET_ALL)
    print("(video codec=\"", end="")
    if (call.settings.Ffmpeg == "none"):
        print(Fore.RED + call.settings.Ffmpeg.videoCodec + Style.RESET_ALL, end="")
    else:
        print(Fore.YELLOW + call.settings.Ffmpeg.videoCodec + Style.RESET_ALL, end="")
    print(
        "\", audio codec=\"" + Fore.CYAN + call.settings.Ffmpeg.audioCodec + Style.RESET_ALL + "\", video q,qmin,qmax=\"",
        end="")
    if (call.settings.Ffmpeg.videoCodec == "none"):
        print(Fore.RED + call.settings.Ffmpeg.videoQuality + Style.RESET_ALL, end="")
    else:
        print(Fore.YELLOW + call.settings.Ffmpeg.videoQuality + Style.RESET_ALL, end="")
    print("\", audio bitrate=\"" + Fore.CYAN + call.settings.Ffmpeg.audioBitrate + Style.RESET_ALL + "\")\n" +
          "<Enter> single video\n" +
          "1. whole folder\n" +
          "2. change settings\n" +
          "0. GoBack")
    cmd = input("#")
    if (cmd == ""):  # ====================SINGLE==================== #
        if (call.settings.Ffmpeg.videoCodec == "remove" and call.settings.Ffmpeg.audioCodec == "remove"):
            print("I mean you can delete the file yourself. :)")
        else:
            print("write path to the file you want to reencode")
            url = input("#")
            if (url[0:3] == "& \'"):  # powershell (& ' ')
                url = url[3:-1]
            elif (url[0:1] == '\"'):  # cmd (" ")
                url = url[1:-1]
            elif (url[0:1] == "'"):  # posix (' ' )
                url = url[1:-2]
            # //append\\ #
            if (call.settings.Ffmpeg.videoCodec == "remove"):
                print("re-encoded file will get \".mp3\" appended, or type a different one")
                append = input("#")
                if (append == ""):
                    append = ".mp3"
            else:
                print("re-encoded file will get \"_hevcopus.mkv\" appended, 1. \"_nvenc.mov\" or type a different one")
                append = input("#")
                if (append == ""):
                    append = "_hevcopus.mkv"
                elif (append == "1"):
                    append = "_nvenc.mov"
            # //Video Quality\\ #
            if "," in call.settings.Ffmpeg.videoQuality:
                VQsplit = call.settings.Ffmpeg.videoQuality.split(",")
            else:
                VQsplit = [call.settings.Ffmpeg.videoQuality, call.settings.Ffmpeg.videoQuality,
                           call.settings.Ffmpeg.videoQuality]
            # //Video Codec\\ #
            if (call.settings.Ffmpeg.videoCodec == "libx265"):
                VideoCodec = f"-c:v {call.settings.Ffmpeg.videoCodec}"
                quality = f"-crf {int(VQsplit[0]) - 1} -qmin {int(VQsplit[1]) - 1} -qmax {int(VQsplit[2]) - 1}"
                Vformat = "-vf format=yuv420p"
            elif (call.settings.Ffmpeg.videoCodec == "copy"):
                VideoCodec = f"-c:v {call.settings.Ffmpeg.videoCodec}"
                quality = ""
                Vformat = ""
            elif (call.settings.Ffmpeg.videoCodec == "remove"):
                VideoCodec = "-vn"
                quality = ""
                Vformat = ""
            else:
                VideoCodec = f"-c:v {call.settings.Ffmpeg.videoCodec}"
                quality = f"-cq {VQsplit[0]} -qmin {VQsplit[1]} -qmax {VQsplit[2]}"
                Vformat = "-vf format=yuv420p"
            # //Audio\\ #
            if (call.settings.Ffmpeg.audioCodec == "remove"):
                AudioEverything = "-an"
            else:
                AudioEverything = f"-c:a {call.settings.Ffmpeg.audioCodec} -strict -2 -b:a {call.settings.Ffmpeg.audioBitrate}"
            # //Subtitles\\ #
            if (call.settings.Ffmpeg.videoCodec == "remove"):
                SubsC = ""
            else:
                SubsC = "-c:s copy"
            os.system(
                f"{floc}ffmpeg -hwaccel auto -i \"{url}\" -map 0:v? -map 0:a? -map 0:s? {VideoCodec} {quality} -max_muxing_queue_size 9999 -b:v 0K {Vformat} {AudioEverything} {SubsC} \"{os.path.splitext(url)[0] + append}\"")
        print("\a")
    elif (cmd == '1'):  # ====================WHOLE FOLDER==================== #
        if (call.settings.Ffmpeg.videoCodec == "remove" and call.settings.Ffmpeg.audioCodec == "remove"):
            print("I'm not gonna delete the folder for you. hmpf")
        else:
            print("write path to the folder with videos")
            url = input("#")
            # //append\\ #
            if (call.settings.Ffmpeg.videoCodec == "remove"):
                print("re-encoded file will get \".mp3\" appended, or type a different one")
                append = input("#")
                if (append == ""):
                    append = ".mp3"
            else:
                print("re-encoded file will get \"_hevcopus.mkv\" appended, 1. \"_nvenc.mov\" or type a different one")
                append = input("#")
                if (append == ""):
                    append = "_hevcopus.mkv"
                elif (append == "1"):
                    append = "_nvenc.mov"
            # //Video Quality\\ #
            if "," in call.settings.Ffmpeg.videoQuality:
                VQsplit = call.settings.Ffmpeg.videoQuality.split(",")
            else:
                VQsplit = [call.settings.Ffmpeg.videoQuality, call.settings.Ffmpeg.videoQuality,
                           call.settings.Ffmpeg.videoQuality]
            # //Video Codec\\ #
            if (call.settings.Ffmpeg.videoCodec == "libx265"):
                VideoCodec = f"-c:v {call.settings.Ffmpeg.videoCodec}"
                quality = f"-crf {int(VQsplit[0]) - 1} -qmin {int(VQsplit[1]) - 1} -qmax {int(VQsplit[2]) - 1}"
                Vformat = "-vf format=yuv420p"
            elif (call.settings.Ffmpeg.videoCodec == "copy"):
                VideoCodec = f"-c:v {call.settings.Ffmpeg.videoCodec}"
                quality = ""
                Vformat = ""
            elif (call.settings.Ffmpeg.videoCodec == "remove"):
                VideoCodec = "-vn"
                quality = ""
                Vformat = ""
            else:
                VideoCodec = f"-c:v {call.settings.Ffmpeg.videoCodec}"
                quality = f"-cq {VQsplit[0]} -qmin {VQsplit[1]} -qmax {VQsplit[2]}"
                Vformat = "-vf format=yuv420p"
            # //Audio\\ #
            if (call.settings.Ffmpeg.audioCodec == "remove"):
                AudioEverything = "-an"
            else:
                AudioEverything = f"-c:a {call.settings.Ffmpeg.audioCodec} -strict -2 -b:a {call.settings.Ffmpeg.audioBitrate}"
            # //Subtitles\\ #
            if (call.settings.Ffmpeg.videoCodec == "remove"):
                SubsC = ""
            else:
                SubsC = "-c:s copy"
            url = url.replace('[', '[[]')
            videos = glob.glob(url + os.path.sep + "*.*")
            for video in videos:
                os.system(
                    f"{floc}ffmpeg -hwaccel auto -i \"{video}\" -map 0:v? -map 0:a? -map 0:s? {VideoCodec} -max_muxing_queue_size 9999 {quality} -b:v 0K {Vformat} {AudioEverything} {SubsC} \"{video[:-4] + append}\"")
        print("\a")
    elif (cmd == '2'):
        print(
            f"VideoCodec = {call.settings.Ffmpeg.videoCodec}, <Enter> keep, 1. libx265, 2. h264_nvenc, 3. copy, 4. remove or write your own")
        cmd = input("#")
        if (cmd == ""):
            pass
        elif (cmd == "1"):
            call.settings.Ffmpeg.videoCodec = "libx265"
        elif (cmd == "2"):
            call.settings.Ffmpeg.videoCodec = "h264_nvenc"
        elif (cmd == "3"):
            call.settings.Ffmpeg.videoCodec = "copy"
        elif (cmd == "4"):
            call.settings.Ffmpeg.videoCodec = "remove"
        else:
            call.settings.Ffmpeg.videoCodec = cmd
        print(
            f"AudioCodec = {call.settings.Ffmpeg.audioCodec}, <Enter> keep, 1. Opus, 2. AAC, 3. copy, 4. remove or write your own")
        cmd = input("#")
        if (cmd == ""):
            pass
        elif (cmd == "1"):
            call.settings.Ffmpeg.audioCodec = "opus"
        elif (cmd == "2"):
            call.settings.Ffmpeg.audioCodec = "aac"
        elif (cmd == "3"):
            call.settings.Ffmpeg.audioCodec = "copy"
        elif (cmd == "4"):
            call.settings.Ffmpeg.audioCodec = "remove"
        else:
            call.settings.Ffmpeg.audioCodec = cmd
        if (call.settings.Ffmpeg.videoCodec not in ("copy", "remove")):
            print(
                f"VideoQuality = {call.settings.Ffmpeg.videoQuality}, <Enter> keep, 1. 24,24,24; or write your own q,qmin,qmax, or just q")
            cmd = input("#")
            if (cmd == ""):
                pass
            elif (cmd == "1"):
                call.settings.Ffmpeg.videoQuality = "24,24,24"
            else:
                call.settings.Ffmpeg.videoQuality = cmd
        else:
            call.settings.Ffmpeg.videoQuality = "none"
        if (call.settings.Ffmpeg.audioCodec not in ("copy", "remove")):
            print(f"AudioBitrate = {call.settings.Ffmpeg.audioBitrate}, <Enter> keep, 1. 190k, or write your own")
            cmd = input("#")
            if (cmd == ""):
                pass
            elif (cmd == "1"):
                call.settings.Ffmpeg.audioBitrate = "190k"
            else:
                call.settings.Ffmpeg.audioBitrate = cmd
        else:
            call.settings.Ffmpeg.audioBitrate = "none"
        call.settings.toJson(settingsPath)
        call.loadpath("hid")
    else:
        clear()
        call.name()
