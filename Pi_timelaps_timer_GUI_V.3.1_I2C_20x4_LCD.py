import datetime
from picamera import PiCamera
from time import sleep
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import threading
import smbus
import time,os
import shutil

start=datetime.datetime.now()

I2C_ADDR  = 0x27
LCD_WIDTH = 20 
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4
LCD_BACKLIGHT  = 0x08
ENABLE = 0b00000100
E_PULSE = 0.0005
E_DELAY = 0.0005
bus = smbus.SMBus(1)
def lcd_init():
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  lcd_init()

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)

root = tk.Tk()
root.title("Pi Timelaps Timer V3.1 beta")
camera = PiCamera()
 

def folder1():
    global folder_selected1
    folder_selected1 = filedialog.askdirectory()

def changeText1():  
    outFolder['text'] = folder_selected1

def startpreview():
    camera.resolution = (2592, 1944)
    camera.framerate = 15
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
            total, used, free = shutil.disk_usage(folder_selected1)
            storagInProsent = total // (2**30)/(used //(2**30))
            NomOfItemsInFolder = os.listdir(folder_selected1)
            
            lcd_string("Photos taken:"+str(len(NomOfItemsInFolder)),LCD_LINE_1)
            lcd_string("Storage:"+str(int(storagInProsent))+"%",LCD_LINE_2)
            lcd_string("Interval:"+str(AllinS)+"s "+str(a)+'-'+str(b) ,LCD_LINE_3)
            lcd_string("Run time:"+ str(datetime.datetime.now()-start),LCD_LINE_4)

            sleep(AllinS)
        else:
            lcd_string("Storage:"+str(int(storagInProsent))+"%",LCD_LINE_1)
            lcd_string("Not with in time",LCD_LINE_2)
            lcd_string("back at "+str(a) ,LCD_LINE_3)
            lcd_string("Run time:"+ str(datetime.datetime.now()-start),LCD_LINE_4)
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