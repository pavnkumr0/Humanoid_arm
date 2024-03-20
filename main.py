'''
{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
{}    /$$   /$$                                                       /$$       /$$   {}
{}   | $$  | $$                                                      |__/      | $$   {}   
{}   | $$  | $$ /$$   /$$ /$$$$$$/$$$$   /$$$$$$  /$$$$$$$   /$$$$$$  /$$  /$$$$$$$   {}
{}   | $$$$$$$$| $$  | $$| $$_  $$_  $$ |____  $$| $$__  $$ /$$__  $$| $$ /$$__  $$   {}
{}   | $$__  $$| $$  | $$| $$ \ $$ \ $$  /$$$$$$$| $$  \ $$| $$  \ $$| $$| $$  | $$   {}
{}   | $$  | $$| $$  | $$| $$ | $$ | $$ /$$__  $$| $$  | $$| $$  | $$| $$| $$  | $$   {}
{}   | $$  | $$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$  | $$|  $$$$$$/| $$|  $$$$$$$   {}
{}   |__/  |__/ \______/ |__/ |__/ |__/ \_______/|__/  |__/ \______/ |__/ \_______/   {}
{}                                                                                    {}
{}                                                                                    {}
{}                                                                                    {}
{}                        /$$$$$$   /$$$$$$  /$$$$$$/$$$$                             {}
{}                       |____  $$ /$$__  $$| $$_  $$_  $$                            {}
{}                        /$$$$$$$| $$  \__/| $$ \ $$ \ $$                            {}
{}                       /$$__  $$| $$      | $$ | $$ | $$                            {}
{}                      |  $$$$$$$| $$      | $$ | $$ | $$                            {}
{}                       \_______/|__/      |__/ |__/ |__/                            {}
{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
'''

import pyfirmata
import cv2
import mediapipe as mp

port = "COM7"  ## change the COM port
board = pyfirmata.Arduino(port)
servo_thumb = board.get_pin('d:3:s') #pin 3 Arduino
servo_index = board.get_pin('d:4:s') #pin 4 Arduino
servo_middle = board.get_pin('d:5:s') #pin 5 Arduino
servo_ring = board.get_pin('d:6:s') #pin 6 Arduino
servo_little = board.get_pin('d:7:s') #pin 7 Arduino

servo_max = 90  # change the maximum angle that the servo must rotate
servo_min = 0   #rest angle of the servo


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read frame from camera")
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandmarks = results.multi_hand_landmarks


    if multiLandmarks:
        handPoints = []
        for hand_lms in multiLandmarks:
            mpDraw.draw_landmarks(img, hand_lms, mpHands.HAND_CONNECTIONS)

            for idx,lm in enumerate(hand_lms.landmark):
                # print(idx,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                # print(cx,cy)
                handPoints.append((cx,cy))

        for points in handPoints:
            cv2.circle(img, points ,10,(0,0,255),cv2.FILLED)

        fingerState = [0,0,0,0,0]

        if handPoints[8][1] <  handPoints[6][1]:
            fingerState[0] = 1
            servo_index.write(servo_max)
        else: 
            servo_index.write(servo_min)

        if handPoints[12][1] < handPoints[10][1]:
            fingerState[1] = 1
            servo_middle.write(servo_max)
        else:
            servo_middle.write(servo_min)

        if handPoints[16][1] < handPoints[14][1]:
            fingerState[2] = 1
            servo_ring.write(servo_max)
        else: 
            servo_ring.write(servo_min)

        if handPoints[20][1] < handPoints[18][1]:
            fingerState[3] = 1
            servo_little.write(servo_max)
        else: 
            servo_little.write(servo_min)

        if handPoints[4][0] > handPoints[2][0]:
            fingerState[4] = 1
            servo_thumb.write(servo_max)
        else:
            servo_thumb.write(servo_min)
        


        print(fingerState)


    cv2.imshow("Fingers", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



'''
▄▄▄▄·  ▄· ▄▌     ▄▄▄· ▄▄▄·  ▌ ▐· ▄▄▄·  ▐ ▄ 
▐█ ▀█▪▐█▪██▌    ▐█ ▄█▐█ ▀█ ▪█·█▌▐█ ▀█ •█▌▐█
▐█▀▀█▄▐█▌▐█▪     ██▀·▄█▀▀█ ▐█▐█•▄█▀▀█ ▐█▐▐▌
██▄▪▐█ ▐█▀·.    ▐█▪·•▐█ ▪▐▌ ███ ▐█ ▪▐▌██▐█▌
·▀▀▀▀   ▀ •     .▀    ▀  ▀ . ▀   ▀  ▀ ▀▀ █▪

'''