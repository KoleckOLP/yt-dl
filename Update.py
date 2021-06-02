from PyQt5.QtWidgets import QMessageBox
# Imports from this project
from release import settingsPath


def Update(window):
    if not window.running:
        window.running = True
        window.status("Busy.")

        window.tabWidget.setTabText(4, "*Update")

        window.upd_output_console.setHtml("")  # clearing the output_console

        if window.upd_update_combobox.currentIndex() == 1:
            update_yt_dl(window)
        elif window.upd_update_combobox.currentIndex() == 2:
            update_depend(window)
        else:
            update_yt_dl(window)
            update_depend(window)

        window.running = False
        window.status("Ready.")
        window.tabWidget.setTabText(4, "Update")
    else:
        window.messagePopup("Process warning", QMessageBox.Warning, "One process already running!")


def update_yt_dl(window):
    cmd = ["git", "pull", "--recurse-submodules"]
    window.process_start(cmd, window.upd_output_console)


def update_depend(window):
    cmd = [window.settings.Python.python, "-V"]
    window.process_start(cmd, window.upd_output_console)
    pips = window.settings.Python.pip.split(" ")
    cmd = [f"{window.settings.Python.python}", "-m", "pip", "install", "-U", "pip"]
    window.process_start(cmd, window.upd_output_console)
    cmd = pips + ["install", "-U", "-r", "req-gui5.txt"]
    window.process_start(cmd, window.upd_output_console)


def upd_auto_toggle(window):
    window.settings.autoUpdate = not window.settings.autoUpdate
    window.settings.toJson(settingsPath)
    window.upd_auto_button.setText(f"Autoupdate=\"{window.settings.autoUpdate}\"")
