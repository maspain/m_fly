from asyncore import read
import cv2
import numpy as np
import mss

def stackImages(scale,imgArray,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

#alternative to cv2 trackbar. Basically allows you to change certain values of any array
def showValues(img,valNames, valRanges,vals,option):
    i=0
    cv2.putText(img, str(option[0]), (20,100),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
    for x in valNames:
        isOption=" "
        if(i==option[0]):
            isOption="#"
            k = cv2.waitKey(1) & 0xff
            if k == ord('w') and option[0]>0:
                option[0]-=1
            elif k == ord('s') and option[0]<len(valNames)-1:
                option[0]+=1
            elif k == ord('a') and vals[i]>valRanges[i][0]:
                vals[i]-=1
            elif k == ord('d') and vals[i]<valRanges[i][1]:
                vals[i]+=1
        a=valRanges[i][0]
        b=valRanges[i][1]
        cv2.putText(img, isOption+x+" "+str(a)+" - "+str(vals[i])+" - "+str(b), (20, (i+1)*20 + 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
        i+=1
        
def mss_screencap():
    with mss.mss() as sct:#starts mss
        while 'Screen capturing':
            monitor_1 = sct.monitors[1]#monitor_1 represents screen monitor
            sct_img = np.array(sct.grab(monitor_1))#grabs input from screen
            img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)#converts screen input to BGR format
            h = img.shape[0] #get height of image
            w = img.shape[1] #get width of image
            img=cv2.resize(img, (int(w/2),int(h/2)))#resize image so it won't take up a huge portion of the screen
            cv2.imshow('img',img) # show img on window named 'img'
            k=cv2.waitKey(27) & 0xff# checks for key press
            if k==ord('q'):# if key pressed is q, exit
                break
    cv2.destroyAllWindows()

def color_detect():
    cap = cv2.VideoCapture(0)
    
    names = ["hue1", "sat1", "value1", "hue2", "sat2", "value2"]
    values = [40, 0, 0, 50, 255, 255]
    ranges =[[0, 100], [0, 255], [0, 255], [0, 100], [0, 255], [0, 255]]
    option = [0]
    
    lowerbound = np.array([50, 30, 30])
    upperbound = np.array([80, 255, 255])
    # hue range is 0 -180
    # sat range is 0 -255
    # 0 is dark max is light

    # maybe values hue 7 - 21; sat 100 - 255; val 100 - 255
    names = ["hue1", "sat1", "value1", "hue2", "sat2", "value2"]
    values = [5, 100, 100, 16, 255, 255]
    ranges =[[0, 100], [0, 255], [0, 255], [0, 100], [0, 255], [0, 255]]
    option = [0]

    while cap.isOpened():
        
        lowerbound = np.array([values[0], values[1], values[2]])
        upperbound = np.array([values[3], values[4], values[5]])
        
        ret, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # determines what pixels remain in image
        mask = cv2.inRange(hsv, lowerbound, upperbound)
        output = cv2.bitwise_and(img, img, mask=mask)
        showValues(img, names, ranges, values, option)
        imgStack = stackImages(0.3, ([output, mask],[img, img]))
        cv2.imshow('img', imgStack)
        k = cv2.waitKey(27)
        
        if k == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("end")


if __name__ == "__main__":
    color_detect()
    
# show vals
# names[]
# vals[]
#ranges[]
# option = [0]
