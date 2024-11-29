import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone
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
result = None 

# Camera Frame Variable
# Define the region where the frame will be inserted
top_left_y = 145
bottom_right_y = 580
top_left_x = 111
bottom_right_x = 576
# Calculate the size of the region where the frame will be inserted
region_height = bottom_right_y - top_left_y
region_width = bottom_right_x - top_left_x

# Instruction are Displaying
instruction = True
instruction_image = cv2.imread('resources/instructions.png')

# Create Video Of Game
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# Create VideoWriter object to write the video
output = cv2.VideoWriter(filename='output.mp4', fourcc=fourcc,fps=40, frameSize=(950, 650))
# Variable To Check When To write Video
writeVideo = False

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

# Main game loop
while True:
    # Load background image
    bgImg = cv2.imread("resources/bg.jpg")
    ret, frame = cam.read()
    if not ret:
        break

    # Resize and crop webcam feed
    frame = cv2.resize(frame, (0, 0), fx=0.95, fy=0.93)
    frame = frame[80:540, 85:520]
    if not instruction:
        frame = cv2.resize(frame, (region_width, region_height))
    else:
        frame = cv2.resize(instruction_image, (region_width, region_height))
    
    # Detect hands if game is running
    hands, image = detector.findHands(frame) if startGame else (None, None)

    if startGame:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(bgImg, f"{int(4 - timer)}", (625,365), cv2.FONT_HERSHEY_PLAIN, 4, (255,0,255), 3)

            if timer > 3:  # Timer for the round
                stateResult = True
                timer = 0

                # Player move
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors
                    else:
                        playerMove = None  # Invalid move
                        resultText = "Invalid Move!"  # Show invalid move message
                else:
                    playerMove = None  # No hand detected
                    resultText = "No Hand Detected!"  # No hand detected message

                # AI move
                aiMove = random.randint(1, 3)

                # Determine winner
                if playerMove:
                    result = determine_winner(playerMove, aiMove)
                    if result == 1:
                        score[1] += 1
                    elif result == -1:
                        score[0] += 1

                # Load and overlay AI image
                aiImg = cv2.imread(f"resources/{aiMove}.png", -1)
                bgImg = cvzone.overlayPNG(bgImg, aiImg, (850, 230))
            
        else: 
            if max(score) < maxScore:   
                cv2.putText(bgImg, "Play: ", (603,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
                cv2.putText(bgImg, "p", (660,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
                cv2.putText(bgImg, "Quit: ", (603,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
                cv2.putText(bgImg, "q", (660,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
        
        if max(score) < maxScore:
            # Show results
            if result == 1 or result == -1:
                cv2.putText(bgImg, resultText, (584, 630), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 4)
                result = None
            else:
                cv2.putText(bgImg, resultText, (565, 630), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 4)
                
    else:    
        # Display game over if max score reached
        if max(score) < maxScore:
            cv2.putText(bgImg, "Press 'P' to Play", (480, 630), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)

    # If it is showing Result, Overlay PNG
    if stateResult:
        # Over Lay AI Image
        bgImg = cvzone.overlayPNG(bgImg, aiImg, (850, 230))

    # Update scores and instructions
    cv2.putText(bgImg, f"{score[1]}", (496, 131), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(bgImg, f"{score[0]}", (1082, 131), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    # Display game over if max score reached
    if max(score) >= maxScore:
        winner = "Player" if score[1] > score[0] else "AI"
        cv2.putText(bgImg, f"Game Over! {winner} Wins!", (420, 630), cv2.FONT_HERSHEY_COMPLEX, 1.4, (0, 255, 255), 5)
        cv2.putText(bgImg, "Restart: ", (600,340), cv2.FONT_HERSHEY_PLAIN, 1, (100,250,55), 1)
        cv2.putText(bgImg, "r", (670,340), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
        cv2.putText(bgImg, "Quit: ", (603,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (100,250,55), 2)
        cv2.putText(bgImg, "q", (660,365), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,50,255), 2)
        # Apply the Summer DeepGreen
        bgImg = cv2.applyColorMap(bgImg, cv2.COLORMAP_DEEPGREEN)
        startGame = False

     # Apply the Summer DeepGreen
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_DEEPGREEN) if startGame and not stateResult else cv2.applyColorMap(frame, cv2.COLORMAP_INFERNO)
    # Overlay the webcam feed
    bgImg[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = frame
    bgImg = cv2.resize(bgImg, (950, 650))
    cv2.imshow("Rock Paper Scissors", bgImg)
    if writeVideo:
        output.write(bgImg)

    # Key press handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("p"):
        startGame = True
        initialTime = time.time()
        stateResult = False
        resultText = ""
    elif key == ord("r"):
        score = [0, 0]
        startGame = False
        stateResult = False
    elif key == ord('s') and writeVideo == False:
        writeVideo = True
    elif key == ord('s') and writeVideo:
        writeVideo = False
        output.release()
    elif key == ord('i'):
        instruction = True
    elif key == ord('c'):
        instruction = False

# Release resources
cam.release()
output.release()
cv2.destroyAllWindows()
