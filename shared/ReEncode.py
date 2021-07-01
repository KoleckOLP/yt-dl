import os
import glob
# Imports from this project
from release import spath


def reencode_shared(call_window, location, videoc, videoq, audioc, audiob, append):
    FfmpegLines = []

    if location[-2:] == os.path.sep + "*":  # whole folder
        VidsToRender = glob.glob(location)
    else:
        VidsToRender = [f"{location}"]
    for video in VidsToRender:
        if os.path.isfile(os.path.splitext(video)[0] + append):
            return f"#yt-dl# file {video} already exists skipping...\n"  # remember to check for this
        else:
            cmd = [["-hwaccel", "auto", "-i", f"{video}", "-map", "0:v?", "-map", "0:a?", "-map", "0:s?"],
                   ["-max_muxing_queue_size", "9999", "-b:v", "0K"], [f"{os.path.splitext(video)[0] + append}"]]

            # //Video Quality\\#
            if "," in videoq:
                VQsplit = videoq.split(",")
            else:
                VQsplit = [videoq, videoq, videoq]
            # //Video Codec\\#
            if (videoc == "libx265"):
                VideoCodec = ["-c:v", f"{videoc}"]
                quality = ["-crf", f"{int(VQsplit[0]) - 1}", "-qmin", f"{int(VQsplit[1]) - 1}", "-qmax",
                           f"{int(VQsplit[2]) - 1}"]
                Vformat = ["-vf", "format=yuv420p"]
                cmd = [cmd[0] + VideoCodec + quality + cmd[1] + Vformat, cmd[2]]
            elif (videoc == "copy"):
                VideoCodec = [f"-c:v", f"{videoc}"]
                cmd = [cmd[0] + VideoCodec + cmd[1], cmd[2]]
            elif (videoc == "remove"):
                VideoCodec = ["-vn"]
                cmd = [cmd[0] + VideoCodec + cmd[1], cmd[2]]
            elif (videoc == "hevc_nvenc"):
                VideoCodec = ["-c:v", f"{videoc}"]
                quality = ["-rc:v", "vbr", "-qmin", f"{int(VQsplit[1])}", "-qmax", f"{int(VQsplit[2])}", "-bf", "1"]
                Vformat = ["-vf", "format=yuv420p"]
                cmd = [cmd[0] + VideoCodec + quality + cmd[1] + Vformat, cmd[2]]
            elif (videoc == "h264_nvenc"):
                VideoCodec = ["-c:v", f"{videoc}"]
                quality = ["-rc:v", "vbr", "-qmin", f"{int(VQsplit[1])}", "-qmax", f"{int(VQsplit[2])}"]
                Vformat = ["-vf", "format=yuv420p"]
                cmd = [cmd[0] + VideoCodec + quality + cmd[1] + Vformat, cmd[2]]
            elif (videoc == "mjpeg"):
                VideoCodec = ["-c:v", f"{videoc}"]
                quality = ["-q:v", videoq]
                Vformat = ["-vf", "format=yuv420p"]
                cmd = [cmd[0] + VideoCodec + quality + cmd[1] + Vformat, cmd[2]]
            else:
                VideoCodec = ["-c:v", f"{videoc}"]
                quality = ["-cq", f"{int(VQsplit[0]) - 1}", "-qmin", f"{int(VQsplit[1]) - 1}", "-qmax",
                           f"{int(VQsplit[2]) - 1}"]
                Vformat = ["-vf", "format=yuv420p"]
                cmd = [cmd[0] + VideoCodec + quality + cmd[1] + Vformat, cmd[2]]
            # //Audio\\#
            if (audioc == "remove"):
                AudioEverything = ["-an"]
                cmd = [cmd[0] + AudioEverything, cmd[1]]
            else:
                AudioEverything = ["-c:a", f"{audioc}", "-strict", "-2", "-b:a", f"{audiob}"]
                cmd = [cmd[0] + AudioEverything, cmd[1]]
            # //Subtitles\\#
            if (videoc == "remove"):
                cmd = cmd[0] + cmd[1]
            else:
                SubsC = ["-c:s", "copy"]
                cmd = cmd[0] + SubsC + cmd[1]

            floc = [f"{spath + 'ffmpeg'}", "-hide_banner"]
            if call_window.floc:
                cmd = floc + cmd
            else:
                cmd = ["ffmpeg", "-hide_banner"] + cmd

        FfmpegLines = FfmpegLines + [cmd]

    return FfmpegLines


def reencode_shared_settings(call_window, setting: int):
    if setting == 5:  # custom
        return(call_window.settings.Ffmpeg.videoCodec,
               call_window.settings.Ffmpeg.videoQuality,
               call_window.settings.Ffmpeg.audioCodec,
               call_window.settings.Ffmpeg.audioBitrate,
               call_window.settings.Ffmpeg.append,
               "custom/current")
    elif setting == 0:  # hevc_opus
        return("libx265",
               "24,24,24",
               "opus",
               "190k",
               "_hevcopus.mkv",
               "hevc_opus")
    elif setting == 1:  # h264_nvenc
        return("h264_nvenc",
               "24,24,24",
               "aac",
               "190k",
               "_nvenc.mov",
               "h264_nvenc")
    elif setting == 2:  # hevc_nvenc
        return("hevc_nvenc",
               "24,24,24",
               "opus",
               "190k",
               "_henc.mkv",
               "hevc_nvenc")
    elif setting == 3:  # mp3
        return("remove",
               "none",
               "mp3",
               "190k",
               ".mp3",
               "mp3")
    elif setting == 4:  # mjpeg_pcm
        return("mjpeg",
               "2",
               "pcm_s16be",
               "190k",
               "_mjpgpcm.mov",
               "mjpeg_pcm")
