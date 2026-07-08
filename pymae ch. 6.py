#!/usr/bin/env python3
"""
Create a units converter GUI using Tkinter and Pint libraries.

Produced for "Python for Mechanical and Aerospace Engineering" by Alex Kenan,
ISBN 978-1-7360606-0-5 and 978-1-7360606-1-2.
Copyright © 2020 Alexander Kenan. Some Rights Reserved.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International License.
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

Explanatory comments throughout this file were added by Ethan Koh.
"""

# Import Tkinter to create the graphical user interface.
import tkinter as tk

# Import Pint to handle the unit conversion math.
import pint


# Third iteration

def main():
    # This function takes the user's input, converts it from one unit to another,
    # and displays the result in the output label.
    def calculate(number: str, unit1: str, unit2: str, field: tk.Label) -> None:
        """
        Cast number as float and convert it from one unit to another.

        :param number: str, number to attempt to cast to float and convert from unit1 to unit2
        :param unit1: str, first unit entered by the user
        :param unit2: str, second unit entered by the user
        :param field: tk.Label to update with the calculated number
        :return: None
        """

        try:
            # Remove commas from the input, then convert the value to a float.
            number = float(number.replace(',', ''))

            # Create a Pint unit registry and use it to create quantities.
            ureg = pint.UnitRegistry()
            converter = ureg.Quantity

            # Attach the starting unit to the number.
            initial_value = converter(number, ureg(unit1))

            # Convert the starting value into the requested final unit.
            final_value = initial_value.to(unit2)

            # Display the converted value rounded to two decimal places.
            field.configure(text='{:,.2f}'.format(final_value.magnitude), relief="sunken")

        # If the input cannot be converted to a number, show an input error.
        except ValueError:
            toreturn = 'Input a number'
            field.configure(text='{}'.format(toreturn), relief="sunken")

        # If Pint does not recognize one of the units, show a unit error.
        except pint.errors.UndefinedUnitError:
            toreturn = 'Unrecognized unit'
            field.configure(text='{}'.format(toreturn), relief="sunken")

        # If the units do not match, such as meters into seconds, show a unit type error.
        except pint.errors.DimensionalityError:
            toreturn = 'Check units'
            field.configure(text='{}'.format(toreturn), relief="sunken")

    # Create the main application window.
    app = tk.Tk()

    # Set the title that appears at the top of the window.
    app.title('Unit Converter')

    # Set the window size to 400 pixels wide by 200 pixels tall.
    app.geometry('400x200')

    # Add the main title label to the top of the window.
    tk.Label(app, text="Converter", font=("Verdana", 24)).grid(
        row=0,
        column=1,
        columnspan=3
    )

    # Add a label before the input field.
    calculate_text = tk.Label(app, text="Convert ")
    calculate_text.grid(row=1, column=1)

    # Store the number the user wants to convert.
    value_to_convert = tk.StringVar()

    # Create the input box where the user types the number.
    input_field = tk.Entry(
        app,
        borderwidth=2,
        relief="sunken",
        textvariable=value_to_convert,
        width=15
    )
    input_field.grid(row=1, column=2)

    # Store the starting unit.
    first_units = tk.StringVar()

    # Set the default starting unit to pascals.
    first_units.set('Pa')

    # Create the input box where the user types the starting unit.
    units_one = tk.Entry(
        app,
        borderwidth=2,
        relief="sunken",
        textvariable=first_units,
        width=10
    )
    units_one.grid(row=1, column=3)

    # Add the "into" label between the starting and ending units.
    into_text = tk.Label(app, text='into')
    into_text.grid(row=2, column=2)

    # Create the label where the converted answer will appear.
    calculated_value = tk.Label(app, borderwidth=2, relief="groove", width=15)
    calculated_value.grid(row=3, column=2)

    # Store the ending unit.
    second_units = tk.StringVar()

    # Set the default ending unit to pascals.
    second_units.set('Pa')

    # Create the input box where the user types the ending unit.
    units_two = tk.Entry(
        app,
        borderwidth=2,
        relief="sunken",
        textvariable=second_units,
        width=10
    )
    units_two.grid(row=3, column=3)

    # Add an empty row for spacing.
    tk.Label(app, text="").grid(row=4, column=2)

    # Create the Convert button.
    # When clicked, it gets the user's values and sends them to calculate().
    convert_button = tk.Button(
        app,
        text="Convert",
        command=lambda: calculate(
            value_to_convert.get().strip(),
            first_units.get().strip(),
            second_units.get().strip(),
            calculated_value
        )
    )
    convert_button.grid(row=5, column=2)

    # Start the Tkinter event loop so the window stays open and responds to clicks.
    app.mainloop()


# Run main() only when this file is executed directly.
if __name__ == '__main__':
    main()