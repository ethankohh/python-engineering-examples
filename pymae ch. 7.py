#!/usr/bin/env python3

"""
Get aluminum properties from Engineering ToolBox and write them to Excel.

Original project/source:
"Python for Mechanical and Aerospace Engineering" by Alex Kenan
GitHub: https://github.com/alexkenan/pymae
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
See http://creativecommons.org/licenses/by-nc-sa/4.0/ for more information.

This version was adapted and explanatory comments were added by Ethan Koh.
"""

# Import Path so the Excel file can be saved next to this Python script.
from pathlib import Path

# Import Requests to download the webpage.
import requests

# Import BeautifulSoup to search through the HTML from the webpage.
from bs4 import BeautifulSoup

# Import OpenPyXL to create and save an Excel spreadsheet.
import openpyxl


def scrape_website(address):
    # Add a user-agent so the website sees the request like a normal browser.
    headers = {
        "user-agent": "Mozilla/5.0"
    }

    # Download the webpage from the given address.
    response = requests.get(address, headers=headers, timeout=10)

    # Stop the program if the website request failed.
    response.raise_for_status()

    # Return the webpage's HTML text.
    return response.text


def clean_cell_text(cell):
    # Get text from an HTML table cell and remove extra spaces.
    text = cell.get_text(strip=True)

    # Some empty cells use special blank characters, so replace them with "None".
    if text == "" or text == "\xa0":
        return "None"

    # Return the cleaned cell text.
    return text


def extract_properties_from_response(response):
    # Convert the HTML text into something Python can search.
    soup = BeautifulSoup(response, "html.parser")

    # Find the aluminum properties table.
    table = soup.select_one("table.large")

    # If the table cannot be found, stop with a helpful error message.
    if table is None:
        raise ValueError("Could not find the aluminum properties table.")

    # This list will store the rows of table data.
    properties = []

    # Go through each table row.
    for table_row in table.find_all("tr"):

        # Get both header cells and normal data cells.
        cells = table_row.find_all(["th", "td"])

        # Skip rows that do not contain any table cells.
        if len(cells) == 0:
            continue

        # This list will store one cleaned row from the table.
        row = []

        # Clean each cell and add it to the row.
        for cell in cells:
            row.append(clean_cell_text(cell))

        # Add the completed row to the full properties list.
        properties.append(row)

    # Return all extracted table rows.
    return properties


def convert_number_if_possible(value):
    # Convert number-looking text into a real number for Excel.
    try:
        return float(value)

    # If the value is not a number, keep it as text.
    except ValueError:
        return value


def create_spreadsheet(info):
    # Create a new Excel workbook.
    workbook = openpyxl.Workbook()

    # Use the active worksheet and rename it.
    worksheet = workbook.active
    worksheet.title = "aluminum"

    # Add each row of scraped data to the worksheet.
    for row in info:
        # This list will store the row after numbers are converted.
        cleaned_row = []

        # Convert each cell to a number if possible.
        for cell in row:
            cleaned_row.append(convert_number_if_possible(cell))

        # Add the cleaned row to the spreadsheet.
        worksheet.append(cleaned_row)

    # Save the file in the same folder as this Python script.
    destination = Path(__file__).with_name("aluminum_properties.xlsx")
    workbook.save(filename=destination)

    # Return the saved file path so it can be printed later.
    return destination


# Run this code only when the file is executed directly.
if __name__ == "__main__":
    # Webpage containing aluminum pipe properties.
    url = "https://www.engineeringtoolbox.com/properties-aluminum-pipe-d_1340.html"

    try:
        # Download the webpage.
        website_text = scrape_website(url)

        # Extract the aluminum table data from the webpage.
        results = extract_properties_from_response(website_text)

        # Create the Excel spreadsheet from the extracted data.
        saved_file = create_spreadsheet(results)

        # Let the user know the spreadsheet was created.
        print("Spreadsheet created successfully.")
        print("Saved file:", saved_file)

    # If any step fails, print the error instead of crashing without explanation.
    except Exception as error:
        print("Something went wrong.")
        print("Error:", error)