import cv2
# import cvzone

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 680)
bgImg = cv2.imread('bg.jpg')

while True:
    r, frame = cam.read()
    if not r:
        break
    
    imageScale = cv2.resize(frame, (0, 0), None, 0.95, 0.93)
    imageScale = imageScale[80:540, 85:520]

    # Resize imageScale to fit the target region in bgImg (465x435)
    imageScale = cv2.resize(imageScale, (465, 435))

    imageScale = cv2.cvtColor(imageScale, cv2.COLOR_BGR2LUV)
    # Assign the resized imageScale to the region in bgImg
    bgImg[145:580, 111:576] = imageScale

    cv2.imshow("BG Image", bgImg)
    
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break 

cam.release()
cv2.destroyAllWindows()
