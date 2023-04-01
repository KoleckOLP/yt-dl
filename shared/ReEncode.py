import os
import glob


def reencode_shared(call_window, location, videoc, videoq, audioc, audiob, append):
    FfmpegLines = []

    if location[-2:] == os.path.sep + "*":  # whole folder
        VidsToRender = glob.glob(location)
    else:
        VidsToRender = [f"{location}"]
    for video in VidsToRender:
        if not os.path.isfile(os.path.splitext(video)[0] + append):
            cmd = [["-hwaccel", "auto", "-i", f"{video}", "-map", "0:v?", "-map", "0:a?", "-map", "0:s?"],
                   ["-max_muxing_queue_size", "9999", "-b:v", "0K"], [f"{os.path.splitext(video)[0] + append}"]]

            # //Video Quality\\#
            if "," in videoq:
                VQsplit = videoq.split(",")
            else:
                VQsplit = [videoq, videoq, videoq]
            # //Video Codec\\#
            if (videoc == "copy"):
                VideoCodec = [f"-c:v", f"{videoc}"]
                cmd = [cmd[0] + VideoCodec + cmd[1], cmd[2]]
            elif (videoc == "remove"):
                VideoCodec = ["-vn"]
                cmd = [cmd[0] + VideoCodec + cmd[1], cmd[2]]

            elif (videoc == "cover"):
                cmd = [cmd[0] + cmd[1], cmd[2]]
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
            else:  # (videoc == "libx265" or videoc == "libx264" or videoc == "libvpx-vp9"):
                VideoCodec = ["-c:v", f"{videoc}"]
                quality = ["-crf", f"{int(VQsplit[0]) - 1}", "-qmin", f"{int(VQsplit[1]) - 1}", "-qmax",
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

            if call_window.floc:
                floc = [f"{call_window.floc + os.path.sep + 'ffmpeg'}", "-hide_banner"]
                cmd = floc + cmd
            else:
                cmd = ["ffmpeg", "-hide_banner"] + cmd

            FfmpegLines = FfmpegLines + [cmd]
        else:
            return f"#yt-dl# file {video} already exists skipping...\n"  # remember to check for this
    return FfmpegLines


def reencode_shared_settings(call_window, setting=0):  # still could be done better, shouldn't be a function at all
    reencode_options = [["libx264",
                         "22,22,22",
                         "opus",
                         "190k",
                         "_libx264.mkv",
                         "x264_opus (avc)"],
                        ["libx265",
                         "22,22,22",
                         "opus",
                         "190k",
                         "_hevcopus.mkv",
                         "x265_opus (hevc)"],
                        ["h264_nvenc",
                         "22,22,22",
                         "aac",
                         "190k",
                         "_nvenc.mov",
                         "h264_nvenc_aac (avc)"],
                        ["hevc_nvenc",
                         "22,22,22",
                         "opus",
                         "190k",
                         "_henc.mkv",
                         "h265_nvenc_opus (hevc)"],
                        ["mjpeg",
                         "2",
                         "pcm_s16be",
                         "190k",
                         "_mjpgpcm.mov",
                         "mjpeg_pcm"],
                        ["libvpx-vp9",
                         "22,22,22",
                         "opus",
                         "190k",
                         "_vopus9.mp4",
                         "vp9_opus"],
                        ["remove",
                         "none",
                         "libmp3lame",
                         "190k",
                         ".mp3",
                         "mp3"],
                        [call_window.settings.Ffmpeg.videoCodec,
                         call_window.settings.Ffmpeg.videoQuality,
                         call_window.settings.Ffmpeg.audioCodec,
                         call_window.settings.Ffmpeg.audioBitrate,
                         call_window.settings.Ffmpeg.append,
                         "custom"]]

    if setting == "len":
        return len(reencode_options)
    return (reencode_options[setting])
