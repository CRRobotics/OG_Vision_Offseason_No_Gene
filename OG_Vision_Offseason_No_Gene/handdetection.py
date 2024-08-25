import mediapipe as mp # For the AI
from mediapipe.tasks import python # Imports Python into Python
from mediapipe.tasks.python import vision # Imports The Vision from Marvel
import cv2 # Camera stuff
import numpy as np # Needed to make image thing work
from config import * # Things for the game
from time import sleep
from time import time
import warnings
warnings.filterwarnings("ignore")

print("imports successful")

# This can change depending on the camera but it has to be a standard resolution
FOV_WIDTH_PIX = 640
FOV_HEIGHT_PIX = 480

currentFrame = None # Used to store the last frame that the AI read
alive = True

# Called on another thread when the AI runs, so it apparently can't display camera images, processes the result of the AI
def processResult(result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global currentFrame, alive
    npImage = output_image.numpy_view().astype(np.uint8) # Converts from mediapipe image to numpy image that cv2 can use
    alive = config_main(npImage)

    if len(result.hand_landmarks) > 0: # Checks if a hand is detected
        for i in [4, 8, 12, 16, 20]: # Thumb, pointer, middle, ring, pinkie
            landmark = result.hand_landmarks[0][i] # Get info on the fingertip from the result
            # Convert from mediapipe coordinate system to pixel coordinates
            x = int(landmark.x * FOV_WIDTH_PIX)
            y = int(landmark.y * FOV_HEIGHT_PIX)
            npImage = cv2.circle(npImage, (x, y), 0, (255, 255, 0), 5) # Draw a circle

    currentFrame = npImage # Outputs the processed frame to be displayed by the main thread

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
baseOptions = python.BaseOptions(model_asset_path='hand_landmarker.task')
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
        
        mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=image) # Convert from numpy image to mediapipe image for AI
        detector.detect_async(mpImage, int(time() * 1000)) # Sends the frame to the AI, which does its thing and calls processResult with the result
        if currentFrame is not None: cv2.imshow("Frame", currentFrame) # This needs to happen on the main thread

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()
