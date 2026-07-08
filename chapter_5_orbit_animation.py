#!/usr/bin/env python3

"""
Create a simple 3D animated orbit visualization.

Original orbit visualization concept/source:
"Python for Mechanical and Aerospace Engineering" by Alex Kenan
GitHub: https://github.com/alexkenan/pymae
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

This simplified version does not need PyAstronomy.
Adapted and explanatory comments added by Ethan Koh.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Create time values for the animation.
# These values represent one full trip around the orbit.
t = np.linspace(0, 2 * np.pi, 200)

# Create a simple elliptical orbit.
# The semi-major axis controls the width of the ellipse.
# The semi-minor axis controls the height of the ellipse.
semi_major_axis = 1.0
semi_minor_axis = 0.6

# Calculate the x and y coordinates of the ellipse.
x = semi_major_axis * np.cos(t)
y = semi_minor_axis * np.sin(t)

# Add a z coordinate so the orbit has a slight 3D tilt.
z = 0.3 * np.sin(t)

# Create the figure and 3D graph.
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot Earth at the center of the orbit.
ax.plot([0], [0], [0], "bo", markersize=9, label="Earth")

# Plot the full satellite path as a black line.
ax.plot(x, y, z, "k-", label="Satellite Trajectory")

# Plot the moving satellite point.
# Each coordinate is placed inside a list because Matplotlib expects sequences.
satellite_dot, = ax.plot([x[0]], [y[0]], [z[0]], "ro", label="Satellite")


def animate(frame):
    # Move the red satellite dot to the next orbit position.
    satellite_dot.set_data([x[frame]], [y[frame]])
    satellite_dot.set_3d_properties([z[frame]])

    # Return the updated dot to Matplotlib's animation system.
    return satellite_dot,


# Create the animation.
# frames=len(t) gives one animation frame for each orbit position.
# interval=50 means each frame lasts 50 milliseconds.
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(t),
    interval=50,
    blit=False
)

# Make the graph easier to read.
ax.set_title("Orbital Simulation")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()

# Set the viewing limits so the orbit stays centered in the window.
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)

# Show the animation window.
plt.show()
