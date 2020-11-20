Due to some miracles on this planet OSANA got relesed on 2020-08-31, so this joke is nolonger relevant.
But at-least I'm not pushing bugfixes everyday since than :D, I'm not updating almost at all.
If you want to see what I'm up to checkout testing or other branches.

New in 2.1.3
new versioning system, Lang, Featureset, patch/bugfix
Adding new settings will nolonger break on first launch.
Python & pip executable name is now saved in settings
fixed very stupid bugs. I mean 0. Goback now works on Videos & subs.
new debug feature

New in 2.1.4:
I switched to venv you should too,
dependecie are now in requirements.txt
update now uses requirements.txt to update all dependencies
added a text so the program does not look like it froze when it's starting youtube-dl
dependecy upglade uses the pip name you set
launch script generator
working autoupdate with a toggle

New in 2.1.5:
Updating pip before updating dependencies
autoupdate, upgrading dependencies
convert any video to HEVC
generate powershell launch script
got rid of wildcard import
got rid of unused imports
if you are missing dependencies we will help you get them

New in 2.1.7:
New install method, no more fiddling, intall python, git, clone repo run main.py
FFmpeg and FFprobe can be read from the yt-dl dir (just place them to yt-dl dir)
Re-encoding all videos in a folder, and buch more re-encode features
is_venv used to not ask users if they are in venv or not.
some parts moved to a second repo (submodule)
tons of bug fixes and overall QoL changes
Finally a tested FreeBSD supprt!
even an Easter egg.