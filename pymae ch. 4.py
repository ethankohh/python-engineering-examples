#!/usr/bin/env python3
"""
Graph 2D airfoils using the University of Illinois Urbana-Champaign (UIUC) website.

Produced for "Python for Mechanical and Aerospace Engineering" by Alex Kenan,
ISBN 978-1-7360606-0-5 and 978-1-7360606-1-2.
Copyright © 2020 Alexander Kenan. Some Rights Reserved.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International License.
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

Explanatory comments throughout this file were added by Ethan Koh.
"""

# Import Requests so the program can download airfoil coordinate data from a website.
import requests

# Import Matplotlib so the program can graph the airfoil shape.
import matplotlib.pyplot as plt


def get_airfoil_coords(airfoil: str) -> tuple:
    """
    Get airfoil coordinates from the UIUC airfoil database.

    https://m-selig.ae.illinois.edu/ads/coord/__.dat
    :param airfoil: Name of the airfoil type
    :return: Tuple of ([x coordinates], [y coordinates], plot_title)
    """

    # Build the URL for the selected airfoil.
    # The airfoil name is converted to lowercase to match the database filenames.
    url = 'https://m-selig.ae.illinois.edu/ads/coord/{}.dat'.format(airfoil.lower())

    # Add a user-agent header so the request looks like it came from a web browser.
    headers = {
        'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) '
            'Gecko/20100101 Firefox/74.0'
    }

    # Download the text file containing the airfoil coordinate data.
    response_text = requests.get(url, headers=headers).text

    # If the database page says "Not Found", stop the function with an error.
    if 'Not Found' in response_text:
        raise NameError('{} not found in UIUC database'.format(airfoil))

    # Split the downloaded text into separate lines.
    all_text = response_text.split('\n')

    # Create empty lists to store the x and y coordinate values.
    x_coordinates, y_coordinates = [], []

    # Store the airfoil title from the first line of the file.
    plot_title = ''

    # Go through each line in the downloaded airfoil data.
    for index, line in enumerate(all_text):

        # The first line is the title/name of the airfoil.
        if index == 0:
            plot_title = line.strip()

        # Every other line should contain an x and y coordinate pair.
        else:
            try:
                # Remove extra spaces from the beginning and end of the line.
                line = line.strip()

                # Split the line into x and y values.
                x, y = line.split(' ' * line.count(' '))  # Line changed.

                # Convert the coordinate strings into decimal numbers.
                x = float(x.strip())
                y = float(y.strip())

                # Only store coordinate points that are within the expected range.
                if x <= 1.0 and y <= 1.0:  # Line changed.
                    x_coordinates.append(x)
                    y_coordinates.append(y)

            # If a line cannot be converted into coordinates, skip it.
            except ValueError:
                continue

    # Return the coordinate lists and the title for plotting.
    return x_coordinates, y_coordinates, plot_title


def plot_airfoil(x_coordinates: list, y_coordinates: list, plot_title: str) -> None:
    """
    Plot the airfoil coordinates given the list of coordinates.

    :param x_coordinates: List of the airfoil's x coordinates
    :param y_coordinates: List of the airfoil's y coordinates
    :param plot_title: String to use as the plot's title
    :return: None
    """

    # Use Matplotlib's default graph style.
    plt.style.use('default')

    # Plot the airfoil shape using a black solid line.
    plt.plot(x_coordinates, y_coordinates, 'k-')

    # Add a title and set the visible graph range.
    plt.title('{} airfoil'.format(plot_title))
    plt.xlim(-0.50, 1.25)
    plt.ylim(-1, 1)

    # Display the completed airfoil graph.
    plt.show()


# Main program

# Choose which airfoil to look up in the UIUC database.
air_foil = 'mh70'

try:
    # Download and process the coordinate data for the selected airfoil.
    x_values, y_values, title = get_airfoil_coords(air_foil)

    # Plot the selected airfoil.
    plot_airfoil(x_values, y_values, title)

# If the selected airfoil is not found, print a helpful message.
except NameError:
    print('{} not in UIUC database, try again!'.format(air_foil))