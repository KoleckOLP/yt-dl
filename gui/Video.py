from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from shared.Video import video_list_shared, video_shared


def Video(window):
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

    window.process = window.process_start(cmd, window.vid_output_console,  window.vid_download_button, window.process)

    window.process_output(window.vid_output_console, window.vid_download_button, window.process)


def vid_quality(window):
    cmd = video_list_shared(window.vid_url_bar.text())

    window.hasCookie(window.vid_cookie_checkbox.isChecked(), cmd)

    window.process = window.process_start(cmd, window.vid_output_console, window.vid_download_button, window.process)

    window.process_output(window.vid_output_console, window.vid_download_button, window.process)


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
