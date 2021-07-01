try:
    from PyQt6.QtWidgets import QFileDialog
except ModuleNotFoundError:
    from PyQt5.QtWidgets import QFileDialog
# Imports from this project
from release import settingsPath
from shared.ReEncode import reencode_shared, reencode_shared_settings
from gui.Process import process_start, process_output


def Reencode(window):
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
            window.sub_output_console.insertPlainText("#yt-dl# starting ffmpeg please wait...\n")

            window.process = process_start(window, line, window.ree_output_console, window.sub_download_button, window.process)

            process_output(window, window.ree_output_console, window.sub_download_button, window.process)


def ree_settings(window):
    reeCodecSettings = reencode_shared_settings(window, window.ree_settings_combobox.currentIndex())

    window.ree_videoc_bar.setText(reeCodecSettings[0])
    window.ree_videoq_bar.setText(reeCodecSettings[1])
    window.ree_audioc_bar.setText(reeCodecSettings[2])
    window.ree_audiob_bar.setText(reeCodecSettings[3])
    window.ree_append_bar.setText(reeCodecSettings[4])


def ree_color(window):
    if window.ree_settings_combobox.currentText() == "mp3":
        window.ree_videoc_bar.setEnabled(False)
        window.ree_videoc_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
        window.ree_videoq_bar.setEnabled(False)
        window.ree_videoq_bar.setStyleSheet(f"background-color: {window.disabledColor}; Border: None; Color: #FFFFFF;")
    else:
        window.ree_videoc_bar.setEnabled(True)
        window.ree_videoc_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")
        window.ree_videoq_bar.setEnabled(True)
        window.ree_videoq_bar.setStyleSheet(f"background-color: {window.enabledColor}; Border: None; Color: #FFFFFF;")


def ree_settings_save(window):
    window.settings.Ffmpeg.videoCodec = window.ree_videoc_bar.text()
    window.settings.Ffmpeg.audioCodec = window.ree_audioc_bar.text()
    window.settings.Ffmpeg.videoQuality = window.ree_videoq_bar.text()
    window.settings.Ffmpeg.audioBitrate = window.ree_audiob_bar.text()
    window.settings.Ffmpeg.append = window.ree_append_bar.text()
    window.settings.defaultCodec = window.ree_settings_combobox.currentIndex()
    window.settings.toJson(settingsPath)


def ree_choose(window):
    window.ree_location_bar.setText(QFileDialog.getOpenFileName()[0])
