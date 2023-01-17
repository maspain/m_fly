from unicodedata import name
import cv2
import argparse
import numpy as np

def blur_img(imgFile):
    pass

def arg_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fileDir", required=True, help="path to image analyzed")

    args = vars(ap.parse_args())
    imgFile = args["fileDir"]
    return imgFile


def find_contour(imgFile):
    thresh1 = 100
    thresh2 = 180

    while True:
        img = cv2.imread(imgFile)
        imgCan = cv2.Canny(img, thresh1, thresh2)
        kernel = np.ones((3, 3))
        imgDil = cv2.dilate(imgCan, kernel, iterations = 1)
        
        cntr, hierarchy = cv2.findContours(imgDil.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for c in cntr:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.03 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            sides = len(approx)
            area = cv2.contourArea(c)
            
            if (area > 500):
                cv2.putText(img, str(sides), (x + y - 100, y + 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0 ), 2)
                cv2.drawContours(img, c, -1, (255, 0, 0), 7)
        
        cv2.imshow("img", img)
        k = cv2.waitKey(27) & 0xff
        if k == ord('q'):
            break
        
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    imgFile = arg_parse()
    find_contour(imgFile)