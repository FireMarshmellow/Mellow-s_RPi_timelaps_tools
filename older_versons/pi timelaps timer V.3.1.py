import datetime
from picamera import PiCamera
from time import sleep
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import threading

root = tk.Tk()
root.title("Pi Timelaps Timer V3.1 beta")
camera = PiCamera()
 

def folder1():
    global folder_selected1
    folder_selected1 = filedialog.askdirectory()

def changeText1():  
    outFolder['text'] = folder_selected1

def startpreview():
    camera.start_preview(fullscreen=False,window=(200,300,400,500))
    print('preview started')

def Stopreview():
    camera.stop_preview()
    print('preview stoped')

def switchon():  
 global switch
 switch = True
 print ('Timelaps Started' )
 starttimelaps()  
      
def switchoff():  
 print ('Timelaps Stoped')
 global switch
 switch = False    
      
def kill():  
 root.destroy()  

StartTime = IntVar()
StartTime = Spinbox(root, width = 9, values=('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'))

StopTime = IntVar()
StopTime = Spinbox(root, width = 9, values=('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'))

Hour = Spinbox(root, width=5, from_=0, to=24)
minute = Spinbox(root, width = 5, from_=0, to=60)
second = Spinbox(root, width = 5, from_=0, to=60)

def starttimelaps():
 def Run():
    while (switch == True):
        HinS = int(Hour.get())*3600
        MinS = int(minute.get())*60
        Sinint = int(second.get())
        AllinS = MinS + HinS + Sinint
        time = datetime.datetime.now().strftime("%H")
        a=StartTime.get()
        b=StopTime.get()
        if time >= b and time <= a:
            print ('Time',datetime.datetime.now().strftime("%H-%M-%S"))
            print("Photo taken")
            print('interval in secands',AllinS)
            camera.resolution = (2592, 1944)
            camera.framerate = 15
            ImgNameWithTime="Timelaps " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            camera.capture(folder_selected1 +"/"+ ImgNameWithTime +".jpg")
            sleep(AllinS)
        else:
            print("Not within time range")
            sleep(120)
            
        if switch == False:
            break

 thread = threading.Thread(target=Run)
 thread.start()

startpreview = tk.Button(root, height=3, width=15, text="Start preview",command=startpreview)
Stopreview = tk.Button(root, height=3, width=15, text="Stop preview",command=Stopreview)
folderLabel = Label(root, text="Select folder for output")
timestarsLabel = Label(root, text="Set Start/Stop time (24H)")
onbutton = tk.Button(root, height=3, width=15, text = "Start Timelape", command = switchon)
offbutton =  tk.Button(root, height=3, width=15,  text = "Stop Timelaps", command = switchoff)
killbutton = tk.Button(root, height=3, width=15, text = "EXIT", command = kill)

hourlabel = Label(root, text="Hours")
minlabel = Label(root, text="Minuts")
seclabel = Label(root, text="Secands")
intvalabel = Label(root, text="Set interval")
emptylabel = Label(root, text="            ")
SSlabel = Label(root, text="<start        /        stop>")

outFolder = tk.Button(root, height=3, width=15, text="Select out folder", command=lambda : [folder1(),changeText1()])

folderLabel.grid(row=1,column=1,)
outFolder.grid(row=2,column=1)

emptylabel.grid(row=3,column=1)

timestarsLabel.grid(row=4,column=1)
StopTime.grid(row=5,column=0)
SSlabel.grid(row=5,column=1)
StartTime.grid(row=5,column=2)

intvalabel.grid(row=6,column=1)

hourlabel.grid(row=7,column=0)
Hour.grid(row=8,column=0)


minlabel.grid(row=7,column=1)
minute.grid(row=8,column=1)


seclabel.grid(row=7,column=2)
second.grid(row=8,column=2)

emptylabel.grid(row=9,column=1)

startpreview.grid(row=10,column=0)
Stopreview.grid(row=10,column=2)


onbutton.grid(row=11,column=0)
offbutton.grid(row=11,column=2)


killbutton.grid(row=12,column=1)

root.mainloop()