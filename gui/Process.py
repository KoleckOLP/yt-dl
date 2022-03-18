import sys
import subprocess
from typing import List
try:
    from PyQt6 import QtWidgets, QtGui
    from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
except ModuleNotFoundError:
    from PyQt5 import QtWidgets, QtGui


class Action(QObject):
    runProcess = pyqtSignal(str)

    @pyqtSlot()
    def RunProcess(self, cmd: List[str], output_console: QtWidgets.QTextBrowser):
        self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        creationflags=0x08000000, universal_newlines=True, encoding="utf8",
                                        errors="ignore")

        while (True):
            output = self.process.stdout.readline()
            prettyOutput = output
            output_console.insertPlainText(prettyOutput)
            QtWidgets.QApplication.processEvents()


class Whatever():
    def sadCry(self, window, cmd, output_console):
        window.action = Action()
        window.thread = QThread(window)
        window.action.runProcess.connect(Action.RunProcess)
        window.action.moveToThread(window.thread)
        window.thread.started.connect(lambda: window.action.RunProcess(cmd, output_console))
        window.thread.start()
