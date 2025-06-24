import sys, platform
# Imports from this project
from shared.Video import video_list_shared, video_shared
from gui.Settings import set_save
from gui.Process import process_start, process_output_threaded
from shared.Shared import hasCookie

import os, subprocess, glob, datetime


def Video(window):
    window.settings.Ytdlp.cookie = window.vid_cookie_checkbox.isChecked()  # overwrites whatever is in the setting, but it should be se to the whatever is the setting.
    set_save(window)  # not a great idea but save the changed ehh state of the checkbox

    if window.vid_normal_radio.isChecked():
        qualityChose = ""
        qual = "best[ext=mp4]"  # these are useless
    elif window.vid_custom_radio.isChecked():
        qualityChose = "2"
        qual = window.vid_quality_bar.text()
    else:
        qualityChose = "1"
        qual = "bestvideo+bestaudio"  # these are useless

    cmd = video_shared(window.vid_url_bar.text(),
                       window.vid_playlist_checkbox.isChecked(),
                       window.vid_playlist_bar.text(),
                       qualityChose,
                       qual,
                       window.floc,
                       window.ytex,
                       window.settings.Ytdlp.videoDir,
                       window.settings.Ytdlp.cookie)

    window.process = process_start(window, cmd, window.vid_output_console, window.vid_download_button, window.process)

    thread = process_output_threaded(window, window.vid_output_console, window.vid_download_button, window.process)
    window.thread = thread

    if (platform.system().lower() == "windows" and window.settings.clipboard):  # platform windows
        if (float(f"{platform.version().split('.')[0]}.{platform.version().split('.')[1]}") >= 6.1):  # Checking if version is 6.1 (Windows 7) or higher
            if window.vid_normal_radio.isChecked() and not window.vid_playlist_checkbox.isChecked(): #only ty to put video in clipboard if it's normal quality, and not playlist
                #attempt putting the downloaded video into the clipboard
                latest_file = max(glob.glob(f"{window.settings.Ytdlp.videoDir}*"), key=os.path.getctime)
                latest_file = latest_file.replace("‘", "*")  # this character makes set-clipboard fail, and prolly is not the only one
                cmd = [f"{window.floc + os.path.sep}powershell{os.path.sep}pwsh", "-Command", f"Add-Type -AssemblyName System.Windows.Forms; $list = [System.Windows.Forms.Clipboard]::GetFileDropList(); $list.Clear(); $list.Add('{latest_file}'); [System.Windows.Forms.Clipboard]::SetFileDropList($list)"]
                Powershell_process = subprocess.run(  # codefactor is mad about this, also this is windows only and doesn't check for platform
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                # Check the exit status
                if Powershell_process.returncode != 0:
                    with open("log.txt", "a", encoding="utf8") as f:
                        f.write(f"{datetime.datetime.now()}\nvideo url: {window.vid_url_bar.text()}\n")
                        f.write(f"Command '{Powershell_process.args}' returned non-zero exit status {Powershell_process.returncode}.\n")
                        f.write(Powershell_process.stdout)
                        f.write(Powershell_process.stderr)

        if (window.settings.autoClose):
            sys.exit()  # problably not the cleanest solution but doesn't left processes behind


def vid_quality(window):
    cmd = video_list_shared(window.vid_url_bar.text(), window.ytex)

    cmd = hasCookie(window.vid_cookie_checkbox.isChecked(), cmd)

    window.process = process_start(window, cmd, window.vid_output_console, window.vid_download_button, window.process)

    thread = process_output_threaded(window, window.vid_output_console, window.vid_download_button, window.process)
    window.thread = thread


def vid_playlist_bar_toggle(window):
    window.vid_playlist_bar.setEnabled(window.vid_playlist_checkbox.isChecked())
    if (window.vid_playlist_checkbox.isChecked()):
        window.vid_playlist_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.vid_playlist_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")


def vid_quality_bar_toggle(window):
    window.vid_quality_bar.setEnabled(window.vid_custom_radio.isChecked())
    if (window.vid_custom_radio.isChecked()):
        window.vid_quality_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.vid_quality_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
