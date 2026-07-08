#!/usr/bin/env python3
"""
Graph thrust required and thrust available at sea level, 10,000 ft, and 35,000 ft (fl350)

Produced for "Python for Mechanical and Aerospace Engineering" by Alex Kenan,
ISBN 978-1-7360606-0-5 and 978-1-7360606-1-2.
Copyright © 2020 Alexander Kenan. Some Rights Reserved.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International License.
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

Explanatory comments throughout this file were added by Ethan Koh.
"""

# Import pi from NumPy so it can be used in the induced-drag equation.
from numpy import pi

# Import Matplotlib's plotting tools to create the thrust graphs.
import matplotlib.pyplot as plt


# Functions

def knots_to_ftpersec(speed):
    # Convert a speed from knots to feet per second.
    return speed * 1.68781


def thrust_required(rho_inf, v_inf, s, cd0_, k, w):
    # Calculate the lift coefficient needed to support the aircraft weight.
    cl = 2 * w / (rho_inf * v_inf ** 2 * s)

    # Calculate thrust required using parasite drag and induced drag.
    return 0.5 * rho_inf * v_inf ** 2 * s * (cd0_ + k * cl ** 2)


# Inputs

# Aircraft and aerodynamic values.
weight = 200000  # Aircraft weight in pounds.
wing_area = 1318  # Wing area in square feet.
wing_span = 117.416666667  # Wing span in feet.
cd0 = 0.0185  # Zero-lift drag coefficient.
thrust = 66000  # Total engine thrust in pounds.

# Calculate aircraft geometry and induced-drag factor.
aspect_ratio = wing_span**2 / wing_area
e = 0.92  # Oswald efficiency factor.
K = 1 / (pi * e * aspect_ratio)

# Air density at sea level, measured in slugs per cubic foot.
rho_sl = 23.77E-4

# Create a list of sea-level velocity values in knots.
x_vals_sl = [i for i in range(80, 750, 10)]

# Calculate thrust required at sea level for each velocity.
tr_sl = [
    thrust_required(rho_sl, knots_to_ftpersec(x), wing_area, cd0, K, weight)
    for x in x_vals_sl
]


# Sea Level

# Create the first subplot for sea-level conditions.
plt.subplot(3, 1, 1)

# Plot thrust required at sea level.
plt.plot(x_vals_sl, tr_sl, 'k-', label=r"$T_R$ at Sea Level")

# Estimate thrust available at sea level.
TA_sl = 0.7 * thrust

# Create a horizontal line showing thrust available.
y_coords_sl = [TA_sl for _ in x_vals_sl]

# Create a vertical line showing takeoff velocity.
takeoff_vel_sl = [180, 180]
cruise_velocity_sl_values = [11000, 46500]

plt.plot(
    x_vals_sl,
    y_coords_sl,
    'k--',
    label='$T_A$ at Sea Level ({:,.0f} lb)'.format(TA_sl)
)

plt.plot(
    takeoff_vel_sl,
    cruise_velocity_sl_values,
    'b-.',
    label="Takeoff Velocity ({} knots)".format(takeoff_vel_sl[0])
)

# Format the sea-level graph.
plt.ylim(5000, 50000)
plt.xlim(50, 1550)
plt.ylabel('Thrust (lb)')
plt.title('Thrust Required & Thrust Available Curves')
plt.legend(loc='lower right')


# FL100

# Create the second subplot for 10,000 ft conditions.
plt.subplot(3, 1, 2)

# Air density at 10,000 ft, measured in slugs per cubic foot.
rho_fl100 = 17.56E-4

# Create velocity values and calculate thrust required at FL100.
x_vals_fl100 = [i for i in range(110, 745, 10)]
tr_fl100 = [
    thrust_required(rho_fl100, knots_to_ftpersec(x), wing_area, cd0, K, weight)
    for x in x_vals_fl100
]

# Estimate thrust available at FL100 by adjusting for lower air density.
TA_fl100 = 0.7 * thrust * rho_fl100 / rho_sl

# Create a vertical line showing cruise velocity at FL100.
cruise_velocity = [250, 250]
cruise_velocity_fl100_values = [10000, 34130]

# Create a horizontal line showing thrust available at FL100.
y_coords_fl100 = [TA_fl100 for _ in x_vals_fl100]

plt.plot(x_vals_fl100, tr_fl100, 'k-', label=r"$T_R$ at FL100")

plt.plot(
    x_vals_fl100,
    y_coords_fl100,
    'k--',
    label="$T_A$ at FL100 ({:,.0f} lb)".format(TA_fl100)
)

plt.plot(
    cruise_velocity,
    cruise_velocity_fl100_values,
    'b-.',
    label="Cruise Velocity ({} knots)".format(cruise_velocity[0])
)

# Format the FL100 graph.
plt.ylabel('Thrust (lb)')
plt.ylim(5000, 38000)
plt.xlim(50, 1550)
plt.legend(loc='lower right')


# FL350

# Create the third subplot for 35,000 ft conditions.
plt.subplot(3, 1, 3)

# Air density at 35,000 ft, measured in slugs per cubic foot.
rho_fl350 = 7.38E-4

# Create a vertical line showing cruise velocity at FL350.
cruise_velocity_fl350 = [450, 450]
cruise_velocity_fl350_values = [9900, 14200]

# Create velocity values and calculate thrust required at FL350.
x_vals_fl350 = [i for i in range(280, 695, 10)]
tr_fl350 = [
    thrust_required(rho_fl350, knots_to_ftpersec(x), wing_area, cd0, K, weight)
    for x in x_vals_fl350
]

# Estimate thrust available at FL350 by adjusting for lower air density.
TA_fl350 = 0.7 * thrust * rho_fl350 / rho_sl

# Create a horizontal line showing thrust available at FL350.
y_coords_fl350 = [TA_fl350 for _ in x_vals_fl350]

plt.plot(x_vals_fl350, tr_fl350, 'k-', label=r"$T_R$ at FL350")

plt.plot(
    x_vals_fl350,
    y_coords_fl350,
    'k--',
    label=r"$T_A$ at FL350 ({:,.0f} lb)".format(TA_fl350)
)

plt.plot(
    cruise_velocity_fl350,
    cruise_velocity_fl350_values,
    'b-.',
    label="Cruise Velocity ({} knots)".format(cruise_velocity_fl350[0])
)

# Format the FL350 graph.
plt.xlabel('Velocity (knots)')
plt.ylabel('Thrust (lb)')
plt.xlim(50, 1550)
plt.ylim(9600, 15000)
plt.legend(loc='lower right')

# Add spacing between the three graphs so labels do not overlap.
plt.subplots_adjust(hspace=0.35)

# Display the final figure.
plt.show()