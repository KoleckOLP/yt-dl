from kolreq import clear, readchar
from datetime import datetime
from time import sleep
import tempfile
import sys, os
import glob
import json
from PyQt5 import QtCore, QtGui, QtWidgets

year = datetime.now().year
curb = "testing"
ver = f"2.1.7-{curb}" #lang(2python3) #featureset #patch/bugfix pre, RC
lstupdt = "2020-09-05"
spath = sys.path[0]+os.path.sep
settings = spath+"settings.json"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(QtCore.QSize(600, 400))
        MainWindow.setMaximumSize(QtCore.QSize(600, 400))
        MainWindow.setTabletTracking(False)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 600, 400))
        self.tabWidget.setMinimumSize(QtCore.QSize(600, 400))
        self.tabWidget.setMaximumSize(QtCore.QSize(600, 400))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.audio_tab = QtWidgets.QWidget()
        self.audio_tab.setMinimumSize(QtCore.QSize(600, 400))
        self.audio_tab.setMaximumSize(QtCore.QSize(600, 400))

        #AUDIO TAB
        self.audio_tab.setObjectName("audio_tab")
        self.url_box = QtWidgets.QLineEdit(self.audio_tab)
        self.url_box.setGeometry(QtCore.QRect(40, 10, 541, 20))

        self.url_box.setObjectName("url_box")
        self.url_label = QtWidgets.QLabel(self.audio_tab)
        self.url_label.setGeometry(QtCore.QRect(10, 10, 21, 20))

        self.url_label.setObjectName("url_label")
        self.output_console = QtWidgets.QTextBrowser(self.audio_tab)
        self.output_console.setGeometry(QtCore.QRect(10, 70, 571, 271))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_console.sizePolicy().hasHeightForWidth())
        self.output_console.setSizePolicy(sizePolicy)

        self.output_console.setObjectName("output_console")
        self.download_button = QtWidgets.QPushButton(self.audio_tab)
        self.download_button.setGeometry(QtCore.QRect(500, 40, 75, 23))

        self.download_button.setObjectName("download_button")
        self.playlist_checkbox = QtWidgets.QCheckBox(self.audio_tab)
        self.playlist_checkbox.setGeometry(QtCore.QRect(10, 40, 70, 17))

        self.playlist_checkbox.setObjectName("playlist_checkbox")
        self.playlist_bar = QtWidgets.QLineEdit(self.audio_tab)
        self.playlist_bar.setEnabled(False)
        self.playlist_bar.setGeometry(QtCore.QRect(70, 40, 361, 20))

        self.playlist_bar.setObjectName("playlist_bar")
        self.playlist_label = QtWidgets.QLabel(self.audio_tab)
        self.playlist_label.setEnabled(False)
        self.playlist_label.setGeometry(QtCore.QRect(440, 40, 47, 13))
        
        self.playlist_label.setObjectName("playlist_label")
        self.tabWidget.addTab(self.audio_tab, "")
        self.video_tab = QtWidgets.QWidget()
                                        
      s  #VIDEO TAB
        self.video_tab.setObjectName("video_tab")
        self.tabWidget.addTab(self.video_tab, "")
        self.subs_tab = QtWidgets.QWidget()
        self.subs_tab.setMinimumSize(QtCore.QSize(600, 400))
        self.subs_tab.setMaximumSize(QtCore.QSize(600, 400))
        self.subs_tab.setObjectName("subs_tab")
        self.tabWidget.addTab(self.subs_tab, "")
        self.ree_tab = QtWidgets.QWidget()
        self.ree_tab.setObjectName("ree_tab")
        self.tabWidget.addTab(self.ree_tab, "")
        self.upd_tab = QtWidgets.QWidget()
        self.upd_tab.setObjectName("upd_tab")
        self.tabWidget.addTab(self.upd_tab, "")
        self.stn_tab = QtWidgets.QWidget()
        self.stn_tab.setObjectName("stn_tab")
        self.tabWidget.addTab(self.stn_tab, "")
        self.abd_tab = QtWidgets.QWidget()
        self.abd_tab.setObjectName("abd_tab")
        self.about_box = QtWidgets.QTextBrowser(self.abd_tab)
        self.about_box.setGeometry(QtCore.QRect(10, 10, 571, 331))
        self.about_box.setObjectName("about_box")
        self.about_box.setPlainText(f"HorseArmored inc (C){year}\n"
                                   +f"Last updated on: {lstupdt}\n"
                                   +f"Project page: https://github.com/KoleckOLP/yt-dl\n"
                                   +f"need help? ask here: https://discord.gg/W88375j\n"
                                   +f"           (C)2011-{year} youtube-dl developers\n"
                                   +f"ffmpeg (C)2000-{year} FFmpeg team")
        self.tabWidget.addTab(self.abd_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "yt-dl_gui"))
        self.url_label.setText(_translate("MainWindow", "URL:"))
        self.download_button.setText(_translate("MainWindow", "Download"))
        self.playlist_checkbox.setText(_translate("MainWindow", "playlist"))
        self.playlist_label.setText(_translate("MainWindow", "1,3,7-9"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.audio_tab), _translate("MainWindow", "Audio"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.video_tab), _translate("MainWindow", "Video"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.subs_tab), _translate("MainWindow", "Subs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ree_tab), _translate("MainWindow", "Re-encode"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.upd_tab), _translate("MainWindow", "Update"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stn_tab), _translate("MainWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.abd_tab), _translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
