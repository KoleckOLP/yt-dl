from call import *

clear()

if(os.path.exists(settings)):
    name()
    loadpath()
else:
    print("Welcome to first time setup,\n"
         +"This program requires py-getch, youtube-dl, ffmpeg & ffprobe\n"
         +"Do you have all the requirements? [Y/n]")
    cmd = input("#")
    cmd = cmd.lower() 
    if (cmd == "y"):
        pass
    else:
        print("Install all the dependencies and come back")
        exit()
    print("Have you installed youtube-dl with pip? [Y/n]]")
    cmd = input("#")
    cmd = cmd.lower() 
    if (cmd == "y"):
        ydpip = True
    else:
        ydpip = False
    savepath(ydpip)   

while(True):
    print("\n1. Audio\n2. Video\t6. Update\n3. Exit\t\t7. Download path\n4. Subtitles\t8. About, Changelog")
    cmd = readchar("#")

    if(cmd == "1"): #audio
        audiod()
    elif(cmd == "2"): #video
        videod()
    elif(cmd == "3"): #exit
        print("See you later aligator.")
        break
    elif(cmd == "4"): #subtitles
        subd()
    elif(cmd == "6"): #update
        update()
    elif(cmd == "7"): #save load path
        clear()
        slpath()
    elif(cmd == "8"): #about
        about()
    elif(cmd == "`"): #debug
        debug()
    else:
        clear()
        print(f"\"{cmd}\" is not an option.")