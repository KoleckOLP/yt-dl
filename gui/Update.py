import os, platform, time

if (platform.system().lower() == "windows"):
    if (int(platform.version().split(".")[0]) < 10):
        from PyQt5 import QtWidgets, QtGui
        from PyQt5.QtCore import QT_VERSION_STR
        
try:
    from PyQt6 import QtWidgets, QtGui
    from PyQt6.QtCore import QT_VERSION_STR
except Exception as e:
    from PyQt5 import QtWidgets, QtGui
    from PyQt5.QtCore import QT_VERSION_STR
        
# Imports from this project
from release import settingsPath, ver
from gui.Process import process_start


def update(window):
    window.upd_output_console.setHtml("")
    if window.upd_update_combobox.currentIndex() == 0:
        update_yt_dl(window)
        # Wait for yt_dl update to finish before starting depend update
        while window.running:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)
        update_depend(window)
    elif window.upd_update_combobox.currentIndex() == 1:
        update_yt_dl(window)
    elif window.upd_update_combobox.currentIndex() == 2:
        update_depend(window)
    else:
        list_versions(window)

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
        cmd = [f"{window.floc+os.path.sep}git{os.path.sep}cmd{os.path.sep}git", "pull", "--recurse-submodules"]
    else:  # is not in portable
        cmd = ["git", "pull", "--recurse-submodules"]
    window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "git")


def update_depend(window):
    pips = window.settings.python_settings.pip.split(" ")
    cmd = [f"{window.settings.python_settings.python}", "-m", "pip", "install", "-U", "pip"]
    # Hold logic: collect output, print after process finishes
    result = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "python", collect_output=True)
    if result is not None:
        _, collected = result
        while window.running:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)
        for line in collected:
            line = line.rstrip("\n")
            if line:
                window.upd_output_console.insertPlainText(line + "\n")
        window.upd_output_console.insertPlainText("\n")

    if (platform.system().lower() == "windows"):  # platform windows
        if (int(platform.version().split(".")[0]) < 10):  # older than windows 10
            if (platform.release().lower() != "vista"):
                cmd = pips + ["install", "-U", "pyqt5"]  # on 7-8.1 update pyqt5 and yt-dlp
        else:
                cmd = pips + ["install", "-U", "pyqt6"]  # in 10-11 update pyqt6 and yt-dlp
        result = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip", collect_output=True)
        if result is not None:
            _, collected = result
            while window.running:
                QtWidgets.QApplication.processEvents()
                time.sleep(0.05)
            for line in collected:
                line = line.rstrip("\n")
                if line:
                    window.upd_output_console.insertPlainText(line + "\n")
            window.upd_output_console.insertPlainText("\n")
    else:  # platforms where I don't control dependecies, meaning they might not come from pip
        cmd = pips + ["install", "-U", "pyqt5"]  # try each dependenci on it's own.
        result = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip", collect_output=True)
        if result is not None:
            _, collected = result
            while window.running:
                QtWidgets.QApplication.processEvents()
                time.sleep(0.05)
            for line in collected:
                line = line.rstrip("\n")
                if line:
                    window.upd_output_console.insertPlainText(line + "\n")
            window.upd_output_console.insertPlainText("\n")

        cmd = pips + ["install", "-U", "pyqt6"]  # try each dependenci on it's own.
        result = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip", collect_output=True)
        if result is not None:
            _, collected = result
            while window.running:
                QtWidgets.QApplication.processEvents()
                time.sleep(0.05)
            for line in collected:
                line = line.rstrip("\n")
                if line:
                    window.upd_output_console.insertPlainText(line + "\n")
            window.upd_output_console.insertPlainText("\n")
        # process_output removed; output is handled by process_start

    if window.settings.ytdlp_settings.from_pip:  # no matter what platform if yt-dlp is from pip then update it
        cmd = pips + ["install", "-U", "yt-dlp"]
        window.process = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, "pip")
        # process_output removed; output is handled by process_start


def upd_auto_toggle(window):
    window.settings.auto_update = not window.settings.auto_update
    window.settings.toJson(settingsPath)
    window.upd_auto_button.setText(f"Autoupdate=\"{window.settings.auto_update}\"")


def missing_dependency(window, name, e):  # still kinda ugly function
    window.upd_output_console.append(f"{name}: {str(e)}\n")
    window.upd_update_button.setText("List")  # I have no clue if this should be Update or List xD
    window.running = False
    window.status("Ready.")
    tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
    window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
    QtWidgets.QApplication.processEvents()
    scrollbar = window.upd_output_console.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())


def list_versions(window):
    import os
    window.upd_output_console.setHtml("")
    window.upd_output_console.insertPlainText(f"yt-dl {ver}\n\n")

    def run_and_show(cmd, label=None):
        emitter, collected = process_start(window, cmd, window.upd_output_console, window.upd_update_button, window.process, False, label or cmd[0], collect_output=True)
        import time
        while window.running:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)
        # Print all lines as-is, no deduplication, just as the old logic did
        for line in collected:
            line = line.rstrip("\n")
            if line:
                window.upd_output_console.insertPlainText(line + "\n")
        window.upd_output_console.insertPlainText("\n")

    # git version
    git_portable = f"{window.floc + os.path.sep}git{os.path.sep}cmd{os.path.sep}git" if hasattr(window, 'floc') and window.floc else None
    if git_portable and os.path.isfile(git_portable):
        run_and_show([git_portable, "--version"], "git")
    else:
        run_and_show(["git", "--version"], "git")

    # python version
    python_path = window.settings.python_settings.python
    run_and_show([python_path, "-V"], "python")
    window.upd_output_console.insertPlainText(f"qt {QT_VERSION_STR}\n\n")

    # yt-dlp version
    ytex_path = window.ytex[0] if window.ytex and isinstance(window.ytex, list) else window.ytex
    if ytex_path and os.path.isfile(ytex_path):
        window.upd_output_console.insertPlainText("yt-dlp ")
        run_and_show([ytex_path, "--version"], "yt-dlp")
    else:
        window.upd_output_console.insertPlainText("yt-dlp ")
        run_and_show(["yt-dlp", "--version"], "yt-dlp")

    # ffmpeg version
    deno_path = f"{window.deno}" if hasattr(window, 'deno') and window.deno else None
    if deno_path and os.path.isfile(deno_path):
        run_and_show([deno_path, "-v"], "deno")
    else:
        run_and_show(["deno", "-v"], "deno")

    # ffmpeg version
    ffmpeg_path = f"{window.floc+os.path.sep}ffmpeg" if hasattr(window, 'floc') and window.floc else None
    #print("floc: "+window.floc)
    #print("ffmpeg_loc: " + ffmpeg_path)
    if ffmpeg_path:
        run_and_show([ffmpeg_path, "-version"], "ffmpeg")
    else:
        run_and_show(["ffmpeg", "-version"], "ffmpeg")

    try:
        window.upd_output_console.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
    except Exception as e:
        print(e)
    QtWidgets.QApplication.processEvents()
