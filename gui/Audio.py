# Imports from this project
from shared.Audio import audio_shared


def Audio(window):
    cmd = audio_shared(window.aud_url_bar.text(),
                       window.aud_playlist_checkbox.isChecked(),
                       window.aud_playlist_bar.text(),
                       window.floc,
                       window.settings.Youtubedl.audioDir)

    cmd = window.hasCookie(window.aud_cookie_checkbox.isChecked(), cmd)

    window.process = window.process_start(cmd, window.aud_output_console, window.aud_download_button, window.process)

    window.process_output(window.aud_output_console, window.aud_download_button, window.process)


def aud_playlist_bar_toggle(window):
    window.aud_playlist_bar.setEnabled(window.aud_playlist_checkbox.isChecked())
    if (window.aud_playlist_checkbox.isChecked()):
        window.aud_playlist_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.aud_playlist_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
