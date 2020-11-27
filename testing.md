========================================
### Issue Tracking / To Do List
##2.1.8
GUI:
#       status severity         the issue description                                                   possible solution                                               affected OS
.#1     [done] (highest)        Make sure subprocess is killed when gui dies                            Loop is cheking if gui lives if not kills subprocess            all
.#2     [done] (highest)        Subprocess output to a TextBox                                          Process events after every single line, see .#6                 all
.#3     [done] (high)           Audio download                                                          Somewhat works                                                  all
.#4     [done] (high)           You can start subpocess more than once download button                  Shown in the status, will throw a message box                   all
.#5     [    ] (medium)         Remember to save download path with double separator at the end         * Check path saving more carefully                              Windows
.#6    *[done] (medium)         UI runs really slowly while subprocess writing to TextBox               * I don't think I can fix that so I show satus                  all
.#7     [done] (medium)         Link on a TextBox was opening in TextBox instead of external app        Allowing openExternalLinks                                      all
.#8     [done] (medium)         Get over initial hurdles of QtDesigner, Qt & window resizing            Reading testing                                                 all
.#9     [done] (medium)         ffapps in directory gui support subprocess                              List magics                                                     all
.#14    [done] (medium)         all the downloading lines are taken as a single line                    posible fix switch back to the character by character rendering all
.#15    [    ] (medium)         Learn how to move cursor to begining of current line QTextBrowser       will make the download look nicer                               all
.#10    [done] (low)            Change UI colors                                                        More QtDesigner learning                                        all
.#18    [    ] (low)            Sub download dos not support playlist download                          if supported in yt-dl than with more loops possible             all
.#11    [    ] (low)            Download in a specific tab could be shown by * or color of tab          Starting audio download would change tab name                   all
.#12    [    ] (low)            Colors changeble in config                                              use settings.json                                               all
.#17    [    ] (low)            ffmpeg now hides banner, maybe I could add some debug                   to see waht ffmpeg version I'm using                            all
CLI:
.#13    [    ] (medium)         Bring Loadpath code up to date with changes in gui                      better order and error handling                                 all
.#16    [    ] (medium)         Sub download (long untouched) does not suppot ffmpeg from dir           I wrote sub download and than let it be a black box             all

(I am 100% aware that stuff could have been done better, but I will finifsh it in this way and improve upon it later)

##2.1.9
GUI:
.#1     [   ] (medium)          Less Tabs design audio, vides, sub radio buttons                        Migth be averall better option.                                 all

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

========================================
### Random stuff I need to write down

video url,
playlist
quality