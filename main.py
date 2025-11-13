import mediapipe as mp
import math
import cv2


class handmaker():
    def __init__(self, maxhands):
        self.mphand= mp.solutions.hands
        self.maxhand=maxhands
        self.hand= self.mphand.Hands(max_num_hands= self.maxhand,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9,
    model_complexity=1)
        self.drawing= mp.solutions.drawing_utils
        self.fintip=[4, 8, 12, 16, 20]

    def finhan(self,frame):

        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.result= self.hand.process(frame)
        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                    self.drawing.draw_landmarks(frame, hand,self.mphand.HAND_CONNECTIONS)
        return frame
    
    def pos(self, frame):
        x,y,lms_list= [],[],[]
        if self.result.multi_hand_landmarks:
            for id, lm in enumerate(self.result.multi_hand_landmarks[0].landmark):
                hig,wid,col=frame.shape
                cx, cy= int(lm.x*wid), int(lm.y*hig)
                x.append(cx)
                y.append(cy)
                lms_list.append([id,cx,cy])
            xmin, xmax= min(x), max(x)
            ymin, ymax= min(y), max(y)
            cv2.rectangle(frame,(xmin-30,ymin-30),(xmax+30,ymax+30),(0,255,0),2)
        return lms_list
    
    def fingup(self, lms):
        fingers=[]
        if lms:
            if lms[self.fintip[0]][1]<lms[self.fintip[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lms[self.fintip[id]][2]<lms[self.fintip[id]-1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers
    
    def dist(self, p1, p2, lms, frame): 
        x1,y1= lms[p1][1], lms[p1][2]
        x2,y2= lms[p2][1], lms[p2][2]
        length= math.hypot(x2 - x1, y2 - y1)
        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
        return length

                
