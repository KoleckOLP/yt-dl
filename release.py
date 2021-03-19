import sys, os
from datetime import datetime

year = datetime.now().year
lstupdt = "2021-02.26" #Well not that it's a separete file I should be updating it more.
spath = sys.path[0]+os.path.sep #path of the yt-dl dir
settings = spath+"settings.json"
curb = "qt-gui"
ver = "2.1.8"