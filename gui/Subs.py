import os
# Imports from this project
from shared.Subs import subs_shared_list, subs_shared_download, subs_shared_paths_for_ffmpeg, subs_shared_lines_for_ffmpeg


def Subs(window):
    result = subs_shared_download(window.sub_url_bar.text(),
                                  window.sub_playlist_checkbox.isChecked(),
                                  window.sub_playlist_bar.text(),
                                  window.sub_lang_bar.text(),
                                  window.floc)

    cmd, temp = result

    cmd = window.hasCookie(window.sub_cookie_checkbox.isChecked(), cmd)

    window.process = window.process_start(cmd, window.sub_output_console, window.sub_download_button, window.process)

    window.process_output(window.sub_output_console, window.sub_download_button, window.process)

    subpath, newsubpath = subs_shared_paths_for_ffmpeg(temp.name + os.path.sep, window.settings.Youtubedl.videoDir)

    FfmpegLines = subs_shared_lines_for_ffmpeg(window, subpath, newsubpath)

    if isinstance(FfmpegLines, str):
        if FfmpegLines == "error":
            window.sub_output_console.insertPlainText(f"#yt-dl# found an issue aborting...\n")
        else:
            window.sub_output_console.insertPlainText(f"#yt-dl# file {FfmpegLines} already exists aborting...\n")

    else:
        for line in FfmpegLines:
            window.sub_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")

            window.process = window.process_start(line, window.sub_output_console, window.sub_download_button, window.process)

            window.process_output(window.sub_output_console, window.sub_download_button, window.process)

    temp.cleanup()


def sub_lang(window):
    cmd = subs_shared_list(window.sub_url_bar.text())  # seems kinda unnecessary

    window.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

    window.process = window.process_start(cmd, window.sub_output_console, window.sub_download_button, window.process)

    window.process_output(window.sub_output_console, window.sub_download_button, window.process)


def sub_playlist_bar_toggle(window):
    window.sub_lang_button.setEnabled(not window.sub_playlist_checkbox.isChecked())
    window.sub_playlist_bar.setEnabled(window.sub_playlist_checkbox.isChecked())
    if (window.sub_playlist_checkbox.isChecked()):
        window.sub_playlist_bar.setStyleSheet("background-color: #909090;")
    else:
        window.sub_playlist_bar.setStyleSheet("background-color: #707070;")
