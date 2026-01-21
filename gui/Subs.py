import os, sys
# Imports from this project
from shared.Subs import subs_shared_list, subs_shared_download, subs_shared_paths_for_ffmpeg, subs_shared_lines_for_ffmpeg
from gui.Process import process_start
from gui.Settings import set_save


def subs(window):
    window.settings.ytdlp_settings.cookie = window.sub_cookie_checkbox.isChecked()  # overwrites whatever is in the setting, but it should be set to whatever is the setting.
    set_save(window)  # not a great idea but save the changed ehh state of the checkbox

    # Download subtitles directly to the video_dir and convert to srt in one step
    from shared.Shared import shared, has_cookie
    cmd = shared(
        window.sub_playlist_checkbox.isChecked(),
        window.sub_playlist_bar.text(),
        window.floc,
        window.ytex,
        window.settings.ytdlp_settings.video_dir,
    )
    cmd += ["--write-sub", "--write-auto-sub", "--sub-format", "vtt", "--convert-subs", "srt", "--skip-download", window.sub_url_bar.text()]
    if window.sub_lang_bar.text():
        if window.sub_lang_bar.text() == "all":
            cmd += ["--all-subs"]
        else:
            cmd += ["--sub-lang", window.sub_lang_bar.text()]
    cmd = has_cookie(window.sub_cookie_checkbox.isChecked(), cmd)
    window.process = process_start(window, cmd, window.sub_output_console, window.sub_download_button, window.process)
    if (window.settings.auto_close):
        sys.exit()  # probably not the cleanest solution but doesn't leave processes behind


def sub_lang(window):
    cmd = subs_shared_list(window.sub_url_bar.text(), window.ytex)  # seems kinda unnecessary

    window.sub_output_console.insertPlainText("#yt-dl# starting yt-dl please wait...\n")

    window.process = process_start(window, cmd, window.sub_output_console, window.sub_download_button, window.process)


def sub_playlist_bar_toggle(window):
    window.sub_lang_button.setEnabled(not window.sub_playlist_checkbox.isChecked())
    window.sub_playlist_bar.setEnabled(window.sub_playlist_checkbox.isChecked())
    if (window.sub_playlist_checkbox.isChecked()):
        window.sub_playlist_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.sub_playlist_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
