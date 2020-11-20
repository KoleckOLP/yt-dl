========================================
### Issue Tracking / To Do List

#       status severity         the issue description                                                   possible solution                                               affected OS
.#1     [done] (highest)        Make sure subprocess is killed when gui dies                            Loop is cheking if gui lives if not kills subprocess            all
.#2     [done] (highest)        Subprocess output to a TextBox                                          Process events after every single line, see .#6                 all
.#3     [done] (high)           Audio download                                                          Somewhat works                                                  all
.#4     [    ] (high)           You can start subpocess more than once download button                  Bool variable that says if subprocess is running already        all
.#5     [    ] (medium)         Remember to save download path with double separator at the end         * Check path saving more carefully                              Windows
.#6     [    ] (medium)         UI runs really slowly while subprocess writing to TextBox               * ProcessingEvents twice a line may be a bad idea               all
.#7     [done] (medium)         Link on a TextBox was opening in TextBox instead of external app        Allowing openExternalLinks                                      all
.#8     [done] (medium)         Get over initial hurdles of QtDesigner, Qt & window resizing            Reading testing                                                 all
.#9     [done] (medium)         ffapps in directory gui support subprocess                              List magics                                                     all
.#10    [done] (low)            Change UI colors                                                        More QtDesigner learning                                        all
.#999   [    ] (low)            Kali: Ctrl+D to quit                                                    * Might actually work in Qt                                     Linux

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