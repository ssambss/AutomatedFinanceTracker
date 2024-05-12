import gspread
import pandas as pd
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

class FinanceTracker:
    """
    
    A class to initialize gspread client and budgets.
    
    """

    def __init__(self, credentials_file_path: str, spreadsheet_name: str, categories: dict) -> None:
        self.credentials_file_path = credentials_file_path
        self.spreadsheet_name = spreadsheet_name
        self.categories = categories
        self.budgets = {}

    def initialize_client(self) -> gspread.Client:
        credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path, 
                                                                            scopes=['https://www.googleapis.com/auth/spreadsheets', 
                                                                                    'https://www.googleapis.com/auth/drive', 
                                                                                    'https://www.googleapis.com/auth/drive.file'])
        return gspread.Client(auth=credentials)
    
    def define_budgets(self) -> None:
        for category in self.categories.keys():
            if category == 'Tulo':
                continue
            budget = float(input(f'Enter the budget for {category}: '))
            self.set_budget_for_category(category, budget)        

    def set_budget_for_category(self, category: str, budget: float) -> None:    
        self.budgets.update({category: budget})

    def create_budgets_df(self) -> pd.DataFrame:
        budgets_df = pd.DataFrame(self.budgets.items(), columns=['Kategoria', 'Budget']).sort_values('Kategoria')
        return budgets_df


    


