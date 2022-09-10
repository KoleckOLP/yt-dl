import os
from datetime import datetime

year = datetime.now().year
lstupdt = "2022-09-10"  # Well now that it's in a separate file I should be updating it more often.
spath = os.getcwd()+os.path.sep  # sys.path[0]+os.path.sep  # path of the yt-dl dir
settingsPath = spath+"settings.json"
videoDirDefault = spath+"videos"+os.path.sep
audioDirDefault = spath+"audio"+os.path.sep
curb = "testing"
ver = "2.2.1.0"  # 2. python, 2. major, 1. minor, 0 hotfix
