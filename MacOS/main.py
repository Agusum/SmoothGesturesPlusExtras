#!/usr/bin/python

import sys
import os
import stat
import re
from Tkinter import *

if not re.search("^/Application", os.path.abspath(__file__)):
  parts = os.path.abspath(__file__).split(".app")
  app = parts[0]+".app"
  os.system("""osascript -e 'do shell script "cp -r \\"%s\\" /Applications/; open /Applications/SmoothGesturesPlusExtras.app" with administrator privileges'""" % app)
  sys.exit()

installdir = '/Library/Google/Chrome/NativeMessagingHosts'
hostname = 'com.smoothgesturesplus.extras'
path = os.path.dirname(os.path.abspath(__file__))+"/sgplus-extras.py"
src = "/tmp/"+hostname+".json"
dest = installdir+"/"+hostname+".json"
manifest = '{"name":"'+hostname+'", "description":"Extra Functionality for Smooth Gestures Plus", "path":"'+path+'", "type":"stdio", "allowed_origins":["chrome-extension://kdcjmllhmhnnadianfhhnoefgcdbpdap/","chrome-extension://ncnbcopaicobijamiljeamdkpplfokaj/","chrome-extension://ijgdgeacmjiigjjepffiijkleklaapfl/"]}'

root = Tk()
stateString = StringVar()

def InstallNative():
  f = open(src, "w")
  f.write(manifest)
  f.close()
  os.system("""osascript -e 'do shell script "mkdir -p %s; mv %s %s; chmod o+r %s" with administrator privileges'""" % (installdir, src, dest, dest))
  CheckInstallNative()

def CheckInstallNative():
  content = ""
  try:
    f = open(dest, "r")
    content = f.read()
  except:
    pass
  installed = content == manifest
  if installed:
    stateString.set("Smooth Gestures Plus Extras IS INSTALLED")
  else:
    stateString.set("Smooth Gestures Plus Extras is NOT INSTALLED")
  return installed

def UninstallNative():
  os.system("""osascript -e 'do shell script "rm %s" with administrator privileges'""" % (dest))
  CheckInstallNative()

#if not CheckInstallNative():
#  InstallNative()
#CheckInstallNative()


#build window
root.title("Smooth Gestures Plus Extras")
root.geometry("500x200")
app = Frame(root)
app.pack(fill='both')

lbl = Label(app, textvariable=stateString, font=("sans-serif", 16, "bold"))
lbl.pack(pady=40)

bttns = Frame(app)
bttns.pack()

bttn1 = Button(bttns, text="Install", font=("sans-serif", 16, "normal"), command=InstallNative)
bttn1.pack(pady=5)

bttn2 = Button(bttns, text="Uninstall", font=("sans-serif", 10, "normal"), command=UninstallNative)
bttn2.pack(pady=5)


if not CheckInstallNative():
  InstallNative()


root.update()
root.tkraise()
root.mainloop()




