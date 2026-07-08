#!/usr/bin/env python3
"""
Graphically show camera shutter effect.

Produced for "Python for Mechanical and Aerospace Engineering" by Alex Kenan,
ISBN 978-1-7360606-0-5 and 978-1-7360606-1-2.
Copyright © 2020 Alexander Kenan. Some Rights Reserved.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International License.
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

Explanatory comments throughout this file were added by Ethan Koh.
"""

# Import Tkinter to create the window that displays the animation.
import tkinter as tk

# Import NumPy to create and update the propeller image using arrays.
import numpy as np

# Import Pillow tools to convert NumPy image data into a Tkinter image.
from PIL import Image, ImageTk


# Create the main Tkinter window.
root = tk.Tk()

# Create a label widget that will display each animation frame.
stage = tk.Label(root)
stage.pack()

# Set the height and width of the square image in pixels.
height = 300

# Set how many propeller blades will be drawn.
num_propeller_blades = 4

# Create a 2D coordinate grid centered around zero.
x, y = np.ogrid[-height / 2: height / 2, -height / 2: height / 2]

# Convert the 2D coordinate grid into complex numbers.
# This makes it easier to rotate the propeller mathematically.
plane = x - 1j * y

# Store the rolling-shutter distorted propeller image as it is built row by row.
bentprop = np.zeros_like(plane, dtype=bool)


# Animation loop

# Go through each row of the image.
# Each frame represents the propeller rotating while the camera scans downward.
for frame in range(height):
    # Start with a blank background.
    backgnd = np.zeros_like(plane, dtype=np.uint8)

    # Create a blank propeller mask for the current frame.
    propeller = np.zeros_like(plane, dtype=bool)

    # Calculate the current rotation angle of the propeller.
    angle = 2 * np.pi * (frame / height)

    # Draw each propeller blade.
    for blade in range(num_propeller_blades):
        # Calculate the rotation phase for this blade.
        phase = np.exp(1j * (angle + blade * np.pi / (num_propeller_blades / 2)))

        # Create a blade-like oval shape using distances in the complex plane.
        ellipse = abs(plane - 0.48 * height * phase) + abs(plane)

        # Add this blade shape to the propeller mask.
        propeller |= ellipse < 0.49 * height

    # Copy only the current scanned row into the bent propeller image.
    # This simulates a rolling shutter camera capturing one row at a time.
    bentprop[frame] = propeller[frame]

    # Create a small red/blue scan band to show where the shutter is currently reading.
    shutter_pan = [f for f in range(frame, min(frame + 3, height - 3))]

    # Define the colors used in the final image.
    # 0 = white background, 1 = black propeller, 2 = red bent propeller,
    # 3 = blue shutter scan band.
    colors = ("white", "black", "red", "blue")

    # Convert color names into RGB values that NumPy can use.
    rgbcolors = np.array(list(map(root.winfo_rgb, colors))) / 256

    # Combine the background, current propeller, and rolling-shutter propeller
    # into one image index array.
    composite = np.maximum.reduce((backgnd, propeller * 1, bentprop * 2))

    # Color the current shutter scan band blue.
    composite[shutter_pan] = 3

    # Convert the image index array into actual RGB pixel colors.
    rgb = rgbcolors.astype(np.uint8)[composite]

    # Convert the NumPy RGB array into an image Tkinter can display.
    image = ImageTk.PhotoImage(Image.fromarray(rgb, mode="RGB"))

    # Update the label with the new image frame.
    stage.config(image=image)

    # Force Tkinter to refresh the window during the loop.
    root.update()


# Bring the window to the front after the animation frames are generated.
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

# Add a title showing how many propeller blades were used.
root.title('{} blade propeller camera effect'.format(num_propeller_blades))

# Keep the Tkinter window open and responsive.
root.mainloop()
