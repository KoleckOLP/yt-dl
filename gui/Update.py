# Imports from this project
from release import settingsPath


def Update(window):
    if window.upd_update_combobox.currentIndex() == 1:
        update_yt_dl(window)
    elif window.upd_update_combobox.currentIndex() == 2:
        update_depend(window)
    else:
        update_yt_dl(window)
        update_depend(window)


def update_yt_dl(window):
    cmd = ["git", "pull", "--recurse-submodules"]
    window.process = window.process_start(cmd, window.upd_output_console, window.upd_update_button, window.process, False, "git")

    window.process_output(window.upd_output_console, window.upd_update_button, window.process)


def update_depend(window):
    cmd = [window.settings.Python.python, "-V"]
    window.process = window.process_start(cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python")

    window.process_output(window.upd_output_console, window.upd_update_button, window.process)
    pips = window.settings.Python.pip.split(" ")
    cmd = [f"{window.settings.Python.python}", "-m", "pip", "install", "-U", "pip"]
    window.process = window.process_start(cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python")

    window.process_output(window.upd_output_console, window.upd_update_button, window.process)
    cmd = pips + ["install", "-U", "-r", "req-gui5.txt"]
    window.process = window.process_start(cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")

    window.process_output(window.upd_output_console, window.upd_update_button, window.process)


def upd_auto_toggle(window):
    window.settings.autoUpdate = not window.settings.autoUpdate
    window.settings.toJson(settingsPath)
    window.upd_auto_button.setText(f"Autoupdate=\"{window.settings.autoUpdate}\"")
