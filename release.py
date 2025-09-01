import os
from datetime import datetime

year = datetime.now().year
lstupdt = "2026-01-21"  # Well now that it's in a separate file I should be updating it more often.
spath = os.getcwd()+os.path.sep  # sys.path[0]+os.path.sep  # path of the yt-dl dir
settingsPath = spath+"settings.json"
videoDirDefault = spath+"videos"+os.path.sep
audioDirDefault = spath+"audio"+os.path.sep
<<<<<<< HEAD
curb = "refactor/snake_case_naming"
ver = "2.2.3.3"  # 2. python(language), 2. major(gigantic), 1. minor(big), 1 hotfix(small)
=======
curb = "Threading3"
ver = "2.2.4.0-dev3"  # 2. python(language), 2. major(gigantic), 1. minor(big), 1 hotfix(small)
>>>>>>> c40dbbf (Fixing Windows 8.1 again...)
