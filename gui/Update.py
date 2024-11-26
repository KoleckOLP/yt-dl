import os, platform

if (platform.system().lower() == "windows"):
    if (int(platform.version().split(".")[0]) < 10):
        from PyQt5 import QtWidgets, QtGui
        from PyQt5.QtCore import QT_VERSION_STR
    else:
        try:
            from PyQt6 import QtWidgets, QtGui
            from PyQt6.QtCore import QT_VERSION_STR
        except Exception as e:
            from PyQt5 import QtWidgets, QtGui
            from PyQt5.QtCore import QT_VERSION_STR
# Imports from this project
from release import settingsPath, ver
from gui.Process import process_start, process_output


def Update(window):
    window.upd_output_console.setHtml("")
    if window.upd_update_combobox.currentIndex() == 0:
        update_yt_dl(window)
        update_depend(window)
    elif window.upd_update_combobox.currentIndex() == 1:
        update_yt_dl(window)
    elif window.upd_update_combobox.currentIndex() == 2:
        update_depend(window)
    else:
        listVersions(window)

def upd_button_change(window):
    if window.upd_update_combobox.currentIndex() == 0:
        window.upd_update_button.setText("Update")
    elif window.upd_update_combobox.currentIndex() == 1:
        window.upd_update_button.setText("Update")
    elif window.upd_update_combobox.currentIndex() == 2:
        window.upd_update_button.setText("Update")
    else:
        window.upd_update_button.setText("List")


def update_yt_dl(window):
    if window.gloc:  # is in portable
        cmd = [f"{window.floc+os.path.sep}git{os.path.sep}cmd{os.path.sep}git.exe", "pull", "--recurse-submodules"]
    else:  # is not in portable
        cmd = ["git", "pull", "--recurse-submodules"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "git")

    process_output(window, window.upd_output_console, window.upd_update_button, window.process, True, "Update")


def update_depend(window):
    pips = window.settings.Python.pip.split(" ")
    cmd = [f"{window.settings.Python.python}", "-m", "pip", "install", "-U", "pip"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python")
    process_output(window, window.upd_output_console, window.upd_update_button, window.process, True, "Update")

    if (platform.system().lower() == "windows"):  # platform windows
        if (int(platform.version().split(".")[0]) < 10):  # older than windows 10
            if (platform.release().lower() != "vista"):
                cmd = pips + ["install", "-U", "pyqt5"]  # on 7-8.1 update pyqt5 and yt-dlp
        else:
                cmd = pips + ["install", "-U", "pyqt6"]  # in 10-11 update pyqt6 and yt-dlp
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, True, "Update")
    else:  # platforms where I don't control dependecies, meaning they might not come from pip
        cmd = pips + ["install", "-U", "pyqt5"]  # try each dependenci on it's own.
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, True, "Update")

        cmd = pips + ["install", "-U", "pyqt6"]  # try each dependenci on it's own.
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, True, "Update")

    if window.settings.Youtubedl.fromPip:  # no matter what plaform if yt-dlp is from pip than update it
        cmd = pips + ["install", "-U", "yt-dlp"]
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, True, "Update")


def upd_auto_toggle(window):
    window.settings.autoUpdate = not window.settings.autoUpdate
    window.settings.toJson(settingsPath)
    window.upd_auto_button.setText(f"Autoupdate=\"{window.settings.autoUpdate}\"")


def missingDependency(window, name, e):  # still kinda ugly function
    window.upd_output_console.append(f"{name}: {str(e)}\n")
    window.upd_update_button.setText("List")  # I have no clue if this should be Update or List xD
    window.running = False
    window.status("Ready.")
    tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
    window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
    QtWidgets.QApplication.processEvents()
    scrollbar = window.upd_output_console.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())


def listVersions(window):
    # yt-dl version
    window.upd_output_console.append(f"yt-dl {ver}\n")

    if window.gloc:
        cmd = [f"{window.floc + os.path.sep}git{os.path.sep}cmd{os.path.sep}git.exe", "-v"]
    else:
        cmd = ["git.exe", "--version"]
    try:
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "git")
        window.upd_output_console.append("")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, False, "List")  # should be List soon.
    except Exception as e:
        missingDependency(window, "git", e)

    # python version
    cmd = [window.settings.Python.python, "-V"]
    try:
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python")
        window.upd_output_console.append("")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, False, "List")  # should be List soon.
    except Exception as e:
        missingDependency(window, "python", e)


    # qt version
    window.upd_output_console.append(f"qt {QT_VERSION_STR}\n")

    # yt-dlp version
    if window.ytex:
        cmd = window.ytex + ["--version"]  # yt-dlp is in a known location (portable)
    else:
        cmd = ["yt-dlp", "--version"]  # yt-dlp should be in users path, and it's not my problem (non portable)
    try:
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False)

        window.upd_output_console.append("yt-dlp ")

        process_output(window, window.upd_output_console, window.upd_update_button, window.process, False, "List")  # should be List soon.
    except Exception as e:
        missingDependency(window, "yt-dlp", e)

    # ffmpeg version
    if window.floc:
        cmd = [f"{window.floc+os.path.sep}ffmpeg", "-version"]
    else:
        cmd = ["ffmpeg", "-version"]
    try:
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "ffmpeg")
        window.upd_output_console.append("")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, False, "List")  # should be List soon.
    except Exception as e:
        missingDependency(window, "ffmpeg", e)

    try:
        window.upd_output_console.moveCursor(QtGui.QTextCursor.MoveOperation.Start)  # this line crashes on Vista but doesn't seem to be needed :D
    except Exception as e:
        print(e)
    QtWidgets.QApplication.processEvents()
