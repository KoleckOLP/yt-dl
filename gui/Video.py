from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from shared.Video import video_shared


def Video(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.tabWidget.setTabText(1, "*Video")

        window.vid_output_console.setHtml("")  # clearing the output_console.

        if window.vid_normal_radio.isChecked():
            qualityChose = "1"
            qual = "best"  # these are useless
        elif window.vid_custom_radio.isChecked():
            qualityChose = "2"
            qual = window.vid_quality_bar.text()
        else:
            qualityChose = ""
            qual = "bestvideo+bestaudio"  # these are useless

        cmd = video_shared(window.vid_url_bar.text(),
                           window.vid_playlist_checkbox.isChecked(),
                           window.vid_playlist_bar.text(),
                           qualityChose,
                           qual,
                           window.floc,
                           window.settings.Youtubedl.videoDir)

        cmd = window.hasCookie(window.vid_cookie_checkbox.isChecked(), cmd)

        window.aud_output_console.insertPlainText("#yt-dl# starting youtube-dl please wait...\n")

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
