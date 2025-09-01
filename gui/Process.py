from typing import List
import sys, subprocess, platform
from collections import deque

if (platform.system().lower() == "windows"):
    if (int(platform.version().split(".")[0]) < 10):
        from PyQt5 import QtWidgets
        from PyQt6.QtCore import QThread, pyqtSignal

try:
    from PyQt6 import QtWidgets
    from PyQt6.QtCore import QThread, pyqtSignal
except Exception as e:
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import QThread, pyqtSignal


class ProcessThread(QThread):
    line_received = pyqtSignal(str)

    def __init__(self, process, window):
        super().__init__()
        self.process = process
        self.window = window
        self._running = True

    def run(self):
        while self._running:
            line = self.process.stdout.readline()
            if line == '' and self.process.poll() is not None:
                break
            if "\\n" in line:
                line = line.replace("\\n", "\n")
            self.line_received.emit(line)
        self.finished.emit()

    def stop(self):
        self._running = False
        try:
            self.process.terminate()
        except Exception:
            pass


def process_start(window, cmd: List[str], output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", output_clear: bool = True, process_name: str = "yt-dlp"):
    if not window.running:
        window.running = True
        window.status("Busy.")
        download_button.setText("Stop!")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        window.tabWidget.setTabText(window.tabWidget.currentIndex(), "*" + tabName)

        if output_clear:
            output_console.setHtml("")  # clearing the output_console
            output_console.insertPlainText(f"#yt-dl# starting {process_name} please wait...\n")
            output_console.insertPlainText(f"#yt-dl# debug `{' '.join(cmd)}`\n\n")

        if (sys.platform.startswith("win")):  # (os.name == "nt"):
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000, universal_newlines=True, encoding="utf8", errors="ignore", stdin=subprocess.DEVNULL)  # this one does not check if another process is running, stdin=subprocess.DEVNULL
        else:  # (sys.platform.startswith(("linux", "darwin", "freebsd"))): #(os.name == "posix"):  # other oeses should be fine with this
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, errors="ignore")
    else:
        process.terminate()
        window.running = False
    return process


def process_output(window, output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", output_clear: bool = True, button_text: str = "Download"):
    if window.running:
        while True:
            if window.isVisible():  # this should make sure that if window dies the subprocess dies too.
                test = process.stdout.readline()
                if test == '' and process.poll() is not None:
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
                sys.exit()  # for some reason killing the subprocess and closing the window dit not kill the app, huh exit does not exists?
        print("\a", end="")  # play alert sound without printing a new line
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


def process_output_threaded(window, output_console, download_button, process, output_clear=True, button_text="Download"):
    thread = ProcessThread(process, window)

    def handle_line(line):
        output_console.insertPlainText(line)
        scrollbar = output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_finished():
        if output_clear:
            output_console.insertPlainText("#yt-dl# Process has finished.\n\n")
        download_button.setText(button_text)
        window.running = False
        window.status("Ready.")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        if tabName.startswith("*"):
            window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])

    thread.line_received.connect(handle_line)
    thread.finished.connect(on_finished)
    thread.start()

    return thread
