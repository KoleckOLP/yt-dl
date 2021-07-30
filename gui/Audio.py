# Imports from this project
from shared.Audio import audio_shared
from gui.Settings import set_save
from gui.Process import process_start, process_output


def Audio(window):
    window.settings.Youtubedl.cookie = window.aud_cookie_checkbox.isChecked()  # overwrites whatever is in the setting, but it should be se to the whatever is the setting.
    set_save(window)  # not a great idea but save the changed ehh state of the checkbox

    cmd = audio_shared(window.aud_url_bar.text(),
                       window.aud_playlist_checkbox.isChecked(),
                       window.aud_playlist_bar.text(),
                       window.floc,
                       window.settings.Youtubedl.audioDir,
                       window.settings.Youtubedl.cookie)

    window.process = process_start(window, cmd, window.aud_output_console, window.aud_download_button, window.process)

    process_output(window, window.aud_output_console, window.aud_download_button, window.process)


def aud_playlist_bar_toggle(window):
    window.aud_playlist_bar.setEnabled(window.aud_playlist_checkbox.isChecked())
    if (window.aud_playlist_checkbox.isChecked()):
        window.aud_playlist_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.aud_playlist_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
