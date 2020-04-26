# yt-dl
Multiplatform console youtube-dl simplifier

### Rewriten in Python 3.

runs on any OS if you can get these
Requrements:
+ python3
+ py-getch
+ youtube-dl
+ ffmpeg, ffprobe

I've tried:
Windows 10 x64, Linux x64, MacOS 10.7 x64, HaikuOS x64, Android(Temux) x64

How I set yt-dl up:
1. <b>install ffmpeg & ffprobe</b> (Win: download https://ffbinaries.com/downloads and add it to $PATH)
1. <b>create venv</b> (all: python -m venv env)
2. <b>activate venv</b> (Win: env\Scripts\activate Rest: source env/bin/activate)
3. <b>upgrade pip</b> (All: python -m pip install --upgrade pip)
4. <b>install dependencies</b> (All: pip install -r requirements.txt Haiku: install youtube-dl from Haiku Depot)
5. <b>launch main.py</b> (python main.py)
