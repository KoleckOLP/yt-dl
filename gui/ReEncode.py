import os
import glob
try:
    from PyQt6.QtWidgets import QFileDialog
except ModuleNotFoundError:
    from PyQt5.QtWidgets import QFileDialog
# Imports from this project
from release import spath, settingsPath


def Reencode(window):
    location = window.ree_location_bar.text()
    videoc = window.ree_videoc_bar.text()
    videoq = window.ree_videoq_bar.text()
    audioc = window.ree_audioc_bar.text()
    audiob = window.ree_audiob_bar.text()
    append = window.ree_append_bar.text()

    if location[-2:] == os.path.sep + "*":  # whole folder
        VidsToRender = glob.glob(location)
    else:
        VidsToRender = [f"{location}"]
    for video in VidsToRender:
        if os.path.isfile(os.path.splitext(video)[0] + append):
            window.ree_output_console.insertPlainText(f"#yt-dl# file {video} already exists skipping...\n")
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

            floc = [f"{spath + os.path.sep + 'ffmpeg'}", "-hide_banner"]
            if window.floc:
                cmd = floc + cmd
            else:
                cmd = ["ffmpeg", "-hide_banner"] + cmd

            window.process = window.process_start(cmd, window.ree_output_console, window.ree_reencode_button, window.process)

            window.process_output(window.ree_output_console, window.ree_reencode_button, window.process, "Re-encode")


def ree_settings(window):
    if window.ree_settings_combobox.currentIndex() == 5:  # custom
        window.ree_videoc_bar.setText(window.settings.Ffmpeg.videoCodec)
        window.ree_videoq_bar.setText(window.settings.Ffmpeg.videoQuality)
        window.ree_audioc_bar.setText(window.settings.Ffmpeg.audioCodec)
        window.ree_audiob_bar.setText(window.settings.Ffmpeg.audioBitrate)
        window.ree_append_bar.setText(window.settings.Ffmpeg.append)
    elif window.ree_settings_combobox.currentIndex() == 0:  # hevc_opus
        window.ree_videoc_bar.setText("libx265")
        window.ree_videoq_bar.setText("24,24,24")
        window.ree_audioc_bar.setText("opus")
        window.ree_audiob_bar.setText("190k")
        window.ree_append_bar.setText("_hevcopus.mkv")
    elif window.ree_settings_combobox.currentIndex() == 1:  # h264_nvenc
        window.ree_videoc_bar.setText("h264_nvenc")
        window.ree_videoq_bar.setText("24,24,24")
        window.ree_audioc_bar.setText("aac")
        window.ree_audiob_bar.setText("190k")
        window.ree_append_bar.setText("_nvenc.mov")
    elif window.ree_settings_combobox.currentIndex() == 2:  # hevc_nvenc
        window.ree_videoc_bar.setText("hevc_nvenc")
        window.ree_videoq_bar.setText("24,24,24")
        window.ree_audioc_bar.setText("opus")
        window.ree_audiob_bar.setText("190k")
        window.ree_append_bar.setText("_henc.mkv")
    elif window.ree_settings_combobox.currentIndex() == 3:  # mp3
        window.ree_videoc_bar.setText("remove")
        window.ree_videoq_bar.setText("none")
        window.ree_audioc_bar.setText("mp3")
        window.ree_audiob_bar.setText("190k")
        window.ree_append_bar.setText(".mp3")
    elif window.ree_settings_combobox.currentIndex() == 4:  # mjpeg_pcm
        window.ree_videoc_bar.setText("mjpeg")
        window.ree_videoq_bar.setText("2")
        window.ree_audioc_bar.setText("pcm_s16be")
        window.ree_audiob_bar.setText("190k")
        window.ree_append_bar.setText("_mjpgpcm.mov")


def ree_color(window):
    if window.ree_settings_combobox.currentText() == "mp3":
        window.ree_videoc_bar.setEnabled(False)
        window.ree_videoc_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
        window.ree_videoq_bar.setEnabled(False)
        window.ree_videoq_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.ree_videoc_bar.setEnabled(True)
        window.ree_videoc_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
        window.ree_videoq_bar.setEnabled(True)
        window.ree_videoq_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")


def ree_settings_save(window):
    window.settings.Ffmpeg.videoCodec = window.ree_videoc_bar.text()
    window.settings.Ffmpeg.audioCodec = window.ree_audioc_bar.text()
    window.settings.Ffmpeg.videoQuality = window.ree_videoq_bar.text()
    window.settings.Ffmpeg.audioBitrate = window.ree_audiob_bar.text()
    window.settings.Ffmpeg.append = window.ree_append_bar.text()
    window.settings.defaultCodec = window.ree_settings_combobox.currentIndex()
    window.settings.defaultCodec = window.ree_settings_combobox.currentIndex()
    window.settings.toJson(settingsPath)


def ree_choose(window):
    window.ree_location_bar.setText(QFileDialog.getOpenFileName()[0])
