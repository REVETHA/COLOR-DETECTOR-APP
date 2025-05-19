# app.py

import cv2
import pandas as pd

# Load the color dataset
csv_path = 'colors.csv'
color_data = pd.read_csv(csv_path)

# Read the image
img_path = 'your_image.jpg'  # Replace with your image filename
img = cv2.imread(img_path)

# Global variables to store clicked coordinates and color values
clicked = False
r = g = b = xpos = ypos = 0

# Mouse click event handler
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Set the window and bind the mouse event
cv2.namedWindow('Color Detector')
cv2.setMouseCallback('Color Detector', draw_function)

# Function to get color name from RGB
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(color_data)):
        r_d = abs(R - int(color_data.loc[i, "R"]))
        g_d = abs(G - int(color_data.loc[i, "G"]))
        b_d = abs(B - int(color_data.loc[i, "B"]))
        distance = r_d + g_d + b_d  # Manhattan distance
        if distance < minimum:
            minimum = distance
            cname = color_data.loc[i, "color_name"]
    return cname


while True:
    cv2.imshow("Color Detector", img)

    if clicked:
        # Draw rectangle and show RGB values
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)
        color_name = get_color_name(r, g, b)
        text = f"{color_name}  R={r} G={g} B={b}"
        # Use black or white text depending on brightness
        text_color = (0, 0, 0) if (r + g + b) >= 600 else (255, 255, 255)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:  # Press 'ESC' key to exit
        break

cv2.destroyAllWindows()
