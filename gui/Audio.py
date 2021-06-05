from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from release import spath
from shared.Audio import audio_shared


def Audio(window):
    if not window.running:
        window.running = True
        window.status("Busy.")
        window.tabWidget.setTabText(0, "*Audio")

        window.aud_output_console.setHtml("")  # clearing the output_console

        if window.fdir:
            floc = spath
        else:
            floc = False

        cmd = audio_shared(window.aud_url_bar.text(), window.aud_playlist_checkbox.isChecked(), window.aud_playlist_bar.text(), floc, window.settings.Youtubedl.audioDir)

        window.hasCookie(window.aud_cookie_checkbox.isChecked(), cmd)

        window.aud_output_console.insertPlainText("#yt-dl# starting youtube-dl please wait...\n")

        window.process_start(cmd, window.aud_output_console)

        window.running = False
        window.status("Ready.")
        window.tabWidget.setTabText(0, "Audio")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def aud_playlist_bar_toggle(window):
    window.aud_playlist_bar.setEnabled(window.aud_playlist_checkbox.isChecked())
    if (window.aud_playlist_checkbox.isChecked()):
        window.aud_playlist_bar.setStyleSheet("background-color: #909090;")
    else:
        window.aud_playlist_bar.setStyleSheet("background-color: #707070;")
