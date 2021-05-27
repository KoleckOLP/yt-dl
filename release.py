import os
import sys
from datetime import datetime

year = datetime.now().year
lstupdt = "2021-05-27"  # Well now that it's in a separate file I should be updating it more often.
spath = sys.path[0]+os.path.sep  # path of the yt-dl dir
settingsPath = spath+"settings.json"
videoDirDefault = spath+"videos"+os.path.sep
audioDirDefault = spath+"audio"+os.path.sep
curb = "testing"
ver = "2.1.10.0"  # !!!Don't forget to change date and window title!!!
