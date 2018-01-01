# Csgo Global Talk (CGT) lets you communicate in different languages in CS:GO.
# Copyright (C) 2018  Tyzeron
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# -------------------------------------------------------------------
# |                                                                 |
# |  _____                                                        ) |
# | /__   \_   _ _______ _ __ ___  _ __                          (  |
# |   / /\/ | | |_  / _ \ '__/ _ \| '_ \    ,___________  ______  )  
# |  / /  | |_| |/ /  __/ | | (_) | | | |  /_///_______(=(_____()    
# |  \/    \__, /___\___|_|  \___/|_| |_|   /  (')  L_O              
# |        |___/                           /__/                     |
# |                                                                 |
# |    ___               _            _   _                         |
# |   / _ \_ __ ___   __| |_   _  ___| |_(_) ___  _ __              |
# |  / /_)/ '__/ _ \ / _` | | | |/ __| __| |/ _ \| '_ \             |
# | / ___/| | | (_) | (_| | |_| | (__| |_| | (_) | | | |            |
# | \/    |_|  \___/ \__,_|\__,_|\___|\__|_|\___/|_| |_|            |
# |                                                                 |
# -------------------------------------------------------------------      --  -
#

import os, sys
from ConfigParser import RawConfigParser
#from colorama import init, Fore, Style
from googletrans import Translator, LANGUAGES
from time import sleep
from codecs import open
from Tkinter import Tk, Text, TclError
from ttk import Scrollbar
from keypress import press, keyDictionary
from requests import get #for getting version

def path():
#    print("Function: path")
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def minSec(t):
    print("Function: minSec")
    m, s = divmod(t, 60)
    if m == 0:
        return str(s) + " sec"
    elif s == 0:
        return str(m) + " min"
    else:
        return str(m) + " min " + str(s) + " sec"

def error(e,cs=False,t=""):
    print("Function: error")
    for i in e.split("\n"):
        cprint(cRED + "[ERROR] " + i)
    if cs:
        ce = "<CSGO GLOBAL TALK>: [WARNING] " + e
        send("say" + t + " " + ce + "\necho " + ce)
    clean()
    cprint(cYELLOW + "After reading the error message, please close this program.")
    from tkMessageBox import showerror
    showerror("Csgo Global Talk v" + VERSION + " - Error",e)
    while True:
        update()

def update():
    try:
        tk.update()
    except TclError:
        #print("Tcl Error in update() function")
        raise SystemExit
    except Exception as e:
        print "IGNORE: " + str(e)

def cprint(s,l=True):
#    print("Function: cprint")
    s = cWHITE + s
    s = s.split("[")
    #console.configure(state="normal")
    for i in s:
        console.insert('end',i[3:],i[:3]) #write at the end, string to print, color
    if l:
        console.insert('end',"\n")
    console.see("end")
    update()
    #console.configure(state="disabled")
    return True

#def dPrint(s): #print stuff for developers when needed
#    if customDebug:
#        #cprint(cBLUE + "<DEBUG> : " + s)
#        print s
#        return True
#    else:
#        return False

def warning(e,cs=False,t=""):
    print("Function: warning")
    for i in e.split("\n"):
        cprint(cRED + "[WARNING] " + e)
    if cs:
        e = "<CSGO GLOBAL TALK>: [WARNING] " + e
        send("say" + t + " " + e + "\necho " + e)
    return True

def cRemove(s):
#    print("Function: cRemove")
    for i in [cRED, cGREEN, cYELLOW, cMAGENTA, cCYAN, cWHITE, cBLUE]:
        s = s.replace(i,"")
    return s

def conf(sect,opt=None,val=None):
    print("Function: conf")
    if not os.path.isfile(path() + "\\cgt.ini"):
        error("Missing cgt.ini! Please re-download or check for missing file!")
    #config = RawConfigParser()
    #config.add_section("Basic")
    #config.set("Basic", "path", "None")
    #config.set("Basic", "default language", "None")
    #config.set("Basic", "control key", "None")
    config = RawConfigParser()
    config.read("cgt.ini")
    if val != None:
        config.set(sect, opt, val)
        with open("cgt.ini", "wb") as f:
            config.write(f)
        return True
    else:
        return dict(config.items(sect))

def translate(t,s,d): #text, source language (s can be 'auto'), destination language
    print("Function: translate")
    #if dPrint("TRANSLATE: '" + t + "'\n\tSource language: '" + s + "' \t Target language: '" + d + "'"):
    #    return s
    print("TRANSLATING: '" + t + "', source: '" + s + "', target: '" + d + "'")
    f = translator.translate(t, src=s, dest=d)
    #if f.origin != t:
    #    error("Translation not working properly! CODE: 6655")
    return f.text

def sendTranslate(s,t,p): #translated message, if teamchat then t="_team" else t="", player that got translated (if nobody then p=" ")
    print("Function: sendTranslate")
    if p != " ":
        p = p + ": "
    send("say" + t + " " + signature + p + s + "\necho <CSGO GLOBAL TALK>: Successfully translated:" + p + s)

def send(s=None):#echo <CSGO GLOBAL TALK>:
    print("Function: send")
    global command
    if s == None:
        s = "echo <CSGO GLOBAL TALK>: Nothing to translate."
        command = False
    else:
        if command:
            warning("Previous message to CSGO has FAILED to be delivered!")
        command = True
    print "WRITE: " + s
    with open(cfgPath + "cgt_command.cfg","w",encoding="utf-8") as f:
        f.write(s + "\n")
    if command:
        print("Pressing '" + controlKey + "'")
        press(controlKey)

def ezSend(s,t):
    print("Function: ezSend")
    cprint(s)
    s = cRemove(s)
    s = "<CSGO GLOBAL TALK>: " + s
    send("say" + t + " " + s + "\necho " + s)

def rm(s):
    print("Function: rm")
    try:
        os.remove(s)
    except Exception as e:
        print "IGNORE: " + str(e)

def clean():
    print("Function: clean")
    for i in ["cgt.cfg","cgt_command.cfg","csgo_global_talk.cfg","cgt_help.cfg","cgt_players.cfg"]:
        try:
            rm(cfgPath + i)
        except Exception as e:
            print "IGNORE: " + str(e)

def close():
    print("Function: close")
    cprint(cYELLOW + "Closing...")
    clean()
    try:
        tkClose(tk)
    except Exception as e:
        print "IGNORE: " + str(e)
    print "END"
    raise SystemExit

def askDir(q="Please select a directory"):
    print("Function: askDir")
    #from Tkinter import Tk
    from tkFileDialog import askdirectory
    
    #tk = Tk()
    #tk.iconbitmap(default="cgt.ico")
    #tk.title("Csgo Global Talk v" + VERSION + " - Select a directory")
    #tk.withdraw() #use to hide tkinter window
    d = askdirectory(parent=tk, initialdir="/", title=q)
    #tk.deiconify() #use to show back tkinter window, without this future tkinter is not working
    #tk.destroy()
    return d

def tkClose(t):
    t.destroy()
    t.quit()

def askDefLang():
    print("Function: askDefLang")
    #from Tkinter import Tk, StringVar, Label, Radiobutton
    from Tkinter import Toplevel, StringVar, Label, Radiobutton
    from ttk import Button
    #tk = Tk()
    tk = Toplevel()
    tk.iconbitmap(default="cgt.ico")
    tk.title("Csgo Global Talk v" + VERSION + " - Default Language")
    var = StringVar()
    var.set(1)
    def tclose():
        print("Function: tclose (in Function: askDefLang)")
        if var.get() == "1":
            if defaultLanguage:
                tkClose(tk)
                return
            warning("You must choose a default language (a language you use)")
        else:
            global defaultLanguage
            defaultLanguage = var.get()
            tkClose(tk)
    def fclose():
        print("Function: fclose (in Function: askDefLang)")
        if defaultLanguage:
            tkClose(tk)
            return
        from tkMessageBox import askokcancel
        if askokcancel("Csgo Global Talk v" + VERSION, "You did not choose a default language!\nDo you want to exit the program?"):
            tkClose(tk)
            close()
    r=4
    c=1
    mxR=21#max number of row in lang
    for slang, lang in sorted(LANGUAGES.iteritems()): #slang - language shortcut
        if slang == "en" or slang == "ru" or slang == "de" or slang == "pl":
            Radiobutton(tk, text = lang.capitalize(), font="Helvetica 10 bold", fg="blue", variable=var, value = slang, width = 15, anchor="w").grid(row=r, column=c)
        else:
            Radiobutton(tk, text = lang.capitalize(), font="Helvetica 10", variable=var, value = slang, width = 15, anchor="w").grid(row=r, column=c)
        r=r+1
        if r > mxR:
            r=4
            c=c+1
    c=c+1#number of columns (starts 0 so +1)
    Label(tk, text = " ").grid(row=0,columnspan=c)
    Label(tk, text = "Select your DEFAULT language",font="bold").grid(row=1,columnspan=c)
    Label(tk, text = "(a language want you want to translate to)").grid(row=2,columnspan=c)
    Label(tk, text = " ").grid(row=3,columnspan=c)
    Label(tk, text = " ").grid(row=mxR+1,columnspan=c)
    #Button(tk, text = "OK", font="bold", width = 15, command=close).grid(row=mxR+2, columnspan=c) FOR: from Tkinter import Button
    Button(tk, text = "OK", width = 15, command=tclose).grid(row=mxR+2, columnspan=c)
    Label(tk, text = " ").grid(row=mxR+3,columnspan=c)
    tk.protocol("WM_DELETE_WINDOW", fclose)
    tk.mainloop()

def askKey():
    print("Function: askKey")
    #from Tkinter import Tk, StringVar, Label
    from Tkinter import Toplevel, StringVar, Label
    from ttk import Combobox, Button
    #tk = Tk()
    tk = Toplevel()
    tk.iconbitmap(default="cgt.ico")
    tk.title("Csgo Global Talk v" + VERSION + " - Select Control Key")
    var = StringVar()
    var.set("")
    def tclose():
        print("Function: tclose (in Function: askKey)")
        if var.get() == "":
            if controlKey:
                tkClose(tk)
                return
            warning("You must choose a control key (toggles translation)")
        elif var.get().upper() not in keyBinds:
            warning("Please choose an acceptable key.")
        else:
            global controlKey
            controlKey = var.get().upper()
            tkClose(tk)
    def fclose():
        print("Function: fclose (in Function: askKey)")
        if controlKey:
            tkClose(tk)
            return
        from tkMessageBox import askokcancel
        if askokcancel("Csgo Global Talk v" + VERSION, "You did not select any control key (toggle translate)!\nDo you want to exit the program?"):
            tkClose(tk)
            close()
    cb = Combobox(tk, textvariable=var, values=keyBinds)
    cb.grid(row=2,column=1)
    cb.config(width=25)
    Label(tk, text = " ", width = 2).grid(row=0)
    Label(tk, text = "Select a control key (toggles translation)").grid(row=1,column=1)
    Label(tk, text = " ", width = 2).grid(column=0)
    Label(tk, text = " ", width = 2).grid(column=2)
    Label(tk, text = " ", width = 2).grid(row=3)
    Button(tk, text="Done", width=15, command=tclose).grid(row=4,column=1)
    Label(tk, text = " ", width = 2).grid(row=5)
    tk.protocol("WM_DELETE_WINDOW", fclose)
    tk.mainloop()

def verifyPath(c):
    print("Function: verifyPath")
    if not os.path.isfile(c + "\\csgo.exe"):
        warning("Cannot locate csgo.exe in your CSGO folder.")
        return False
    if not os.path.isdir(c + "\\csgo\\cfg"):
        warning("Cannot locate configuration folder in your CSGO folder.")
        return False
    return True

def getCpath():
    print("Function: getCpath")
    cpath = conf("Basic")["path"]
    if not cpath == "None" and verifyPath(cpath):
        return cpath
    else:
        while True:
            cpath = askDir("Please select \"Counter-Strike Global Offensive\" folder\n\nIt is located under \"STEAM FOLDER\steamapps\common\Counter-Strike Global Offensive\"")
            if cpath == "":
                error("You did not select any directory!")
            if verifyPath(cpath):
                conf("Basic","path",cpath)
                return cpath

def getDefLang():
    print("Function: getDefLang")
    defLan = conf("Basic")["default language"]
    if not defLan == "None" and defLan in LANGUAGES.keys():
        global defaultLanguage
        defaultLanguage = defLan
    else:
        global defaultLanguage
        defaultLanguage = None
        askDefLang()
        conf("Basic","default language",defaultLanguage)

def getKey():
    print("Function: getKey")
    ckey = conf("Basic")["control key"]
    if not ckey == "None" and ckey in keyBinds:
        global controlKey
        controlKey = ckey
    else:
        global controlKey
        controlKey = None
        askKey()
        conf("Basic","control key",controlKey)

def waitExec():
    print("Function: waitExec")
    if not os.path.isfile(cfgPath + "csgo_global_talk.cfg"):
        t = 0
        cprint(cYELLOW + "Waiting for user to type '" + cCYAN + "exec cgt" + cYELLOW + "' intro CS:GO console...")
        while not os.path.isfile(cfgPath + "csgo_global_talk.cfg"):
            update()
            t = t + 1
            sleep(0.05)
        #print(cGREEN + "Waited " + minSec(t) + " till"),
        cprint(cGREEN + "Waited " + minSec(int(t/20)) + " till",l=False)
    cprint(cGREEN + "CSGO Global Talk finished loading!")

def getName():
    print("Function: getName")
    t = 0
    while t <= 100:
        with open(cfgPath + "csgo_global_talk.cfg","r") as f:
            for l in f:
                l = l.rstrip()
                update()
                if '"name" = ' in l:
                    return l.split('"name" = ')[1].split('"')[1]
        t = t + 1
        sleep(0.05)
    error("Couldn't get your CSGO name!")

def writeHelp():
    print("Function: writeHelp")
    with open(cfgPath + "cgt_help.cfg","w") as f:
        f.write("echo\necho\necho\necho " + "-"*53 + "\necho\n")
        f.write("echo " + "<"*15 + " CSGO GLOBAL TALK HELP " + ">"*15 + "\necho\n")
        f.write('echo "YOUR CSGO NAME: \t' + name + '"\n')
        f.write('echo "DEFAULT LANGUAGE: \t' + LANGUAGES[defaultLanguage].capitalize() + '"\n')
        if targetLanguage:
            tl = LANGUAGES[targetLanguage].capitalize()
        else:
            tl = "NONE"
        f.write('echo "TARGET LANGUAGE: \t' + tl + '"\n')
        f.write('echo "CONTROL KEY: \t\t' + controlKey + '"\necho\necho\n')
        f.write("echo TRANSLATED PLAYERS:\n")
        for x,y in players.iteritems():
            if y == "auto":
                z = "Auto-detect"
            else:
                z = LANGUAGES[y].capitalize()
            f.write('echo "' + x + ' (his/her language: ' + z + ')"\n')
        f.write("\necho\necho\necho LIST OF LANGUAGES:\necho\n")
        for x,y in sorted(LANGUAGES.iteritems()):
            f.write('echo "   ' + x + ' '*(6-len(x)) + ' |   ' + y.capitalize() + '"\n')
        f.write("echo\necho " + "-"*53 + "\n")

def readPlayers():
    print("Function: readPlayers")
#    cprint(cYELLOW + "Waiting for players list...")
#    t = 0
#    while t <= 100:
    if os.path.isfile(cfgPath + "cgt_players.cfg"):
#        cprint(cGREEN + "Waited " + str(float(t)*0.05)) + " seconds."
        with open(cfgPath + "cgt_players.cfg","r") as f:
            a = f.readlines()
        global allPlayers
        allPlayers = {}
        os.remove(cfgPath + "cgt_players.cfg")
        if a[0] == "No players currently connected who can be muted.":
            warning("No 'real' player can be found!")
            print "empty player list"
            return
        for i in a[2:-1]:
            x,y = i.strip().split(" "*9)
            allPlayers[x] = y
    else:
        warning("Failed to read players list!",cs=True)
#        tk.update()
#        t = t + 1
#        sleep(0.05)

def setup():
    print("Function: setup")
    clog = cfgPath + "csgo_global_talk.cfg"
    if os.path.isfile(cfgPath + "csgo_global_talk.cfg"):
        try:
            os.remove(cfgPath + "csgo_global_talk.cfg")
        except WindowsError:
            cprint(cRED + "CSGO is probably already running. It should be fine but not suggested.")
    if os.path.isfile(cfgPath + "cgt_players.cfg"):
        os.remove(cfgPath + "cgt_players.cfg")
    with open(cfgPath + "cgt.cfg","w") as f: #cgt.cfg
        f.write("con_logfile cfg\\csgo_global_talk.cfg\n") #csgo_global_talk.cfg
        f.write("echo Starting Csgo Global Talk...\n")
        f.write("name\necho\necho\n")
        for i in logo:
            #f.write("echo" + i.replace(cRED,"").replace(cGREEN,"").replace(cYELLOW,"").replace(cWHITE,"").replace(cCYAN,"") + "\n")
            f.write('echo "' + cRemove(i) + '"\n')
        f.write("echo\necho\n")
        for i in logo2:
            #f.write("echo" + i.replace(cRED,"").replace(cGREEN,"").replace(cYELLOW,"").replace(cWHITE,"").replace(cCYAN,"") + "\n")
            f.write('echo "' + cRemove(i) + '"\n')
        f.write('bind ' + controlKey + ' "exec cgt_command.cfg"\n')
        f.write('alias cgt "exec cgt_help.cfg"\n')
        f.write('alias players "echo; echo; con_logfile cfg\\cgt_players.cfg; voice_show_mute; con_logfile cfg\\csgo_global_talk.cfg; echo; echo <CSGO GLOBAL TALK>: Please use the player number (on the left column) to identify desired player.; echo; echo;"\n')
        f.write("echo\necho CSGO GLOBAL TALK v" + VERSION + " finished loading!\n")

def verifyMsg(n,l): #name of player saying, the line
#    print("Function: verifyMsg")
    t = "Terrorist) " + n in l
    if t: #remove @ location in alive-team-chat
        loc = l.split(n,1)[1].split(" : ",1)[0]
        l = l.replace(loc,"",1)
    if not n + " : " in l:
        return False
    l = l.split(n + " : ",1)
    print('"' + str(l[0]) + '"')
    if l[0] not in ["*DEAD*(Terrorist) ","*DEAD*(Counter-Terrorist) ","*DEAD* ","(Terrorist) ","(Counter-Terrorist) ",""]: #need to make it nicer
        return False
    else:
        d = "*DEAD*" in l[0]
        return l[1],t,d

def chatPrint(n,msg,team,dead): #name, msg, team (bool), dead (bool)
    print("Function: chatPrint")
    d = ""
    t = ""
    if dead:
        d = cMAGENTA + "*DEAD*"
    if team:
        t = cCYAN + "(TEAM) "
    if msg.startswith(signature):
        #global command
        #command = False not needed because if in echo is "<CSGO GLOBAL TALK>: " then command = False
        d = cGREEN + "[CGT TRANSLATION] " + d #is it neccessary?
        msg = cGREEN + signature + cCYAN + msg[len(signature):]
    elif msg.startswith("<CSGO GLOBAL TALK>: "):
        d = cGREEN + "[CGT OUTPUT] " + d #is it neccessary?
        msg = cGREEN + "<CSGO GLOBAL TALK>: " + cWHITE + msg[20:]
    elif msg.startswith(CMD):
#        if msg[len(CMD):].startswith(("help",CMD2)+tuple(LANGUAGES.keys())):
        d = cGREEN + "[COMMAND] " + d #is it neccessary?
        msg = cGREEN + CMD + cWHITE + msg[len(CMD):]
    cprint(d + t + cYELLOW + n + " : " + cWHITE + msg)

def checkCommands(s,t):
    print("Function: checkCommands")
    s = s[len(CMD):]
    if s.startswith(CMD2): #save player to players database
        s = s[len(CMD2):] #name <lang>
        s = s.split()
        if len(s) == 0:
            warning("Missing argument.",cs=True,t=t)
            return False
        if s[0] not in allPlayers.keys():
            warning("Player not found! (check the player's id number using command 'players' in csgo console)",cs=True,t=t)
            return False
        if len(s) == 1:            
            l = "auto"
        else:
            l = s[1]
            if l not in LANGUAGES.keys():
                warning("Language shortcut '" + l + "' doesn't exist!",cs=True,t=t)
                return False
        n = allPlayers[s[0]]
        ezSend(cGREEN + "Will translate '" + cYELLOW + n + cGREEN + "' from " + cCYAN + LANGUAGES[l].capitalize() + cGREEN + " to " + cCYAN + LANGUAGES[defaultLanguage].capitalize() + cGREEN + ".",t)
        global nameFilter
        nameFilter.append(n)
        global players
        players[n] = l
        return False
    elif s.lower().rstrip() == "help":
        cprint(cGREEN + "Help displayed in csgo console.")
        send("exec cgt_help.cfg\nsay" + t + " <CSGO GLOBAL TALK>: Help displayed in csgo console.")
        return False
    elif s.lower().rstrip() == "players":
        cprint(cGREEN + "Players list displayed in csgo console.")
        send("players\nsay" + t + " <CSGO GLOBAL TALK>: Players list displayed in csgo console.")
        return False
    for i in LANGUAGES.keys():
        if s.startswith(i + " "):
            cprint(cGREEN + "Target Language set to '" + cCYAN + LANGUAGES[i].capitalize() + cGREEN + "'")
            global targetLanguage
            targetLanguage = i
            return s[len(i + " "):]
    return s

def check(l):
#    print("Function: check")
    for n in nameFilter:
        tmp = verifyMsg(n,l)
        if tmp:
            text,team,dead = tmp #it is a chat message (probably)
            chatPrint(n,text,team,dead)
            t = ""
            if team:
                t = "_team"
            if n == name: #if user
                if text.startswith("<CSGO GLOBAL TALK>: ") or text.startswith(signature): #output from send() probably
                    print("That was program generated output")
                    send()
                    return True
                elif not text.startswith(CMD):
                    print("That was a normal chat message by user")
                    return True
                text = checkCommands(text,t)
                if not text:
                    return True
                src = defaultLanguage
                if not targetLanguage:
                    warning("Target language not defined! (translate to what language?)",cs=True,t=t)
                    return True
                tar = targetLanguage
                n = " "
            else:
                src = players[n]
                tar = defaultLanguage
            final = translate(text,src,tar)
            sendTranslate(final,t,n)
            return True
    if l == "<CSGO GLOBAL TALK> : Please use the player number ( on the left column ) to identify desired player. ":
        readPlayers()
    elif l == "Starting Csgo Global Talk... ":
        cprint(cYELLOW + "User typed '" + cCYAN + "exec cgt" + cYELLOW + "' again!")
    else:
        pass
    return True

def follow(f): #https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file
    print("Function: follow")
    f.seek(0,2)
    while True:
        update()
        line = f.readline()
        if not line:
            sleep(0.1)
            continue
        yield line

def main():
    print("Function: main")
    log = open(cfgPath + "csgo_global_talk.cfg","r")
    lines = follow(log)
    for l in lines:
        l = l.rstrip("\n")
        check(l)

#--------------------

def menuGUI():
    print("Function: menuGUI")
    global TOP
    TOP = True
    from Tkinter import Toplevel, Label,StringVar
    from ttk import Button
    #tk = Tk()
    tk = Toplevel()
    tk.iconbitmap(default="cgt.ico")
    tk.title("Csgo Global Talk v" + VERSION + " - Setting")

    def update():
        print("Function: update (in Function: menuGUI)")
        global TOP2
        TOP2 = None #top on this setting window
        csL.set(csgoPath)
        defL.set(LANGUAGES[defaultLanguage].capitalize())
        conL.set(controlKey)

    def close():
        print("Function: close (in Function: menuGUI)")
        global TOP
        TOP = False
        tkClose(tk)

    def topCheck(s):
        print("Function: topCheck (in Function: menuGUI)")
        if TOP2:
            warning("You are changing " + TOP2 + " right now!")
            return True
        else:
            global TOP2
            TOP2 = s
            return False

    def changeCpath():
        print("Function: changeCpath (in Function: menuGUI)")
        if topCheck("CSGO folder path"):
            return
        cpath = askDir("Please select \"Counter-Strike Global Offensive\" folder\n\nIt is located under \"STEAM FOLDER\steamapps\common\Counter-Strike Global Offensive\"")
        if cpath == "":
            print("You did not select any directory!")
        from tkMessageBox import showinfo
        if verifyPath(cpath):
            print("Changing csgoPath")
            conf("Basic","path",cpath)
            update()
            showinfo("Csgo Global Talk v" + VERSION, "Changes to CSGO path were made.\nRestart the program to see the changes.")
        else:
            showinfo("Csgo Global Talk v" + VERSION, "The directory you selected is not valid, therefore no changes were made.")

    def changeDefLang():
        print("Function: changeDefLang (in Function: menuGUI)")
        if topCheck("Default Language"):
            return
        askDefLang()
        conf("Basic","default language",defaultLanguage)
        update()

    def changeKey():
        print("Function: changeKey (in Function: menuGUI)")
        if topCheck("Control Key"):
            return
        askKey()
        conf("Basic","control key",controlKey)
        update()

    csL = StringVar()
    defL = StringVar()
    conL = StringVar()
    update()

    # filler
    Label(tk, text = " ", width = 2).grid(row=0)
    Label(tk, text = " ", width = 2).grid(row=2)
    Label(tk, text = " ", width = 2).grid(row=6)
    #Label(tk, text = " ", width = 2).grid(row=8)
    Label(tk, text = " ", width = 2).grid(column=0)
    Label(tk, text = " ", width = 2).grid(column=3)
    Label(tk, text = " ", width = 2).grid(column=5)

    Label(tk, text = "SETTING", font="Helvetica 12 bold").grid(row=1,columnspan=6)

    #csgo path
    Label(tk, text = "CS:GO folder path: ", font="Helvetica 10 bold").grid(sticky="e",row=3,column=1)
    Label(tk, textvariable = csL, font="Helvetica 10").grid(sticky="w",row=3,column=2)
    Button(tk, text="change", width=10, command=changeCpath).grid(row=3,column=4)

    #Default language
    Label(tk, text = "Default Language: ", font="Helvetica 10 bold").grid(sticky="e",row=4,column=1)
    Label(tk, textvariable = defL, font="Helvetica 10").grid(sticky="w",row=4,column=2)
    Button(tk, text="change", width=10, command=changeDefLang).grid(row=4,column=4)

    #Control key
    Label(tk, text = "Control Key: ", font="Helvetica 10 bold").grid(sticky="e",row=5,column=1)
    Label(tk, textvariable = conL, font="Helvetica 10").grid(sticky="w",row=5,column=2)
    Button(tk, text="change", width=10, command=changeKey).grid(row=5,column=4)

    Button(tk, text="Close", width=15, command=close).grid(row=7,columnspan=6)

    tk.protocol("WM_DELETE_WINDOW", close)
    tk.mainloop()

def shortcut(e):
    print("Function: shortcut")
    if e.state==12 and e.keysym=="c": #http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html ; http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
        print("CTRL+C keypress detected")
        return None
    elif e.keysym=="Escape":
        print("Escape keypress detected")
        if not TOP:
            menuGUI()
        else:
            warning("Setting window is already opened.")
        return "break"
    else:
        #print e.state
        return "break"

def mainGUI():
    print("Function: mainGUI")
    global tk
    tk = Tk()
    tk.geometry("880x495")
    tk.title("Csgo Global Talk v" + VERSION)
    tk.iconbitmap(default="cgt.ico")

    global console
    console = Text(bg="black")
    console.pack(fill="both", expand=1, side="left") #expand=1 is expand=YES
    console.config(font=("consolas", 11), wrap="word")
    #console.configure(state="disabled")
    console.bind("<Key>", shortcut) #function shortcut(), alternative: to 'shortcut' is 'lambda e: shortcut(e)'

    scroll = Scrollbar(command=console.yview)
    scroll.pack(fill='y', expand=0, side="left") #expand=0 is expand=NO
    #scroll.grid(column=1)
    console["yscrollcommand"] = scroll.set

    #colors
    console.tag_configure("31m", foreground="red")
    console.tag_configure("32m", foreground="green")
    console.tag_configure("33m", foreground="yellow")
    console.tag_configure("34m", foreground="blue")
    console.tag_configure("35m", foreground="magenta")
    console.tag_configure("36m", foreground="cyan")
    console.tag_configure("37m", foreground="white")

    tk.after(1000,initial)

    tk.protocol("WM_DELETE_WINDOW", close) #global close() function
    tk.mainloop()

def initial():
    print("Function: initial")
    #logo & keybinds
    global logo
    logo = [cRED + " -------------------------------------------------------------------",cRED + " |" + cGREEN + "                                                                 " + cRED + "|",cRED + " |" + cGREEN + "  _____                                                       " + cWHITE + " ) " + cRED + "|",cRED + " |" + cGREEN + " /__   \_   _ _______ _ __ ___  _ __                          " + cWHITE + "(  " + cRED + "|",cRED + " |" + cGREEN + "   / /\/ | | |_  / _ \ '__/ _ \| '_ \  " + cYELLOW + "  ,___________  ______ " + cWHITE + " )  ",cRED + " |" + cGREEN + "  / /  | |_| |/ /  __/ | | (_) | | | | " + cYELLOW + " /_///_______(=(_____()    ",cRED + " |" + cGREEN + "  \/    \__, /___\___|_|  \___/|_| |_| " + cYELLOW + "  /  (')  L_O              ",cRED + " |" + cGREEN + "        |___/                          " + cYELLOW + " /__/                     " + cRED + "|",cRED + " |" + cGREEN + "                                                                 " + cRED + "|",cRED + " |" + cCYAN + "    ___               _            _   _                         " + cRED + "|",cRED + " |" + cCYAN + "   / _ \_ __ ___   __| |_   _  ___| |_(_) ___  _ __              " + cRED + "|",cRED + " |" + cCYAN + "  / /_)/ '__/ _ \ / _` | | | |/ __| __| |/ _ \| '_ \             " + cRED + "|",cRED + " |" + cCYAN + " / ___/| | | (_) | (_| | |_| | (__| |_| | (_) | | | |            " + cRED + "|",cRED + " |" + cCYAN + " \/    |_|  \___/ \__,_|\__,_|\___|\__|_|\___/|_| |_|            " + cRED + "|",cRED + " |" + cCYAN + "                                                                 " + cRED + "|",cRED + " -------------------------------------------------------------------      --  -"]
    for i in logo:
        cprint(i)
    global logo2
    logo2=[cYELLOW + "",cYELLOW + "                      ____ ____   ____  ___   ",cYELLOW + "                     / ___/ ___| / ___|/ _ \  ",cYELLOW + "                    | |   \___ \| |  _| | | | ",cYELLOW + "                    | |___ ___) | |_| | |_| | ",cYELLOW + "                     \____|____/ \____|\___/  ","",cGREEN + "   ____ _     ___  ____    _    _      " + cWHITE + " _____  _    _     _  __ ",cGREEN + "  / ___| |   / _ \| __ )  / \  | |     " + cWHITE + "|_   _|/ \  | |   | |/ / ",cGREEN + " | |  _| |  | | | |  _ \ / _ \ | |     " + cWHITE + "  | | / _ \ | |   | ' /  ",cGREEN + " | |_| | |__| |_| | |_) / ___ \| |___  " + cWHITE + "  | |/ ___ \| |___| . \  ",cGREEN + "  \____|_____\___/|____/_/   \_\_____| " + cWHITE + "  |_/_/   \_\_____|_|\_\ ","",cRED + " " + "-"*63]
    global keyBinds
    keyBinds = keyDictionary.keys()
    cprint(cYELLOW + "\nWelcome to " + cCYAN + "CSGO GLOBAL TALK " + cRED + "v" + VERSION + cYELLOW + " created by " + cCYAN + "Tyzeron\n")

    #OS check
    if sys.platform == "win32":
        cprint(cGREEN + "Compatible operating system detected")
    else:
        warning("Potentionally incompatible operating system (" + sys.platform + ")")

    checkVer()

    #pre-defined GLOBAL variables
#    global customDebug
#    customDebug = False
    global CMD
    CMD = "!t "
    global CMD2
    CMD2 = "save " #next is player name, player to track
    global signature
    signature = "<CGT TRANSLATION> "
    global translator
    translator = Translator()
    global targetLanguage
    targetLanguage = False
    #global command #not neccessary
    #command = False #not neccessary
    global players #name and language
    players = {}
    global allPlayers #identification number and name
    allPlayers = {}
    global TOP
    TOP = False #if menuGUI is open
    
    #generated GLOBAL variables
    global csgoPath
    csgoPath = getCpath()
    global cfgPath
    cfgPath = csgoPath + "\\csgo\\cfg\\"
    cprint(cYELLOW + "CSGO Path: " + cCYAN + csgoPath)
    getDefLang()
    cprint(cYELLOW + "Default Language: " + cCYAN + LANGUAGES[defaultLanguage].capitalize())
    getKey()
    cprint(cYELLOW + "Control Key: " + cCYAN + controlKey)

    #start functions
    setup()
    waitExec()
    send()#cgt_command.cfg
    for i in logo2:
        cprint(i)

    #get, save and use user csgo name
    global name
    name = getName()
    cprint(cYELLOW + "Your CSGO name: " + cCYAN + name)
    global nameFilter
    nameFilter = [name]

    writeHelp()#cgt_help.cfg

    #finally main function
    main()

def getStuff(u,t):
    print("Function: getStuff")
    try:
        d = get(u).text
    except Exception as e:
        print "IGNORE: " + str(e)
        warning("Could not check the program " + t + ".")
        return False
    if "error" in d.lower():
        warning("There was an error when checking the program " + t + ".")
        print("-"*14 + " [RESPONSE] " + "-"*14)
        print d
        print("-"*40)
        return False
    return d

def checkVer():
    print("Function: checkVer")
    cprint(cYELLOW + "Checking updates...")
    new = getStuff("http://bit.ly/2CjqHMi","newest version")
    if not new:
        return
    v = tuple(map(int,VERSION.split(".")))
    try:
        n = tuple(map(int,new.split(".")))
        if len(n) != 3:
            raise ValueError
    except:
        warning("Newest version number is not readable!")

    if v != n:
        if v < n:
            url = getStuff("http://bit.ly/2CiS5tD","website url")
            if not url:
                url = "http://bit.ly/2zVPUq0"
            if v[0] != n[0]:
                print("MAJOR RELEASE")
                from tkMessageBox import askokcancel
                if askokcancel("Csgo Global Talk v" + VERSION + " - Major Update", "There is a new significant update which is mandatory!\nDo you want to download it now?"):
                    print("Open browser on URL: " + url)
                    try:
                        if sys.platform=='win32':
                            os.startfile(url)
                        elif sys.platform=='darwin':
                            from subprocess import Popen
                            Popen(['open', url])
                        else:
                            from webbrowser import open_new_tab
                            open_new_tab(url)
                    except Exception as e:
                        print "IGNORE: " + str(e)
                error("The program is out-of-date!\nPlease update it to the latest version!\nYou can download the latest version here: " + cCYAN + url)
            elif v[1] != n[1]:
                print("MINOR RELEASE")
                cprint(cYELLOW + "This program has a newer version: " + cCYAN + new + cYELLOW + " available.\nYou can download the latest version here: " + cCYAN + url)
            else:
                print("PATCH")
                cprint(cYELLOW + "This program has a new small patch: " + cCYAN + new + cYELLOW + " available on the official website.")
        else:
            print("WTF? This program WILL be released in the FUTURE!? :D")
            warning("WTF?? You have a FUTURE release?\nThis program is " + cCYAN + "v" + VERSION + cRED + " even though the newest version is " + cCYAN + "v" + new + cRED + "!")
    else:
        print("Program Up-To-Date!")
        cprint(cGREEN + "You have the latest up-to-date version (" + cCYAN + VERSION + cGREEN + ")!")

if __name__ == "__main__":
    global VERSION
    VERSION = "0.1.0"
    os.system("title Csgo Global Talk v" + VERSION)

    print "-"*80
    print "Csgo Global Talk v" + VERSION + "  Copyright (C) 2018  Tyzeron"
    print "This program comes with ABSOLUTELY NO WARRANTY."
    print "This is free software, and you are welcome to redistribute it"
    print "under certain conditions."
    print "-"*80
    print ""

    #colors
    global cRED, cGREEN, cYELLOW, cBLUE, cMAGENTA, cCYAN, cWHITE
    cRED = "[31m"
    cGREEN = "[32m"
    cYELLOW = "[33m"
    cBLUE = "[34m"
    cMAGENTA = "[35m"
    cCYAN = "[36m"
    cWHITE = "[37m"
    #init()
    #cprint(cYELLOW + Style.BRIGHT + "")

    if not os.path.isfile(path() + "\\cgt.ico"):
        print("Missing ICON!!!")
        from tkMessageBox import showerror
        tk = Tk()
        tk.withdraw() #use to hide tkinter window
        showerror("Csgo Global Talk v" + VERSION + " - Error","Missing cgt.ico! Please re-download or check for missing file!")
        tk.deiconify() #use to show back tkinter window, without this future tkinter is not working
        tk.destroy()
        tk.quit()
        raise SystemExit

    mainGUI()
    raise SystemExit
