import os
import sys
from datetime import datetime

year = datetime.now().year
lstupdt = "2021-07-30"  # Well now that it's in a separate file I should be updating it more often.
spath = os.getcwd()+os.path.sep  # sys.path[0]+os.path.sep  # path of the yt-dl dir
settingsPath = spath+"settings.json"
videoDirDefault = spath+"videos"+os.path.sep
audioDirDefault = spath+"audio"+os.path.sep
curb = "testing"
ver = "2.2.0.0"
