import cv2
import numpy as np
import time

fourcc=cv2.VideoWriter_fourcc(*"XVID")
outputFile=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))

capture=cv2.VideoCapture(0)

time.sleep(2)
bg=0

for i in range(60):
    ret,bg=capture.read()

#flipping the background
bg=np.flip(bg,axis=1)

while(capture.isOpened()):
    ret,image=capture.read()
    if not ret:
        break
    
    image=np.flip(image,axis=1)

    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    lower_black=np.array([104,153,70])
    upper_black=np.array([30,30,0])
    mask1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_black,upper_black)

    mask=mask1+mask2

    mask1=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones(3,3),np.uint8)
    mask1=cv2.morphologyEx(mask,cv2.MORPH_DILATE,np.ones(3,3),np.uint8)
    
    mask2=cv2.bitwise_not(mask1)

    resolution1=cv2.bitwise_and(image,image,mask=mask2)

    resolution2=cv2.bitwise_and(bg,bg,mask=mask1)

    finaloutput=cv2.addWeighted(resolution1,1,resolution2,1,0)
    outputFile.write(finaloutput)

    cv2.imshow("magic",finaloutput)
    cv2.waitKey(1)

capture.release()
outputFile.release()
cv2.destroyAllWindows()