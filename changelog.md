Due to some miracles on this planet, OSANA got released on 2020-08-31, so this joke is no-longer relevant.<br>
But at-least I'm not pushing bugfixes every day since then :D<br>
Yeah this meme is old by now.<br>

### New in 2.1.3:
new versioning system, Lang, Features, patch/bugfix<br>
Adding new settings will no-longer break on first launch.<br>
Python & pip executable name is now saved in settings<br>
fixed very stupid bugs. I mean 0. Goback now works on Videos & subs.<br>
new debug feature<br>

### New in 2.1.4:
I switched to venv you should too,<br>
dependencies are now in requirements.txt<br>
update now uses requirements.txt to update all dependencies<br>
added a text, so the program does not look like it froze when it's starting youtube-dl<br>
dependency update uses the pip name you set<br>
launch script generator<br>
working autoupdate with a toggle<br>

### New in 2.1.5:
Updating pip before updating dependencies<br>
autoupdate, upgrading dependencies<br>
convert any video to HEVC<br>
generate powershell launch script<br>
got rid of wildcard import<br>
got rid of unused imports<br>
if you are missing dependencies we will help you get them<br>

### New in 2.1.6:
First run, dependency update fix<br>
added support link to my discord https://discord.gg/W88375j<br>
added NVENC h264 encoding <br>
quality of life improvements<br>

### New in 2.1.7:
New install method, no more fiddling, install python, git, clone repo run main.py<br>
ffmpeg and ffprobe can be read from the yt-dl dir (just place them to yt-dl dir)<br>
Re-encoding all videos in a folder, and bunch more re-encode features<br>
is_venv used to not ask users if they are in venv or not.<br>
some parts moved to a second repo (submodule)<br>
tons of bug fixes and overall QoL changes<br>
Finally a tested FreeBSD support!<br>
even an Easter egg.<br>

### New in 2.1.8:
Graphical user interface (gui5.py)<br>
audio + playlist download<br>
video + playlist + quality, list quality download<br>
subtitles + playlists + language, list language download<br>
re-encode + whole folder(folder\\*), presets and more<br>
very bad drag and drop implementation (I hate it, needs to be fixed somehow)<br>
update + autoupdate<br>
settings !default settings may not work for you after setting default check them!<br>
about with link that opens<br>

### New in 2.1.8.1 bugfix:
Fixed output being written into a wrong console label.<br>
Replaced placeholder text in setting tab.<br>
Found by Domo and KoleckOLP, fixed by KoleckOLP<br>

### New in 2.1.9.0:
Improved text rendering on console label, this improves cpu usage and speed by a lot!<br>
Suggested improvement by siscode, fixed by KoleckOLP.<br>

### New in 2.1.9.1 bugfix:
Fixed bug that resulted in default config not generating on some Linux distributions.<br>
Found by KoleckOLP (Arch VM) & kangalioo (Antergos), KoleckOLP found the cause,<br>
Rori fixed it with a pull request.<br>

### New in 2.1.9.2 bugfix:
Fixing issues suggested by PyCharm, which lead me to find that whole folder re-encode "path\\*"<br>
was not working at all.
