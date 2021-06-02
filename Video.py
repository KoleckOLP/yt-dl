from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from release import spath


def Video(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.tabWidget.setTabText(1, "*Video")

        window.vid_output_console.setHtml("")  # clearing the output_console.

        url = window.vid_url_bar.text()
        if window.vid_playlist_checkbox.isChecked():
            numb = window.vid_playlist_bar.text()
        else:
            numb = None

        if (numb is None):
            cmd = [["youtube-dl", "-o", f"{window.settings.Youtubedl.videoDir}%(title)s.%(ext)s", "-f"],
                   ["--no-playlist", f"{url}"]]
        elif (numb == ""):
            cmd = [
                ["youtube-dl", "-o", f"{window.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s", "-f"],
                ["--yes-playlist", f"{url}"]]
        else:
            cmd = [
                ["youtube-dl", "-o", f"{window.settings.Youtubedl.videoDir}%(playlist_index)s. %(title)s.%(ext)s", "-f"],
                ["--yes-playlist", "--playlist-items", f"{numb}", f"{url}"]]

        if window.vid_best_radio.isChecked():
            qual = ["bestvideo+bestaudio"]
        elif window.vid_custom_radio.isChecked():
            qual = [window.vid_quality_bar.text()]
        else:
            qual = ["best"]

        floc = [f"--ffmpeg-location", f"{spath}"]
        if window.fdir:
            cmd = cmd[0] + qual + floc + cmd[1]
        else:
            cmd = cmd[0] + qual + cmd[1]

        window.hasCookie(window.vid_cookie_checkbox.isChecked(), cmd)

        window.process_start(cmd, window.vid_output_console)

        window.running = False
        window.status("Ready.")
        window.tabWidget.setTabText(1, "Video")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def vid_quality(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.vid_output_console.setHtml("")  # clearing the output_console

        url = window.vid_url_bar.text()
        cmd = ["youtube-dl", "-F", "--no-playlist", f"{url}"]

        window.hasCookie(window.vid_cookie_checkbox.isChecked(), cmd)

        window.vid_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

        window.process_start(cmd, window.vid_output_console)

        window.running = False
        window.status("Ready.")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def vid_playlist_bar_toggle(window):
    window.vid_playlist_bar.setEnabled(window.vid_playlist_checkbox.isChecked())
    if (window.vid_playlist_checkbox.isChecked()):
        window.vid_playlist_bar.setStyleSheet("background-color: #909090;")
    else:
        window.vid_playlist_bar.setStyleSheet("background-color: #707070;")


def vid_quality_bar_toggle(window):
    window.vid_quality_bar.setEnabled(window.vid_custom_radio.isChecked())
    if (window.vid_custom_radio.isChecked()):
        window.vid_quality_bar.setStyleSheet("background-color: #909090;")
    else:
        window.vid_quality_bar.setStyleSheet("background-color: #707070;")
