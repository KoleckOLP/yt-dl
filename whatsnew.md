New in 2.1.5
Updating pip before updating dependencies

New in 2.1.4
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

Osana is still not finished, lol.

To do by severity:
        [done] (extreme) fix updating
        [done] (high)    update pip
        [done] (high)    to HEVC
        [    ] (normal)  add colors
        [done] (normal)  generate powershell launch script
        [    ] (low)     PATH export ffmpeg to the yt-dl dir.

how to git:

testing:
git add . (stage changes)
git commit -m "message" (commit)
git push

master:
git checkout master
git merge --squash testing
Do all changes you need in master
git add .
git commit -m "message"
git push