
# Stacks multiple images into 1 large image, useful for comparing and testing.
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
