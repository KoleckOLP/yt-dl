from call import *

clear()

if(os.path.exists(settings)):
    name()
    loadpath()
else:
    firstrun()  

while(True):
    print("71. Audio\n2. Video\t6. Update\n3. Exit\t\t7. Download path\n4. Subtitles\t8. About, Changelog")
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