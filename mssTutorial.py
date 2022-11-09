import cv2
import mss
import numpy as np

with mss.mss() as sct:#starts mss
    while 'Screen capturing':
        monitor_1 = sct.monitors[1]#monitor_1 represents screen monitor
        sct_img = np.array(sct.grab(monitor_1))#grabs input from screen
        img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)#converts screen input to BGR format
        h = img.shape[0]#get height of image
        w = img.shape[1]#get width of image
        img=cv2.resize(img, (int(w/2),int(h/2)))#resize image so it won't take up a huge portion of the screen
        cv2.imshow('img',img)# show img on window named 'img'
        k=cv2.waitKey(27) & 0xff# checks for key press
        if k==ord('q'):# if key pressed is q, exit
            break
cv2.destroyAllWindow()