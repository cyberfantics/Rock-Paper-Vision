import cv2
from cvzone.HandTrackingModule import HandDetector # We load this model for hand tracking

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 680)
bgImg = cv2.imread('resources/bg.jpg')

# Create Instance of HandDetector
detector = HandDetector(maxHands=1) # As we need only one hand for Game

while True:
    r, frame = cam.read()
    if not r:
        break
    
    imageScale = cv2.resize(frame, (0, 0), None, 0.95, 0.93)
    imageScale = imageScale[80:540, 85:520]
    # Resize imageScale to fit the target region in bgImg (465x435)
    imageScale = cv2.resize(imageScale, (465, 435))

    # We Detect Hand On Scale Image
    hands, image = detector.findHands(imageScale)

    # Check For Fingers
    if hands:
        # Get First Hand, As we get hands in list
        hand = hands[0]
        fingers = detector.fingersUp(myHand=hand)
        
        print(fingers)
    imageScale = cv2.cvtColor(imageScale, cv2.COLOR_BGR2LUV)

    # Assign the resized imageScale to the region in bgImg
    bgImg[145:580, 111:576] = imageScale

    cv2.imshow("BG Image", bgImg)
    
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break 

cam.release()
cv2.destroyAllWindows()
