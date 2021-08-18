try:
    from PyQt6 import QtWidgets, QtGui
    from PyQt6.QtCore import QT_VERSION_STR
except ModuleNotFoundError:
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


def update_yt_dl(window):
    cmd = ["git", "pull", "--recurse-submodules"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "git")

    process_output(window, window.upd_output_console, window.upd_update_button, window.process)


def update_depend(window):
    pips = window.settings.Python.pip.split(" ")
    cmd = [f"{window.settings.Python.python}", "-m", "pip", "install", "-U", "pip"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python")
    process_output(window, window.upd_output_console, window.upd_update_button, window.process)

    cmd = pips + ["install", "-U", "-r", f"req-gui.txt"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")
    process_output(window, window.upd_output_console, window.upd_update_button, window.process)


def upd_auto_toggle(window):
    window.settings.autoUpdate = not window.settings.autoUpdate
    window.settings.toJson(settingsPath)
    window.upd_auto_button.setText(f"Autoupdate=\"{window.settings.autoUpdate}\"")


def listVersions(window):
    window.upd_output_console.append(f"yt-dl {ver}\n\n")

    cmd = [window.settings.Python.python, "-V"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python")
    process_output(window, window.upd_output_console, window.upd_update_button, window.process, False)

    window.upd_output_console.append(f"qt {QT_VERSION_STR}\n")  # youtube-dl

    cmd = ["youtube-dl", "--version"]
    try:
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False)

        window.upd_output_console.append("youtube-dl ")

        process_output(window, window.upd_output_console, window.upd_update_button, window.process, False)
    except Exception as e:
        window.upd_output_console.append(f"youtube-dl: {str(e)}")
        # TODO this should be a function and kinda is a really bad implementation anyway (duplicate code)
        window.upd_update_button.setText("Update")
        window.running = False
        window.status("Ready.")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
        QtWidgets.QApplication.processEvents()
        scrollbar = window.upd_output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    window.upd_output_console.append("")

    cmd = ["ffmpeg", "-version"]
    try:
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "ffmpeg")
        process_output(window, window.upd_output_console, window.upd_update_button, window.process, False)
    except Exception as e:
        window.upd_output_console.append(f"ffmpeg: {str(e)}")
        window.upd_update_button.setText("Update")
        window.running = False
        window.status("Ready.")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
        QtWidgets.QApplication.processEvents()
        scrollbar = window.upd_output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    window.upd_output_console.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
    QtWidgets.QApplication.processEvents()
