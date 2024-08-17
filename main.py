import cv2
from config import *
import numpy as np
# Open the default camera (usually the first one)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a named window with the option to resize
cv2.namedWindow("Epic Vision Game", cv2.WINDOW_NORMAL)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # show_enemy(frame, enemy)

    #break if can't oepn camera
    if ret == False:
        print("Can't open camera")
        break

    # Display the resulting frame in the resizable window
    cv2.imshow("Epic Vision Game", frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()



















def show_enemy(frame, Enemy: Enemy)-> None:
    cords = Enemy.getCords()
    if type(Enemy) == Hexagon:
        draw_hexagon(frame, (100,100), 30, Enemy.getColor())
    elif type(Enemy) == Diamond:
        draw_diamond(frame, (100,100), 30, Enemy.getColor())




def draw_hexagon(frame, coordinates_on_the_screen: tuple, size: int, color: tuple):


    # Calculate the six vertices of the hexagon
    center_x, center_y = coordinates_on_the_screen
    vertices = []
    for i in range(6):
        angle = 2 * np.pi / 6 * i
        x = int(center_x + size * np.cos(angle))
        y = int(center_y + size * np.sin(angle))
        vertices.append((x, y))

    # Convert vertices to a numpy array
    vertices = np.array(vertices, np.int32)
    vertices = vertices.reshape((-1, 1, 2))

    # Draw the hexagon on the image
    cv2.polylines(frame, [vertices], isClosed=True, color=color, thickness = 2)




def draw_diamond(frame, coordinates_on_the_screen: tuple, size: int, color: tuple):


    # Calculate the four vertices of the diamond
    center_x, center_y = coordinates_on_the_screen
    vertices = [
        (center_x, center_y - size),  # Top
        (center_x + size, center_y),  # Right
        (center_x, center_y + size),  # Bottom
        (center_x - size, center_y)   # Left
    ]

    # Convert vertices to a numpy array
    vertices = np.array(vertices, np.int32)
    vertices = vertices.reshape((-1, 1, 2))

    # Draw the diamond on the image
    cv2.polylines(frame, [vertices], isClosed=True, color=color, thickness=2)
