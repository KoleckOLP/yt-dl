New in 2.1.7:
New install method, no more fiddling, intall python, git, clone repo run main.py
FFmpeg and FFprobe can be read from the yt-dl dir (just place them to yt-dl dir)
Re-encoding all videos in a folder, and buch more re-encode features
even an Easter egg.
some parts moved to a second repo (submodule)
is_venv used to no ask users if they are in vevn or not.
tons of bug fixes and overall QoL changes

New in 2.1.5:
Updating pip before updating dependencies
autoupdate, upgrading dependencies
convert any video to HEVC
generate powershell launch script
got rid of wildcard import
got rid of unused imports
if you are missing dependencies we will help you get them

New in 2.1.4:
I switched to venv you should too,
dependecie are now in requirements.txt
update now uses requirements.txt to update all dependencies
added a text so the program does not look like it froze when it's starting youtube-dl
dependecy upglade uses the pip name you set
launch script generator
working autoupdate with a toggle

New in 2.1.3
new versioning system, Lang, Featureset, patch/bugfix
Adding new settings will nolonger break on first launch.
Python & pip executable name is now saved in settings
fixed very stupid bugs. I mean 0. Goback now works on Videos & subs.
new debug feature

Due to some miracles on this planet OSANA got relesed on 2020-08-31, so this joke is nolonger relevant.
But at-least I'm not pushing bugfixes everyday since than :D

To do by severity 2.1.7:
        [done] (high)    Convert everything in a folder
        [    ] (medium)  posix sh files only support bash, and don't work on BSD at all.        *written, will test on BSD sson*
        [    ] (medium)  BSD single quotes on video drag don't work                             *written, will test on BSD sson*
        [    ] (high)    BSD reencoding quality is -0.0 with "24,24,24" on BSD ???visual bug??? *will test on BSD soon*
I'wont  [done] (low)     PATH export ffmpeg to the yt-dl dir. is ffmpeg in yt-dl dir
I'wont  [    ] (low)     Ctrl+D to quit (I have no clue how to implement it, and it's not a priority)


how to git:

testing:
git add . (stage changes)
git commit -m "message" (commit)
git push (push)NO

master:
git checkout master (chage to master)
git merge --squash testing (squash testing branch)
Do all changes you need in master 
git add .
git commit -m "message"
git push

updating submodule cd submodule, write update add, commit(update to submodule), push, cd.., add, commit(updated submodule), push, git pull --recurse-submodules(git pullall *alias*)

yt-dl in PowerShell in Windows Terminal
"wt pwsh D:\Programs\1.NoInstall\yt-dl\yt-dl.ps1"
