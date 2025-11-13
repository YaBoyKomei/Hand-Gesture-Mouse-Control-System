import main as m
import cv2
import time
import numpy as np
from pynput.mouse import Controller, Button
import pyautogui as pg
from threading import Thread

mouse= Controller()
fintip=[4, 8, 12, 16, 20]
sw, sh= pg.size()
detector=m.handmaker(maxhands=1)

class VideoStream:
    def __init__(self, src=0):
        self.stream=cv2.VideoCapture(src)
        self.size= self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.height= self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.fps=self.stream.set(cv2.CAP_PROP_FPS, 144)
        self.buffer=self.stream.set(cv2.CAP_PROP_BUFFERSIZE,1)
        self.success, self.frame= self.stream.read()

    def start(self):
        self.t=Thread(target=self.update, args=())
        self.t.start()
        return self
    def update(self):
        while True:
            if not self.success:
                self.stop()
            else:
                self.success, self.frame= self.stream.read()
    def read(self):
        return self.frame
    def stop(self):
        self.t.join()
        self.stream.release()
        cv2.destroyAllWindows()
    
vs= VideoStream(src=0).start()
px, py=0,0
smooch=5
fliper= False
while True:
    try:
        frame= vs.read()
        frame= cv2.flip(frame,1)
        frame= detector.finhan(frame)
        lms= detector.pos(frame)
        if len(lms)!=0:
            fingers= detector.fingup(lms)
            print(fingers)   
            if fingers !=[]:
                if fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
                    x,y = lms[fintip[1]][1], lms[fintip[1]][2]
                    x1 = np.interp(x,(50,590),(0,sw))
                    y1 = np.interp(y,(100,370),(0,sh))
                    cx= px + (x1-px)//smooch
                    cy= py + (y1-py)//smooch
                    mouse.position= (cx,cy)
                    px, py= cx, cy
                    cv2.circle(frame,(x,y),10,(255,0,255),cv2.FILLED)
                elif fingers[1]==1 and fingers[2]==0 and fingers[0]==0 and fingers[3]==0 and fingers[4]==1:
                    dist=detector.dist(fintip[1],fintip[2],lms,frame)
                    if dist<150:
                        mouse.click(Button.left,1)
                        time.sleep(0.5)
                elif fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1: 
                    p,q= lms[fintip[0]][1], lms[fintip[0]][2]
                    for i in fintip:
                        id,x,y=lms[i]
                        cv2.circle(frame,(x,y),5,(0,255,0),2)
                        cv2.line(frame,(p,q),(x,y),(0,255,0),2)
                        p,q=x,y


                    ph= lms[fintip[0]][2]
                    d=480//2-30
                    d1=480//2+30
                    if ph<d:
                        speed=abs(d-ph)
                        pg.scroll(40+speed)
                    elif ph>d1:
                        speed=ph-d1
                        pg.scroll(-40-speed)
                    
                elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
                    dist= detector.dist(fintip[2],fintip[3],lms,frame)
                    if dist<90:
                        mouse.click(Button.right,1)
                        time.sleep(0.5)
                elif fingers[0]==0 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 and fingers[1]==1:
                    dist=detector.dist(fintip[1],fintip[2],lms,frame)
                    dist1=detector.dist(fintip[3],fintip[4],lms,frame)
                    dist2=detector.dist(fintip[2],fintip[3],lms,frame)
                    if dist<30:
                        if fliper!=True:
                            mouse.press(Button.left)
                            fliper= True
                        x,y = lms[fintip[1]][1], lms[fintip[1]][2]
                        x1 = np.interp(x,(50,590),(0,sw))
                        y1 = np.interp(y,(100,370),(0,sh))
                        cx= px + (x1-px)//smooch
                        cy= py + (y1-py)//smooch
                        mouse.position= (cx,cy)
                        px, py= cx, cy
                    elif dist1>30:
                        if fliper==True:
                            fliper= False
                            mouse.release(Button.left)
                        x,y = lms[fintip[1]][1], lms[fintip[1]][2]
                        x1 = np.interp(x,(50,590),(0,sw))
                        y1 = np.interp(y,(100,370),(0,sh))
                        cx= px + (x1-px)//smooch
                        cy= py + (y1-py)//smooch
                        mouse.position= (cx,cy)
                        px, py= cx, cy
        frame= cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        cv2.imshow("Hand Gesture Control",frame)
        if cv2.waitKey(2) & 0xFF== ord('q'):
            vs.stop()
            break
    except KeyboardInterrupt:
       vs.stop()
       break
    

     


