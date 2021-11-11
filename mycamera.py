#!/usr/bin/python3

from gpiozero import MotionSensor
import time
import picamera
import os
import subprocess

try:
    pir = MotionSensor(4)
    os.chdir('/motion')
    while True:
        files = [x[14:-5] for x in os.listdir('/motion/') if 'motion_capture' in x]
#    print(files)
        if files == []:
            newfile = 'motion_capture0.h264'
        else:
            files = [int(x) for x in files]
            newfile = 'motion_capture' + str((int(max(files)) + 1)) + '.h264'
        fsize = sorted([x for x in os.listdir('/motion/') if 'motion_capture' in x], key=os.path.getctime, reverse=True)
        if len(fsize) > 3:
            while len(fsize) > 3:
                os.remove('/motion/' + fsize.pop())
               # print(fsize) 
        #print(newfile)
        pir.wait_for_motion()
        print('motion!')
        camera = picamera.PiCamera(resolution=(1024, 768))
   #    print(os.getcwd())
        camera.start_preview()
        time.sleep(1)
        camera.start_recording(newfile, format='h264')
        camera.wait_recording(7)
        camera.stop_recording()
        camera.close()
        subprocess.call(['python /motion/upload_video.py --file="/motion/{a}"  --title="{b}" --description="{c}" --keywords="{d}" --privacyStatus="private" --noauth_local_webserver'.format(a=newfile, b=newfile[:-5], c=newfile[:-5], d='Home')], shell=True)
        print('uploded')
        subprocess.call(['python3 /motion/mailme.py'], shell=True)
        time.sleep(2)
except Exception as a:
    print(str(a))
    print('something went wrong')

