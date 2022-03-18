# Imports from this project
from shared.Video import video_list_shared, video_shared
from gui.Settings import set_save
# from gui.Process import process_start, process_output
from shared.Shared import hasCookie


def Video(window):
    window.settings.Youtubedl.cookie = window.vid_cookie_checkbox.isChecked()  # overwrites whatever is in the setting, but it should be se to the whatever is the setting.
    set_save(window)  # not a great idea but save the changed ehh state of the checkbox

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
                       window.ytex,
                       window.settings.Youtubedl.videoDir,
                       window.settings.Youtubedl.cookie)

    # window.process = process_start(window, cmd, window.vid_output_console,  window.vid_download_button, window.process)

    # process_output(window, window.vid_output_console, window.vid_download_button, window.process)


def vid_quality(window):
    cmd = video_list_shared(window.vid_url_bar.text(), window.ytex)

    hasCookie(window.vid_cookie_checkbox.isChecked(), cmd)

    window.process = process_start(window, cmd, window.vid_output_console, window.vid_download_button, window.process)

    process_output(window, window.vid_output_console, window.vid_download_button, window.process)


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
