import cv2
import argparse
import numpy as np



ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fileDir", required=True, help="path to image analyzed")

args = vars(ap.parse_args())
imgFile = args["fileDir"]

while True:
    img = cv2.imread(imgFile)
    cv2.imshow("img", img)
    k = cv2.waitKey(27) & 0xff
    
    if k == ord('q'):
        break
    
cv2.destroyAllWindows()