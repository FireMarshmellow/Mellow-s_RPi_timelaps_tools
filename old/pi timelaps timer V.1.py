import datetime
from picamera import PiCamera
from time import sleep
import tkinter as tk
from time import sleep
import RPi.GPIO as GPIO
root = tk.Tk()
root.title("pi laps")
camera = PiCamera()
current_time = datetime.datetime.now()
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)


def folder1():
    camera.start_preview(fullscreen=False,window=(200,300,400,500))


def Run():
    camera.stop_preview()
    for _ in range(10000):
        folder_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        howers = datetime.datetime.now().strftime("%H")
        if howers >= "06" and howers <= "20":
            print (howers)
            print("im working")
            camera.resolution = (2592, 1944)
            camera.framerate = 15
            camera.capture('/home/pi/Desktop/New/'+(folder_time)+'TimeLaps.jpg')
            sleep(5)
        else:
            print("not with in time")
            sleep(60)


Button1 = tk.Button(root, text="start preview",activeforeground="blue", height=5, width=20, command=folder1())
Button1.pack()
Button3 = tk.Button(root, text="Run time laps",activeforeground="green", height=5, width=20, command=Run )
Button3.pack()

root.mainloop()