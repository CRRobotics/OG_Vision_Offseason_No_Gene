import cv2
# from config import *
import numpy as np
# Open the default camera (usually the first one)
cap = cv2.VideoCapture(0)

from config import *
# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a named window with the option to resize
cv2.namedWindow("Epic Vision Game", cv2.WINDOW_NORMAL)



# def show_enemy(frame, Enemy: Enemy)-> None:
#     cords = Enemy.getCords()
#     if type(Enemy) == Hexagon:
#         draw_hexagon(frame, (100,100), 30, Enemy.getColor())
#     elif type(Enemy) == Diamond:
#         draw_diamond(frame, (100,100), 30, Enemy.getColor())




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

    # Create a copy of the original frame to draw the filled hexagon
    overlay = frame.copy()

    # Fill the hexagon on the overlay
    cv2.fillPoly(overlay, [vertices], color)

    # Blend the overlay with the original frame using alpha transparency
    alpha = 0.5  # Set transparency level to 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Optionally, you can still draw the border
    cv2.polylines(frame, [vertices], isClosed=True, color=color, thickness=2)




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

    # Create a copy of the original frame to draw the filled diamond
    overlay = frame.copy()

    # Fill the diamond on the overlay
    cv2.fillPoly(overlay, [vertices], color)

    # Blend the overlay with the original frame using alpha transparency
    alpha = 0.5  # Set transparency level to 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Optionally, you can still draw the border
    cv2.polylines(frame, [vertices], isClosed=True, color=color, thickness=2)



while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        print("have frame")
    # draw_hexagon(frame, (100,100), 30, (255,0,0))
    # draw_diamond(frame, (300,100), 30, (0,0,255))
    config_main(frame)


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

# Release the capture when everytsng is done
cap.release()
cv2.destroyAllWindows()


