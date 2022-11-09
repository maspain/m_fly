from asyncore import read
import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()
    cv2.imshow('img', img)
    
    k = cv2.waitKey(27)
    
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print("end")