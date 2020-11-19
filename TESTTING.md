========================================
### To Do List

To do by severity 2.1.7:
        [done] (high)    Convert everything in a folder
        [done] (medium)  posix sh files only support bash, and don't work on BSD at all.        *written, will test on BSD sson*
        [done] (medium)  BSD single quotes on video drag don't work                             *written, will test on BSD sson*
        [done] (high)    BSD reencoding quality is -0.0 with "24,24,24" on BSD ???visual bug??? *will test on BSD soon*
I'wont  [done] (low)     PATH export ffmpeg to the yt-dl dir. is ffmpeg in yt-dl dir
I'wont  [    ] (low)     Ctrl+D to quit (I have no clue how to implement it, and it's not a priority)

========================================
### GitHub

# testing:
git add . (stage changes)
git commit -m "message" (commit)
git push (push)NO

# master:
git checkout master (chage to master)
git merge --squash testing (squash testing branch)
Do all changes you need in master 
git add .
git commit -m "message"
git push

# pull with submodules
git pull --recurse-submodules
git config --global alias.pullall "pull --recurse-submodules"
git pullall

# pushing update to a submodule
(clone the main repo, go into repo folder clone submodule, do not "git submodule init")
updating submodule, "cd submodule", write update "add",  "commit"(update to submodule), "push", "cd..", "add", "commit"(updated submodule), "push", "pullall"

========================================
### Windows Terminal

yt-dl in PowerShell in Windows Terminal
"wt pwsh D:\Programs\1.NoInstall\yt-dl\yt-dl.ps1"