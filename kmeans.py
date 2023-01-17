import cv2
import argparse
import numpy as np

def color2ID(argument):
    #"white","black","gray","red","blue","green","yellow","purple","brown","orange"
    switcher={
        "white":[[[0,0,230],[180,75,255]]],#    Yifu (mod: upper hue changed 179->180)
        "black":[[[0,0,0],[180,255,60]]],#      Ramsey (mod: upper hue changed from 255->180)
        "gray":[[[0,0,120],[180,40,180]]],
        "red":[[[170,125,90],[180,255,255]],[[0,125,90],[3,255,255]]],#  Abraham
        "blue":[[[85,110,120],[130,255,255]]],#     Ryan 
        "green":[[[35,100,100],[85,250,250]]],#     Nan
        "yellow":[[[45/2,110,30],[45/2+15,255,255]]],
        "purple":[[[130, 50, 70],[155, 255, 255]]],#    Meghan
        "brown":[[[9,100,80],[40,220,180]]],#           Joyce (mod: lower hue changed 0->9)
        "orange":[[[5,100,100],[16,255,255]]]#          Mason 
    }
    
    return switcher.get(argument, "Bad Color!!!")

def IDcolor(hsv):
    pixcolor="unknown"
    colors = ["white","black","gray","red","blue","green","yellow","purple","brown","orange"]
    for color in colors:
        colorArr = color2ID(color)
        if (hsv[0] >= colorArr[0][0][0] and hsv[1] >= colorArr[0][0][1] 
            and hsv[2] >= colorArr[0][0][2] and hsv[0] <= colorArr[0][1][0] 
            and hsv[1] <= colorArr[0][1][1] and hsv[2] <= colorArr[0][1][2]):
            pixcolor = color
            break
        if (color == "red" and hsv[0] >= colorArr[1][0][0] and hsv[1] >= colorArr[1][0][1] 
            and hsv[2] >= colorArr[1][0][2] and hsv[0] <= colorArr[1][1][0] 
            and hsv[1] <= colorArr[1][1][1] and hsv[2] <= colorArr[1][1][2]):
            pixcolor = color
            break
    return pixcolor
    
    
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fileDir", required=True, help="path to image analyzed")

args = vars(ap.parse_args())
imgFile = args["fileDir"]
img = cv2.imread(imgFile)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

pink = [175, 100, 255]
mask_value = 255
super_mask = cv2.inRange(hsv, np.array([0,0,0]), np.array([100, 255, 255]))
super_mask = 255 - super_mask

area = hsv.shape[0]*hsv.shape[1]
colors = ["white","black","gray","red","blue","green","yellow","purple","brown","orange"]

rank=[]
for trgtColor in colors:
    cNum = []
    for id in color2ID(trgtColor):
        cNum.append(id)
    low = np.array([cNum[0][0]])
    high = np.array([cNum[0][1]])
    mask = cv2.inRange(hsv, low, high)
    
    if (trgtColor == "red"):
        low2 = np.array([cNum[1][0]])
        high2 = np.array([cNum[1][1]])
        mask2 = cv2.inRange(hsv, low2, high2)
        mask = cv2.bitwise_or(mask, mask2)
    super_mask = cv2.bitwise_or(super_mask, mask)
    
    switcher = {
        "white": [0,0,255],
        "black": [0,0,0],
        "gray": [0,0,150],
        "red": [4, 219, 219],
        "blue":[109, 219, 219],
        "green":[59, 219, 255],
        "yellow":[30, 219, 255],
        "purple": [127, 219, 255],
        "brown": [19, 199, 109],
        "orange": [14, 230, 255]
    }
    
    ratio = (mask==225).sum()/area*100
    rank.append([ratio, trgtColor])
    sel = mask == mask_value
    hsv[sel] = switcher.get(trgtColor)
    
rank = sorted(rank, reverse=True)
# data = np.reshape(hsv, (height * width, 3))

# num_clusters = 5
# kmeans = KMeans(n_clusters=num_clusters)
# kmeans.fit(data)
# dominant_colors = np.array(kmeans.cluster_centers_, dtype='uint')
# percentages = (np.unique(kmeans.labels_, return_counts=True)[1])/data.shape[0]
# p_and_c = zip(percentages, dominant_colors)
# p_and_c = sorted(p_and_c, reverse=True)d(rank, reverse=True)
for x in rank:
    print(x)
    


# height, width,_ = np.shape(hsv)
# data = np.reshape(hsv, (height * width, 3))

# num_clusters = 5
# kmeans = KMeans(n_clusters=num_clusters)
# kmeans.fit(data)
# dominant_colors = np.array(kmeans.cluster_centers_, dtype='uint')
# percentages = (np.unique(kmeans.labels_, return_counts=True)[1])/data.shape[0]
# p_and_c = zip(percentages, dominant_colors)
# # p_and_c = sorted(p_and_c, reverse=True)
# for i in range(num_clusters):
#     print(str(p_and_c[i])+ " " + IDcolor(p_and_c[i][1]))

while True:
    cv2.imshow("img", img)
    cv2.imshow("simplified", img)
    
    k = cv2.waitKey(27) & 0xff
    
    if k == ord('q'):
        break
    
cv2.destroyAllWindows()