from typing import List
import sys, subprocess, platform
import threading
from queue import Queue, Empty
from PyQt6.QtCore import pyqtSignal, QObject

if (platform.system().lower() == "windows"):
    if (int(platform.version().split(".")[0]) < 10):
        from PyQt5 import QtWidgets

try:
    from PyQt6 import QtWidgets
except Exception as e:
    from PyQt5 import QtWidgets


class OutputEmitter(QObject):
        output_signal = pyqtSignal(str)
        error_signal = pyqtSignal(str)
        finished_signal = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.process = None

        def terminate_process(self):
            if self.process:
                try:
                    self.process.terminate()
                except Exception:
                    pass
                try:
                    self.process.kill()
                except Exception:
                    pass
                self.process = None


def process_start(window, cmd: List[str], output_console: QtWidgets.QTextBrowser, download_button: QtWidgets.QPushButton, process_worker=None, output_clear: bool = True, process_name: str = "yt-dlp", collect_output: bool = False):
    if window.running:
        # Only call terminate_process if it exists
        if hasattr(window, 'process_worker') and window.process_worker:
            if hasattr(window.process_worker, 'terminate_process'):
                window.process_worker.terminate_process()
        window.running = False
        return None

    window.running = True
    window.status("Busy.")
    download_button.setText("Stop!")
    tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
    window.tabWidget.setTabText(window.tabWidget.currentIndex(), "*" + tabName)

    if output_clear:
        output_console.setHtml("")
        output_console.insertPlainText(f"#yt-dl# starting {process_name} please wait...\n")
        output_console.insertPlainText(f"#yt-dl# debug `{' '.join(cmd)}`\n\n")

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000 if sys.platform.startswith("win") else 0, universal_newlines=True, encoding="utf8", errors="ignore", stdin=subprocess.DEVNULL)
    q = Queue()
    emitter = OutputEmitter()
    emitter.process = process
    window.process_worker = emitter  # for compatibility

    def enqueue_output(pipe, tag):
        for line in iter(pipe.readline, ''):
            q.put((tag, line))
        pipe.close()

    t_out = threading.Thread(target=enqueue_output, args=(process.stdout, 'stdout'))
    t_err = threading.Thread(target=enqueue_output, args=(process.stderr, 'stderr'))
    t_out.daemon = True
    t_err.daemon = True
    t_out.start()
    t_err.start()

    collected = [] if collect_output else None

    def process_queue():
        while True:
            try:
                tag, line = q.get(timeout=0.1)
            except Empty:
                if process.poll() is not None:
                    break
                continue
            if tag == 'stderr':
                emitter.error_signal.emit(line)
            else:
                emitter.output_signal.emit(line)
                if collect_output:
                    collected.append(line)
        emitter.finished_signal.emit()

    t_proc = threading.Thread(target=process_queue)
    t_proc.daemon = True
    t_proc.start()

    def handle_output(line):
        if collect_output:
            return  # Do not print real-time output when collecting
        if "\r" in line:
            text = line.split("\r")[-1].rstrip("\n")
            cursor = output_console.textCursor()
            cursor.movePosition(cursor.End)
            cursor.select(cursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deletePreviousChar()
            cursor.insertText(text)
            output_console.setTextCursor(cursor)
        else:
            output_console.insertPlainText(line)
        scrollbar = output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        QtWidgets.QApplication.processEvents()

    def handle_error(line):
        output_console.insertPlainText('[stderr] ' + line)
        scrollbar = output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        QtWidgets.QApplication.processEvents()

    def handle_finished():
        if not collect_output:
            output_console.insertPlainText("#yt-dl# Process has finished.\n\n")
        # Set button text based on which button is used
        if hasattr(download_button, 'objectName') and download_button.objectName() == 'ree_reencode_button':
            download_button.setText("Re-encode")
        else:
            download_button.setText("Download")
        window.running = False
        window.status("Ready.")
        tabName = window.tabWidget.tabText(window.tabWidget.currentIndex())
        if tabName.startswith("*"):
            window.tabWidget.setTabText(window.tabWidget.currentIndex(), tabName[1:])
        QtWidgets.QApplication.processEvents()
        scrollbar = output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    emitter.output_signal.connect(handle_output)
    emitter.error_signal.connect(handle_error)
    emitter.finished_signal.connect(handle_finished)
    return emitter if not collect_output else (emitter, collected)
