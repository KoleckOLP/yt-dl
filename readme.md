# yt-dl
Multiplatform cli (soon gui) youtube-dl simplifier

### Rewriten in Python 3.

runs on any OS if you can get these
Requrements:
+ python3
+ python libraries
+ youtube-dl
+ ffmpeg, ffprobe
<br>

Tested Working:<br>
+ Windows 10 x64<br>
+ Linux x64<br>

Not Tested:<br>
+ Mac OS 10.7 x64<br>
+ HaikuOS x64<br>
+ Android(Temux) x64<br>

Tested Not Working:<br>
+ freeBSD x64<br>
<br>

How to set yt-dl up:<br>
## Windows:
1. intall git: https://git-scm.com/download/win
2. install python3: https://www.python.org/downloads/
3. clone repo with git `git clone https://github.com/koleckolp/yt-dl`
    1. \(optional) update pip: `py -m pip install -U pip`
4. install requirements: `pip install -r requirements.txt`
5. download ffmpeg.exe and ffprobe.exe: https://ffbinaries.com/downloads and put them into the yt-dl directory
5. launch `pythonw gui5.py` (if you are missing a config hit ok and restart the app)
    1. \(recommended) on the settings tab fix your setting and Make Lauch Script
    2. than you can make a desktop shortcut from `yt-dl_gui.bat` or `yt-dl_gui.vbs` (which ever you like)

## Linux:
1. install git (with your package manager)
2. install python3 (with your package manager)
3. clone repo with git `git clone https://github.com/koleckolp/yt-dl`
    1. \(optional) update pip (with pip): `py -m pip install -U pip`
4. install ffmpeg (with your package manager)
4. launch `python gui5.py` (if you are missing a config hit ok and restart the app)
    1. \(recommended) on the settings tab fix your setting and Make Lauch Script
    2. than you can make a desktop shortcut from `yt-dl`

Haiku(icon and re-encode does not work yet):
1. install git (from HaikuDepot)
2. install pyqt_x86_python3, python3_x86, pip_python3 (from HaikuDepot, or 64bit equivalent)
3. clone repo with git `git clone https://github.com/koleckolp/yt-dl`
4. install ffmpeg, ffmpeg-tools and youtube-dl (from HaikuDepot)
5. launch `python gui5.py` (if you are missing a config hit ok and restart the app)
4. launch `python gui5.py` (if you are missing a config hit ok and restart the app)
    1. \(recommended) on the settings tab fix your setting and Make Lauch Script
    2. than you can make a desktop shortcut from `yt-dl`

Mac:
1. To do

BSD:
1. To do