from cvzone.HandTrackingModule import HandDetector
import cvzone, cv2
import random

# Initialize webcam
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Create hand detector instance
detector = HandDetector(maxHands=1)

# Game variables
startGame = False
timer = 0
stateResult = False
playerMove = None
score = [0, 0]  # [AI, Player]
maxScore = 5  # Set max score for the game
resultText = ""

# Function to determine the winner
def determine_winner(player, ai):
    global resultText
    if (player == 1 and ai == 3) or (player == 2 and ai == 1) or (player == 3 and ai == 2):
        resultText = "You Win!"
        return 1  # Player wins
    elif (player == 3 and ai == 1) or (player == 1 and ai == 2) or (player == 2 and ai == 3):
        resultText = "AI Wins!"
        return -1  # AI wins
    else:
        resultText = "It's a Draw!"
        return 0  # Draw
    
while True:
    # Check background Image Inside Loop, So that when User update Value It changed
    bgImg = cv2.imread('resources/bg.jpg')
    r, frame = cam.read()
    if not r:
        break
    
    # Resize and crop webcam feed
    frame = cv2.resize(frame, (0, 0), fx=0.95, fy=0.93)
    frame = frame[80:540, 85:520]
    frame = cv2.resize(frame, (465, 435))

    # We Detect Hand On Scale Image
    hands, image = detector.findHands(imageScale) if startGame else (None, None)

    if startGame:
        if statesResult is False:
            timer = time.time() - initialTime
            cv2.putText(bgImg, str(int(timer)), (625,365), cv2.FONT_HERSHEY_PLAIN, 4, (255,0,255), 3)

            if timer >= int(4):
                statesResult = True
                timer = 0

                # Check For Fingers
                if hands:
                    # Get First Hand, As we get hands in list
                    hand = hands[0]
                    fingers = detector.fingersUp(myHand=hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1 # Rock
                    elif fingers == [1,1,1,1,1]:
                        playerMove = 2 # Seccior
                    elif fingers == [0,1,1,0,0]:
                        playerMove = 3 # Seccior
                
                # Choose Random Choice
                ai_choice = random.randint(1,3)
        
                # Load AI Image
                aiImage = cv2.imread(f'resources/{ai_choice}.png', -1)

                # Over Lay AI Image
                bgImg = cvzone.overlayPNG(bgImg, aiImage, (850, 230))

                    
                if (playerMove == 1 and ai_choice == 3) or (playerMove == 2 and ai_choice == 1) or (playerMove == 3 and ai_choice == 2):
                    score[1] += 1                    
                    
                    
                elif (playerMove == 3 and ai_choice == 1) or (playerMove == 1 and ai_choice == 2) or (playerMove == 2 and ai_choice == 3):
                    score[0] += 1
 
 
        else:    
            cv2.putText(bgImg, "Play: ", (603,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
            cv2.putText(bgImg, "p", (660,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
            cv2.putText(bgImg, "Quit: ", (603,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
            cv2.putText(bgImg, "q", (660,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
    else:    
        cv2.putText(bgImg, "Play: ", (603,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
        cv2.putText(bgImg, "p", (660,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
        cv2.putText(bgImg, "Quit: ", (603,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
        cv2.putText(bgImg, "q", (660,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
                
    # If it is showing Result, Overlay PNG
    if statesResult:
        # Over Lay AI Image
        bgImg = cvzone.overlayPNG(bgImg, aiImage, (850, 230))

    cv2.putText(bgImg, str(score[1]), (496, 131), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.2, (0,255,0), 4) # Update Player Score
    cv2.putText(bgImg, str(score[0]), (1082, 131), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.2, (255,0,255), 4) # Update AI Score
  
    
    # Apply the Summer DeepGreen
    imageScale = cv2.applyColorMap(imageScale, cv2.COLORMAP_DEEPGREEN) if startGame and statesResult else cv2.applyColorMap(imageScale, cv2.COLORMAP_INFERNO)

  # Assign the resized imageScale to the region in bgImg
    bgImg[145:580, 111:576] = imageScale
    bgImg = cv2.resize(bgImg, (800, 580))
    cv2.imshow("BG Image", bgImg)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        break 

    elif key == ord('P') or key == ord('p'):
        startGame = True
        initialTime = time.time()
        statesResult = False

cam.release()
cv2.destroyAllWindows()
