from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from release import spath


def Audio(window):
    if not window.running:
        window.running = True
        window.status("Busy.")
        window.tabWidget.setTabText(0, "*Audio")

        window.aud_output_console.setHtml("")  # clearing the output_console

        url = window.aud_url_bar.text()
        if window.aud_playlist_checkbox.isChecked():
            numb = window.aud_playlist_bar.text()
        else:
            numb = None

        if (numb is None):
            cmd = [["youtube-dl", "-o", f"{window.settings.Youtubedl.audioDir}%(title)s.%(ext)s", "--no-playlist", "-x",
                    "--prefer-ffmpeg"], ["--audio-format", "mp3", f"{url}"]]
        elif (numb == ""):
            cmd = [["youtube-dl", "-o", f"{window.settings.Youtubedl.audioDir}%(playlist_index)s. %(title)s.%(ext)s",
                    "--yes-playlist", "-i", "-x", "--prefer-ffmpeg"], ["--audio-format", "mp3", f"{url}"]]
        else:
            cmd = [["youtube-dl", "-o", f"{window.settings.Youtubedl.audioDir}%(playlist_index)s. %(title)s.%(ext)s",
                    "--yes-playlist", "-i", "--playlist-items", f"{numb}", "-x", "--prefer-ffmpeg"],
                   ["--audio-format", "mp3", f"{url}"]]

        floc = [f"--ffmpeg-location", f"{spath}"]
        if window.fdir:
            cmd = cmd[0] + floc + cmd[1]
        else:
            cmd = cmd[0] + cmd[1]

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
