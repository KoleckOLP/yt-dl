import platform

if (platform.system().lower() == "windows"):
    if (int(platform.version().split(".")[0]) < 10):
        from PyQt5.QtWidgets import QFileDialog

try:
    from PyQt6.QtWidgets import QFileDialog
except ModuleNotFoundError:
    from PyQt5.QtWidgets import QFileDialog
# Imports from this project
from release import settingsPath
from shared.ReEncode import reencode_shared, reencode_shared_settings
from gui.Process import process_start


def reencode(window):
    location = window.ree_location_bar.text()
    videoc = window.ree_videoc_bar.text()
    videoq = window.ree_videoq_bar.text()
    audioc = window.ree_audioc_bar.text()
    audiob = window.ree_audiob_bar.text()
    append = window.ree_append_bar.text()

    result = reencode_shared(window, location, videoc, videoq, audioc, audiob, append)

    if isinstance(result, str):
        window.ree_output_console.insertPlainText(result)
    else:
        for line in result:
            window.ree_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")
            window.process = process_start(window, line, window.ree_output_console, window.ree_reencode_button, window.process)


def ree_settings(window):
    reeCodecSettings = reencode_shared_settings(window, window.ree_settings_combobox.currentIndex())

    window.ree_videoc_bar.setText(reeCodecSettings[0])
    window.ree_videoq_bar.setText(reeCodecSettings[1])
    window.ree_audioc_bar.setText(reeCodecSettings[2])
    window.ree_audiob_bar.setText(reeCodecSettings[3])
    window.ree_append_bar.setText(reeCodecSettings[4])


def ree_settings_save(window):
    if window.ree_settings_combobox.currentText() == "custom":
        window.settings.ffmpeg_settings.video_codec = window.ree_videoc_bar.text()
        window.settings.ffmpeg_settings.audio_codec = window.ree_audioc_bar.text()
        window.settings.ffmpeg_settings.video_quality = window.ree_videoq_bar.text()
        window.settings.ffmpeg_settings.audio_bitrate = window.ree_audiob_bar.text()
        window.settings.ffmpeg_settings.append = window.ree_append_bar.text()
        window.settings.defaultCodec = window.ree_settings_combobox.currentIndex()
    window.settings.to_json(settingsPath)


def ree_choose(window):
    window.ree_location_bar.setText(QFileDialog.getOpenFileName()[0])
