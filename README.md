# Finance Tracker

This project is a finance tracker that automates the process of importing and analyzing financial data from CSV files. It uses the Google Sheets API to import the data into a Google Sheets spreadsheet and perform calculations on the data.

---

## Features

- **Expense Tracking**: Automatically track expenses and savings from bank transactions csv files.
- **Moving and renaming transaction files**: Automatically moves transaction files from e.g. downloads inside the project's "Files" -folder and renames them <bank-year-month>.
- **Budgeting**: Set up budgets for different spending categories and track your expenses against them.

### Could be added
- **Financial Reports**: Generate detailed reports to analyze spending patterns, identify areas for improvement, and make informed financial decisions.
- **Formatting**: Color cells based on values (e.g. if food category's budget has gone over for the month, color it red).

---

### Prerequisites

#### Python version and requirements

- Python 3.10.3 or newer.
- Open cmd and navigate to the directory where you have downloaded this project. Use command "pip install -r requirements.txt" to install dependencies.

#### Creating a Google Project

Here's how to setup a Google project for this to work.

1. Create A Google Spreadsheet and name it "Automated Finance Tracker".
2. Head to https://console.developers.google.com/ and create a new project. Once you have created the project, search for APIs & Services.
3. Find the "ENABLE APIS AND SERVICES" button and click it.
4. Search for “Google Drive API” and “Google Sheets API”, enable both.
5. From APIs & Services go to "Credentials” and click "Create credentials" -> "Service account".
6. Fill out the form in step 1, steps 2 and 3 can be left blank.
7. Find the "Manage service accounts" button and click it.
8. Press the three dot button under the "Actions" label and select "Manage Keys".
9. Press "Add Key" and "Create new key".
10. Select JSON key type and press "Create". A JSON file will be downloaded, save it somewhere on your environment.
11. Go to your spreadsheet and share it with the client_email you have in the downloaded JSON file.

#### Filling out the Config class with wanted information

1. Open the "config_example.py" file and name it "config.py".
2. Look for the "create_config" function and replace the example values with your own values where needed:
   ![image](https://github.com/ssambss/AutomatedFinanceTracker/assets/61969837/2558f197-2c31-4ca8-8776-e620f6c27b39)
3. "Muu" can be left empty, whatever is not specified in the other categories will be added to this category.

---

## Usage

1. Open a command line and navigate to the project directory.
2. Use command "python main.py" to run the program.
   
#### What happens
1. A config file based on the values you entered above will be created if such file does not yet exist.
2. Specified csv files will be moved inside the project folder under \Files and renamed <bank-year-month>.
3. You will be asked to specify the amount of csv files that should be manipulated and inserted (typing 1 and pressing Enter means only the latest csv file is inserted to Google Sheets).
4. Data is prepared for insertion.
5. Worksheet named YYYY-MM is created if such worksheet does not yet exist.
6. Data is inserted into the corresponding worksheet.
7. If more than 1 files were chosen, steps 4-6 will be repeated.





