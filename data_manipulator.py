import pandas as pd
import os

class DataManipulator:
    """

    A class for manipulating the data from the CSV files.

    """
    def __init__(self, categories: dict, finance_file_folder: str ) -> None:
        self.categories = categories
        self.finance_file_folder = finance_file_folder
        self.set_categories = []
        self.chosen_csv_files_paths = []
        self.csv_files = []

    def set_transaction_categories(self, df) -> None: 
        for title in df['Otsikko']:
            category_set = False
            for category, keywords in self.categories.items():
                for keyword in keywords:
                    if keyword in title:
                        self.set_categories.append(category)
                        category_set = True
                        break
                    
            if not category_set:
                self.set_categories.append('Muu')
        
        return self.set_categories

    @staticmethod
    def set_savings_to_positive(df) -> None:
        for index, row in df.iterrows():
            if row['Kategoria'] == 'Säästö':
                df.at[index, '+-'] = df.at[index, '+-'] * -1

    @staticmethod
    def calculate_total_sum(df, column_name: str) -> float:
        return df[column_name].sum()
    
    @staticmethod
    def calculate_total_sum_per_category(df) -> pd.DataFrame:
        return df.groupby('Kategoria')['Määrä'].sum().reset_index()

    @staticmethod
    def calculate_total_income_sum(df) -> float:
        return df[df['Kategoria'] == 'Tulo']['Määrä'].sum()
    
    @staticmethod
    def load_csv_file(csv_file_path: list, selected_columns: list) -> pd.DataFrame:
        return pd.read_csv(csv_file_path, delimiter=';', usecols=selected_columns)
    
    def csv_files_to_manipulate(self) -> list:
        number_of_files_to_manipulate = int(input('Enter the number of CSV files to manipulate: ')) 
        for file in os.scandir(self.finance_file_folder):
            self.csv_files.append(file.path)
        for _ in range(number_of_files_to_manipulate):
            self.chosen_csv_files_paths.append(self.csv_files[-1])
            self.csv_files.pop(-1)
        return self.chosen_csv_files_paths
    
    

    