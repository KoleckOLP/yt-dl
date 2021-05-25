import sys, os
from datetime import datetime

year = datetime.now().year
lstupdt = "2021-05-22"  # Well now that it's in a separate file I should be updating it more often.
spath = sys.path[0]+os.path.sep  # path of the yt-dl dir
settigui5 = spath+"gui5_settings.json"
setticli = spath+"cli_settings.json"
curb = "master"
ver = "2.1.9.1"
