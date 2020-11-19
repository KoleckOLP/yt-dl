========================================
### To Do List

To do by severity 2.1.8-gui:
        [done] (highest) youtube-dl output to a TextBox (realtime, or in dire situation a summary)
        [    ] (high)    Audio download (needs testing)
        [done] (medium)  clicking link on TextBox open in external app not the same TextBox (fixed by enabling open external links)
        [done] (medium)  get over the initial hurdles of QTdesigner and QT overall.
        [done] (low)     change colors of the UI
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