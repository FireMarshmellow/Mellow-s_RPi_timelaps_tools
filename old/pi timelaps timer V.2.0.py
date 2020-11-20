import datetime
from picamera import PiCamera
from time import sleep
from tkinter import *
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.title("pi laps")
camera = PiCamera()

def folder1():
    global folder_selected1
    folder_selected1 = filedialog.askdirectory()

def changeText1():  
    outFolder['text'] = folder_selected1

def startpreview():
    camera.start_preview(fullscreen=False,window=(200,300,400,500))

StartTime = IntVar()
StartTime = Spinbox(root, width = 5, values=('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'))

StopTime = IntVar()
StopTime = Spinbox(root, width = 5, values=('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'))


def RunTimelaps():
    camera.stop_preview()
    for _ in range(10000):
        howers = datetime.datetime.now().strftime("%H")
        a=StartTime.get()
        b=StopTime.get()
        if howers >= b and howers <= a:
            print (howers)
            print("im working")
            camera.resolution = (2592, 1944)
            camera.framerate = 15
            ImgNameWithTime="Timelaps " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            camera.capture(folder_selected1 +"/"+ ImgNameWithTime +".jpg")
            sleep(5)
        else:
            print("not with in time")


startpreview = tk.Button(root, text="Start preview",command=startpreview)
folderLabel = Label(root, text="Select folder for output")
timestarsLabel = Label(root, text="Time for timelaps to Start (24H)")
timeStopLabel = Label(root, text="Time for timelaps to Stop (24H)")

RunTimelaps = tk.Button(root, text="Start timelaps",command=RunTimelaps)


outFolder = tk.Button(root, text="Select out folder", command=lambda : [folder1(),changeText1()])

folderLabel.pack()
outFolder.pack()
timestarsLabel.pack()
StopTime.pack()
timeStopLabel.pack()
StartTime.pack()
startpreview.pack()
RunTimelaps.pack()

root.mainloop()