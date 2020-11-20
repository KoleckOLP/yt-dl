========================================
### To Do List

To do by severity 2.1.8-gui (rewrite this into a CSV or formatt better) :
        [    ] (highest)  make sure subprocess dies mhen the main script dies                   (probably was a debug bug, it was not a test bug oof.)
                * Only solution is to check if the window of the app is running anf if it's not terminte the sub process *
        [done] (highest) youtube-dl output to a TextBox                                         (realtime, or in dire situation a summary)
        [done] (high)    Audio download                                                         (needs testing)
        [    ] (high)    You can press the download button many times anf it starts the donload many times
                * Solution would be to have a running/downloading bool variable and check if it's not true *
        [    ] (medium)  Remeber saving downlosad path with a separator at the end              (double) *fix by just saving the path preperly
        [    ] (medium)  the UI runs really slow, can be dragged can be closed but takes two tries
        [done] (medium)  clicking link on TextBox open in external app not the same TextBox     (fixed by enabling open external links)
        [done] (medium)  get over the initial hurdles of QTdesigner and QT overall.
        [done] (medium)  ffmpeg in dir and in PATH implementation.                              (working)
        [done] (low)     change colors of the UI
I'wont  [    ] (low)     Ctrl+D to quit                                                         (I have no clue how to implement it, and it's not a priority)

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