import os
from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from shared.Subs import subs_list_shared, subs_shared_part1, subs_shared_part2, subs_shared_part3


def Subs(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.tabWidget.setTabText(2, "*Subs")

        window.sub_output_console.setHtml("")  # clearing the output_console.

        result = subs_shared_part1(window.sub_url_bar.text(),
                                   window.sub_playlist_checkbox.isChecked(),
                                   window.sub_playlist_bar.text(),
                                   window.sub_lang_bar.text(),
                                   window.floc)

        cmd, temp = result

        cmd = window.hasCookie(window.sub_cookie_checkbox.isChecked(), cmd)

        window.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

        window.process_start(cmd, window.sub_output_console)

        subpath, newsubpath = subs_shared_part2(temp.name+os.path.sep, window.settings.Youtubedl.videoDir)

        FfmpegLines = subs_shared_part3(window, subpath, newsubpath)

        if isinstance(FfmpegLines, str):
            if FfmpegLines == "error":
                window.sub_output_console.insertPlainText(f"#yt-dl# found an issue aborting...\n")
            else:
                window.sub_output_console.insertPlainText(f"#yt-dl# file {FfmpegLines} already exists aborting...\n")

        else:
            for line in FfmpegLines:
                window.sub_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")

                window.process_start(line, window.sub_output_console)

        temp.cleanup()

        window.running = False
        window.status("Ready.")
        window.tabWidget.setTabText(2, "Subs")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def sub_lang(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.sub_output_console.setHtml("")  # clearing the output_console

        cmd = subs_list_shared(window.sub_url_bar.text())  # seems kinda unnecessary

        window.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

        window.process_start(cmd, window.sub_output_console)

        window.running = False
        window.status("Ready.")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def sub_playlist_bar_toggle(window):
    window.sub_lang_button.setEnabled(not window.sub_playlist_checkbox.isChecked())
    window.sub_playlist_bar.setEnabled(window.sub_playlist_checkbox.isChecked())
    if (window.sub_playlist_checkbox.isChecked()):
        window.sub_playlist_bar.setStyleSheet("background-color: #909090;")
    else:
        window.sub_playlist_bar.setStyleSheet("background-color: #707070;")


def sub_lang_bar_toggle(window):
    window.sub_lang_bar.setEnabled(window.sub_lang_checkbox.isChecked())
    if (window.sub_lang_checkbox.isChecked()):
        window.sub_lang_bar.setStyleSheet("background-color: #909090;")
    else:
        window.sub_lang_bar.setStyleSheet("background-color: #707070;")
