import mediapipe as mp # For the AI
from mediapipe.tasks import python # Imports Python into Python
from mediapipe.tasks.python import vision # Imports The Vision from Marvel
import cv2 # Camera stuff
import numpy as np # Needed to make image thing work
import yaml # For the highscores file
from config import * # Stuff for the game
from time import sleep
from time import time

print("imports successful")

# This can change depending on the camera but it has to be a standard resolution
FOV_WIDTH_PIX = 640
FOV_HEIGHT_PIX = 480

currentFrame = None # Used to store the last frame that the AI read
alive = True

previousTime = time()
totalTime = 0

# Called on another thread when the AI runs, so it apparently can't display camera images, processes the result of the AI
def processResult(result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global currentFrame, alive, previousTime, totalTime
    npImage = output_image.numpy_view().astype(np.uint8) # Converts from mediapipe image to numpy image that cv2 can use
    currentTime = time()
    deltaTime = currentTime - previousTime
    previousTime = currentTime
    
    if len(result.hand_landmarks) > 0: # Checks if a hand is detected
        xCoords = []
        yCoords = []
        for i in [4, 8, 12, 16, 20]: # Thumb, pointer, middle, ring, pinkie
            landmark = result.hand_landmarks[0][i] # Get info on the fingertip from the result
            # Convert from mediapipe coordinate system to pixel coordinates
            x = int(landmark.x * FOV_WIDTH_PIX)
            y = int(landmark.y * FOV_HEIGHT_PIX)
            # npImage = cv2.circle(npImage, (x, y), 0, (255, 255, 0), 5) # Draw a circle
            xCoords.append(x)
            yCoords.append(y)
        totalTime += deltaTime
        alive = config_main(npImage, xCoords, yCoords)
    else:
        npImage = pauseScreen(npImage)
    currentFrame = npImage # Outputs the processed frame to be displayed by the main thread

def startScreen(npImage):
    npImage = cv2.rectangle(npImage, (0, 0), (FOV_WIDTH_PIX, FOV_HEIGHT_PIX), (0, 0, 0), -1)
    npImage = cv2.putText(npImage, "Hello!!!!!!!!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 1)
    return npImage

def pauseScreen(npImage):
    #npImage = cv2.rectangle(npImage, (0, 0), (FOV_WIDTH_PIX, FOV_HEIGHT_PIX), (0, 0, 0), -1)
    npImage = cv2.putText(npImage, "Hand not detected", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
    return npImage

def deathScreen(npImage):
    npImage = cv2.rectangle(npImage, (0, 0), (FOV_WIDTH_PIX, FOV_HEIGHT_PIX), (0, 0, 0), -1)
    npImage = cv2.putText(npImage, "Oh no yiy died!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 1)#jguyuyg
    return npImage

# From AprilTag code
def waitForCam(path):
    """Waits until there is a camera available at `path`. This is to ensure that cameras that are unplugged can be plugged back in and not interrupt the script."""
    while True:
        cap = cv2.VideoCapture(path)
        cap:cv2.VideoCapture
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FOV_WIDTH_PIX)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FOV_HEIGHT_PIX)
        cap.set(cv2.CAP_PROP_FPS, 20)
        if cap.isOpened():
            print("open")
            return cap
        else:
            sleep(0.001)
            print("Waiting")

# Make the AI
baseOptions = python.BaseOptions(model_asset_path=r"OG_Vision_Offseason_No_Gene\\hand_landmarker.task")
options = vision.HandLandmarkerOptions(base_options=baseOptions, running_mode=vision.RunningMode.LIVE_STREAM, result_callback=processResult, num_hands=1, min_hand_detection_confidence=0.2)

# Use the AI
with vision.HandLandmarker.create_from_options(options) as detector:
    print("detector successful")

    # Start camera feed
    cap = waitForCam(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    while alive:
        # From AprilTag code, reads cap and makes sure it's successful
        success, image = cap.read()
        if not success:
            print("failed to get image from camid 0")
            cap.release()
            cap = waitForCam(0)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        
        image = cv2.flip(image, 1)
        mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=image) # Convert from numpy image to mediapipe image for AI
        detector.detect_async(mpImage, int(time() * 1000)) # Sends the frame to the AI, which does its thing and calls processResult with the result
        if currentFrame is not None: cv2.imshow("Frame", currentFrame) # This needs to happen on the main thread

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print("You is do be ded. Sry.")
    print(f"You stayed alive for {totalTime} seconds.")
    print("Highscores:")
    filename = "OG_Vision_Offseason_No_Gene\\highscores.yml"
    with open(filename, "r") as file: scores = yaml.safe_load(file)
    for key in ["FIRST", "SECOND", "THIRD"]:
        if scores[key] < totalTime:
            oldHigh = scores[key]
            scores[key] = totalTime
            totalTime = oldHigh
        print(key + ": " + str(scores[key]))
    print(scores)
    with open(filename, "w") as file: yaml.safe_dump(scores, file)



# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()
