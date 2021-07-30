import sys
import subprocess
from typing import List
try:
    from PyQt6 import QtWidgets, QtGui
except ModuleNotFoundError:
    from PyQt5 import QtWidgets, QtGui


def process_start(window, cmd: List[str], output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", output_clear: bool = True, process_name: str = "youtube_dl"):
    if not window.running:
        window.running = True
        window.status("Busy.")
        download_button.setText("Stop!")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        window.tabWidget.setTabText(window.tabWidget.currentIndex(), "*" + tabName)

        if output_clear:
            output_console.setHtml("")  # clearing the output_console
            output_console.insertPlainText(f"#yt-dl# starting {process_name} please wait...\n")

        if (sys.platform.startswith("win")):  # (os.name == "nt"):
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000, universal_newlines=True, encoding="utf8")  # this one does not check if another process is running
        else:  # (sys.platform.startswith(("linux", "darwin", "freebsd"))): #(os.name == "posix"): #other oeses should be fine with this
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, errors="ignore")

        return process
    else:
        process.terminate()
        window.running = False


def process_output(window, output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", output_clear: bool = True, button_text: str = "Download"):
    if window.running:
        while True:
            if window.isVisible():  # this should make sure that if window dies the subprocess dies too.
                test = process.stdout.readline()
                if not test:
                    break
                test = str(test)
                if "\\n" in test:
                    test = test.replace("\\n", "\n")
                output_console.insertPlainText(test)
                scrollbar = output_console.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
                QtWidgets.QApplication.processEvents()
            else:
                process.terminate()
                exit()  # for some reason killing the subprocess and closing the window dit not kill the app
        print("\a")
        if output_clear:
            output_console.insertPlainText("#yt-dl# Process has finished.\n\n")
        download_button.setText(button_text)
        window.running = False
        window.status("Ready.")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
        QtWidgets.QApplication.processEvents()
        scrollbar = output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
