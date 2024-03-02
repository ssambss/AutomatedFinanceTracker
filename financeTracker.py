import gspread
import pandas as pd
import os
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Define the path to your CSV file
csv_file_path = input('Enter the path to the CSV file: ')

# Define the columns to be imported from the CSV file
selected_columns = [0, 1, 5]

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path, delimiter=';', usecols=selected_columns)

# Convert the values in amount column from string to float
df.Määrä = df.Määrä.str.replace(',', '.').astype(float)

# Column names to be inserted into the first row of the Google Sheets worksheet
columns = [df.columns.values.tolist()]

# Column values to be inserted into the Google Sheets worksheet
values = df.values.tolist()

# Define the path to your Google Sheets credentials JSON file
credentials_file_path =  os.getenv('credentials_path')

# Define the name of the Google Sheets spreadsheet
spreadsheet_name = 'Automated Finance Tracker'

# Define the name of the worksheet within the Google Sheets spreadsheet
worksheet_name = input('Enter the name of the worksheet: ')

# Load the credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file'])

# Authorize the credentials
client = gspread.Client(auth=credentials)

# Open the Google Sheets spreadsheet
spreadsheet = client.open(spreadsheet_name)

# Select the worksheet within the spreadsheet
worksheet = spreadsheet.worksheet(worksheet_name)

# Write the data to the Google Sheets worksheet
worksheet.update(columns + values)

print('Data has been successfully imported to Google Sheets.')