import datetime
from picamera import PiCamera
from time import sleep

camera = PiCamera()
print('project name')
name = input()
print('where to save:')
save_path = input()
print('intaval in sec:')
interval = int(input())
print('time to start: 24 hour')
start_time = input()
print('time to stop: 24 hour')
stop_time = input()
print('resulushan: 720-0,1080-1,full-2')
resolution = input()
print("ready to start? yes-y")
start = input()

if resolution == "0":
    size = 1280, 720
if resolution == "1":
    size = 1920, 1080
if resolution == "2":
    size = 2592, 1944


def sumary():
    print('project name: ', name)
    print('save path: ', save_path)
    print('the resolution it: ', size)
    print('the interval it: ', interval)
    print('start time: ', start_time)
    print('stop time:', stop_time)
    pass


def capture():
    while True:
        courent_hour = datetime.datetime.now().strftime("%H")
        if courent_hour <= stop_time and courent_hour >= start_time:
            sleep(interval)
            print("i take a pic")
            ImgNameWithTime = name + '-' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            camera.resolution = (size)
            camera.framerate = 15
            camera.capture(save_path + "/" + ImgNameWithTime + ".jpg")
        else:
            print("not within time frame")
            print('will start at: ',
                  start_time)
            sleep(60)


if start == "y":
    sumary()
    capture()
