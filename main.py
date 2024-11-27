import cv2, time
from cvzone.HandTrackingModule import HandDetector # We load this model for hand tracking

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 680)

# Create Instance of HandDetector
detector = HandDetector(maxHands=1) # As we need only one hand for Game

# We writer timer and states for game
timer = 0
statesResult = False
startGame = False

while True:
    # Check background Image Inside Loop, So that when User update Value It changed
    bgImg = cv2.imread('resources/bg.jpg')
    r, frame = cam.read()
    if not r:
        break
    
    imageScale = cv2.resize(frame, (0, 0), None, 0.95, 0.93)
    imageScale = imageScale[80:540, 85:520]
    # Resize imageScale to fit the target region in bgImg (465x435)
    imageScale = cv2.resize(imageScale, (465, 435))

    # We Detect Hand On Scale Image
    hands, image = detector.findHands(imageScale)

    if startGame:
        if statesResult is False:
            timer = time.time() - initialTime
            cv2.putText(bgImg, str(int(timer)), (625,365), cv2.FONT_HERSHEY_PLAIN, 4, (255,0,255), 3)

            if timer > int(4):
                statesResult = True
                timer = 0

                # Check For Fingers
                if hands:
                    # Get First Hand, As we get hands in list
                    hand = hands[0]
                    fingers = detector.fingersUp(myHand=hand)
                    print(fingers)
                    if 1 not in fingers:
                        rock = True
                    
                    if 0 not in fingers:
                        paper = True

                    if fingers[1] == 1 and fingers[2] == 1 and 1 not in fingers[2:] and fingers[0]==0:
                        seccior = True
    else:    
        cv2.putText(bgImg, "Play: ", (603,335), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
        cv2.putText(bgImg, "p", (660,335), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
        cv2.putText(bgImg, "Quit: ", (603,360), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
        cv2.putText(bgImg, "q", (660,360), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
                    
    imageScale = cv2.cvtColor(imageScale, cv2.COLOR_BGR2LUV)

    # Assign the resized imageScale to the region in bgImg
    bgImg[145:580, 111:576] = imageScale

    cv2.imshow("BG Image", bgImg)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        break 

    elif key == ord('P') or key == ord('p'):
        startGame = True
        print("Game is Started")
        initialTime = time.time()
        statesResult = True

cam.release()
cv2.destroyAllWindows()