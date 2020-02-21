from call import *

clear()

if(os.path.exists(settings)):
    print(f"yt-dl {ver} by KoleckOLP (C){year}\n")
    loadpath()
else:
    firstrun()
    

while(True):
    print("\n1. Audio\n2. Video\n3. Exit\n4. Subtitles\n\n6. Update\n"+
    "7. About & Credits\n8. Show Download path\n9. Change Download path")
    cmd = readchar("#")

    if(cmd == "1"): #Audio
        audiod()
    elif(cmd == "2"): #Video
        videod()
    elif(cmd == "3"): #Exit (done)
        print("See you later aligator.")
        break
    elif(cmd == "4"): #Subtitles
        subd()
    elif(cmd == "6"): #Update (done)
        update()
    elif(cmd == "7"): #About (done)
        about()
    elif(cmd == "8"): #showpath (done)
        clear()
        loadpath()
    elif(cmd == "9"): #savepath (done)
        clear()
        savepath()
        clear()
        loadpath()
    elif(cmd == "`"): #debug (done)
        debug()
    else:
        clear()
        print(f"\"{cmd}\" is not an option.")