import gspread
import pandas as pd
import numpy as np
import os
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def set_transaction_categories(df, categories): 
    for title in df['Otsikko']:
        category_set = False
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title:
                    set_categories.append(category)
                    category_set = True
                    break
        
        if keyword not in title and category_set == False:
            set_categories.append('Muu')


def set_savings_to_positive(df):
    for index, row in df.iterrows():
        if row['Määrä'] < 0 and row['Kategoria'] == 'Säästö':
            df.at[index, 'Määrä'] = df.at[index, 'Määrä'] * -1


def calculate_total_monthly_sum(df):
    return df['Määrä'].sum()


def calculate_total_sum_per_category(df):
    return df.groupby('Kategoria')['Määrä'].sum().reset_index()


def load_csv_file(csv_file_path, selected_columns):
    return pd.read_csv(csv_file_path, delimiter=';', usecols=selected_columns)


# Insert the column names and values into a list of lists to use with gspread update method
def prepare_data_for_google_sheets(df):
    columns = [df.columns.values.tolist()]
    values = df.values.tolist()
    return columns, values


set_categories = []

categories = {"Säästö": [os.getenv('saving_account')],
            "Tulo": [os.getenv('salary')],
            "Ruoka": ["LIDL", "K-MARKET", "K-CITYMARKET", "PRISMA", "S-MARKET", "K-SUPERMARKET", "ALEPA", "SALE"], 
            "Laskut": ["ELISA", "SATS", "VIHREÄ ÄLYENERGIA", "DNA", "SPOTIFY", "INSINÖÖRILIITTO", "TURVA"],
            "Vuokra": [os.getenv('rent')]
            }


""" 
    
    Load the CSV file into a pandas dataframe, set categories for transactions and create dataframes for the total sum per category and monthly total sum 

"""

csv_file_path = input('Enter the path to the CSV file: ')

# Define the columns to be imported from the CSV file
selected_columns = [0, 1, 5]

df = load_csv_file(csv_file_path, selected_columns)

# Convert the values in amount column from string to float
df.Määrä = df.Määrä.str.replace(',', '.').astype(float)

set_transaction_categories(df, categories)

df['Kategoria'] = set_categories

#set_savings_to_positive(df)

df_categories_total = calculate_total_sum_per_category(df)

monthly_total_sum = calculate_total_monthly_sum(df)

monthly_total_df = pd.DataFrame({'Total': [monthly_total_sum]})


"""
    
    Column names and values are prepared for Google Sheets import

"""

columns = prepare_data_for_google_sheets(df)[0]

values = prepare_data_for_google_sheets(df)[1]

categories_total_columns = prepare_data_for_google_sheets(df_categories_total)[0]

categories_total_values = prepare_data_for_google_sheets(df_categories_total)[1]

monthly_total_column = prepare_data_for_google_sheets(monthly_total_df)[0]

monthly_total_value = prepare_data_for_google_sheets(monthly_total_df)[1]


""" 

    Import the data to Google Sheets

"""

credentials_file_path =  os.getenv('credentials_path')

spreadsheet_name = 'Automated Finance Tracker'

worksheet_name = input('Enter the name of the worksheet: ')


# Load the credentials from the JSON file and set the scopes
credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file'])

client = gspread.Client(auth=credentials)


spreadsheet = client.open(spreadsheet_name)

worksheet = spreadsheet.worksheet(worksheet_name)


worksheet.update(columns + values)

worksheet.update(categories_total_columns + categories_total_values, 'G5')

worksheet.update(monthly_total_column + monthly_total_value, 'H12')


print('Data has been successfully imported to Google Sheets.')