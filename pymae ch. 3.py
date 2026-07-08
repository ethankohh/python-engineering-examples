#!/usr/bin/env python3
"""
Program that graphically shows maximum dynamic pressure (Max Q) as a function of
time for several different rocket launches.

Produced for "Python for Mechanical and Aerospace Engineering" by Alex Kenan,
ISBN 978-1-7360606-0-5 and 978-1-7360606-1-2.
Copyright (c) 2020 Alexander Kenan. Some Rights Reserved.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International License.
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

NOTE: An older version of this file incorrectly calculated density, which resulted
in computing an initial Max Q of nearly 1 billion psf. This is the correct
`density()` function that more accurately calculates density.

See `chap3_old.py` for the original `density()` function.

Explanatory comments throughout this file were added by Ethan Koh.
"""

# Imports

# NumPy is used for numerical tools, including arrays and the exponential function.
import numpy as np

# Matplotlib is used to create and display the graph.
import matplotlib.pyplot as plt


# Equations

def density(height: float) -> float:
    """
    Return the air density in slug/ft^3 based on altitude.

    Equations from https://www.grc.nasa.gov/www/k-12/rocket/atmos.html
    :param height: Altitude in feet
    :return: Density in slugs/ft^3
    """

    # Use one atmosphere equation for lower altitudes.
    if height < 36152.0:
        temp = 59 - 0.00356 * height
        p = 2116 * ((temp + 459.7) / 518.6) ** 5.256

    # Use a second atmosphere equation for middle altitudes.
    elif 36152 <= height < 82345:
        temp = -70
        p = 473.1 * np.exp(1.73 - 0.000048 * height)

    # Use a third atmosphere equation for higher altitudes.
    else:
        temp = -205.05 + 0.00164 * height
        p = 51.97 * ((temp + 459.7) / 389.98) ** -11.388

    # Convert pressure and temperature into air density.
    rho = p / (1718 * (temp + 459.7))
    return rho


def velocity(time: float, acceleration: float) -> float:
    """
    Convert time to velocity using Vf = Vi + at.

    In this program, initial velocity is 0, so the equation becomes Vf = at.
    :param time: Time in seconds
    :param acceleration: Acceleration in ft/s^2
    :return: Velocity in ft/s
    """

    # Calculate velocity after accelerating for the given amount of time.
    return acceleration * time


def altitude(time: float, acceleration: float) -> float:
    """
    Convert time to altitude using the constant acceleration equation.

    x = vi*t + 0.5*a*t^2, where initial velocity is 0 in this case.
    :param time: Time in seconds
    :param acceleration: Acceleration in ft/s^2
    :return: Altitude in feet
    """

    # Calculate altitude after accelerating for the given amount of time.
    return 0.5 * acceleration * time ** 2


# Main program

if __name__ == '__main__':
    # Use Matplotlib's built-in "bmh" style for the graph.
    plt.style.use('bmh')

    # Store the dynamic pressure values for the first acceleration case.
    y_values = []

    # Create time values from 0 to 550 seconds in 0.5 second steps.
    x_values = np.arange(0.0, 550.0, 0.5)

    # Calculate dynamic pressure for the first acceleration case.
    for elapsed_time in x_values:
        # Average acceleration needed to go from 0 ft/s to 26,400 ft/s
        # in 8.5 minutes. This is about 51.76 ft/s^2.
        accel = 51.764705882

        # Calculate altitude at this time.
        alt = altitude(elapsed_time, accel)

        # Dynamic pressure equation:
        # q = 0.5 * rho * V^2
        q = 0.5 * density(alt) * velocity(elapsed_time, accel) ** 2

        # Add the calculated dynamic pressure to the list.
        y_values.append(q)

    # Plot the first dynamic pressure curve.
    plt.plot(
        x_values,
        y_values,
        'b-',
        label=r"a = 51.76 $\frac{ft}{s^2}$"
    )

    # Find the maximum dynamic pressure value and where it occurs.
    max_val = max(y_values)
    ind = y_values.index(max_val)

    # Add an arrow and text label showing the Max Q value.
    plt.annotate(
        '{:.0f} psf @ {} s'.format(max_val, x_values[ind]),
        xy=(x_values[ind] + 2, max_val),
        xytext=(x_values[ind] + 15, max_val + 15),
        arrowprops=dict(facecolor='blue', shrink=0.05),
    )

    # Mark the Max Q point with a red x.
    plt.plot(x_values[ind], max_val, 'rx')


    # Second acceleration case: 32.2 ft/s^2

    # Store dynamic pressure values for the second acceleration case.
    y2_values = []

    for elapsed_time in x_values:
        # Set acceleration to 32.2 ft/s^2, which is about 1 g.
        accel = 32.2

        # Calculate altitude and dynamic pressure at this time.
        alt = altitude(elapsed_time, accel)
        q = 0.5 * density(alt) * velocity(elapsed_time, accel) ** 2

        # Add the calculated dynamic pressure to the list.
        y2_values.append(q)

    # Plot the second dynamic pressure curve.
    plt.plot(
        x_values,
        y2_values,
        'k-',
        label=r"a = 32.2 $\frac{ft}{s^2}$"
    )

    # Find the Max Q value for the second acceleration case.
    max_val = max(y2_values)
    ind = y2_values.index(max_val)

    # Add an arrow and text label showing the Max Q value.
    plt.annotate(
        '{:.0f} psf @ {} s'.format(max_val, x_values[ind]),
        xy=(x_values[ind] + 3, max_val),
        xytext=(x_values[ind] + 15, max_val + 15),
        arrowprops=dict(facecolor='black', shrink=0.05),
    )

    # Mark the Max Q point with a red x.
    plt.plot(x_values[ind], max_val, 'rx')


    # Third acceleration case: 20.0 ft/s^2

    # Store dynamic pressure values for the third acceleration case.
    y3_values = []

    for elapsed_time in x_values:
        # Set acceleration to 20.0 ft/s^2.
        accel = 20.0

        # Calculate altitude and dynamic pressure at this time.
        alt = altitude(elapsed_time, accel)
        q = 0.5 * density(alt) * velocity(elapsed_time, accel) ** 2

        # Add the calculated dynamic pressure to the list.
        y3_values.append(q)

    # Plot the third dynamic pressure curve.
    plt.plot(
        x_values,
        y3_values,
        'g-',
        label=r"a = 20.0 $\frac{ft}{s^2}$"
    )

    # Find the Max Q value for the third acceleration case.
    max_val = max(y3_values)
    ind = y3_values.index(max_val)

    # Add an arrow and text label showing the Max Q value.
    plt.annotate(
        '{:.0f} psf @ {} s'.format(max_val, x_values[ind]),
        xy=(x_values[ind] + 3, max_val),
        xytext=(x_values[ind] + 15, max_val + 15),
        arrowprops=dict(facecolor='green', shrink=0.05),
    )

    # Mark the Max Q point with a red x.
    plt.plot(x_values[ind], max_val, 'rx')


    # Graph formatting

    # Show only the first 150 seconds on the x-axis.
    plt.xlim(0, 150)

    # Add axis labels, a title, and a legend.
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (psf)')
    plt.title('Dynamic pressure as a function of time')
    plt.legend()

    # Display the completed graph.
    plt.show()