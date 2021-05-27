import sys, os
from datetime import datetime

year = datetime.now().year
lstupdt = "2021-05-25"  # Well now that it's in a separate file I should be updating it more often.
spath = sys.path[0]+os.path.sep  # path of the yt-dl dir
settingsPath = spath+"settings.json"
curb = "temp-test"
ver = "2.1.9.2"  # !!!Don't forget to change date and window title!!!
