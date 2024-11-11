import sys
import subprocess
import threading
from typing import List
try:
    from PyQt6 import QtWidgets
except ModuleNotFoundError:
    from PyQt5 import QtWidgets


def process_start(window, cmd: List[str], output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process: subprocess.Popen = "", output_clear: bool = True, process_name: str = "yt-dlp"):
    if not window.running:
        window.running = True
        window.status("Busy.")
        download_button.setText("Stop!")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        window.tabWidget.setTabText(window.tabWidget.currentIndex(), "*" + tabName)

        if output_clear:
            output_console.setHtml("")  # clearing the output_console
            if (process_name == "none"):  # this is horrible xD
                process_name = "yt-dlp"
            output_console.insertPlainText(f"#yt-dl# starting {process_name} please wait...\n")

        if (sys.platform.startswith("win")):  # (os.name == "nt"):
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000, universal_newlines=True, encoding="utf8", errors="ignore")  # this one does not check if another process is running
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
                line = process.stdout.readline()
                if not line:
                    break
                line = str(line)
                if "\\n" in line:
                    line = line.replace("\\n", "\n")
                #print(test)
                output_console.insertPlainText(line)
                scrollbar = output_console.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
                QtWidgets.QApplication.processEvents()
            else:
                process.terminate()
                exit()  # for some reason killing the subprocess and closing the window dit not kill the app, huh exit does not exists?
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


def run_process_mto(window, cmd, output_console, download_button, output_clear_proc: bool = True, process_name: str = "none", output_clear_out: bool = True, button_text: str = "Download"):  # !!!Multi Threaded Ouput!!! still has a tendency to random crash
    window.process = process_start(window, cmd, output_console,  download_button, window.process, output_clear_proc, process_name)

    thread = threading.Thread(target=process_output, args=(window, output_console, download_button, window.process, output_clear_out, button_text))
    thread.start()  # this is kinda bad because I'm editting the gui from a thread, and it could go wrong, I shold be emitting signals from a thread instead.

def run_process_sto(window, cmd, output_console, download_button, output_clear_proc: bool = True, process_name: str = "none", output_clear_out: bool = True, button_text: str = "Download"):  # !!!Single Threadded Output!!! for gui/Update.py
    window.process = process_start(window, cmd, output_console, download_button, window.process, output_clear_proc, process_name)
    if (process_name == "yt-dlp"):
        window.upd_output_console.append("yt-dlp ")
    process_output(window, window.upd_output_console, window.upd_update_button, window.process, output_clear_out, button_text)
