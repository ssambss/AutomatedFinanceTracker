import re
import pandas as pd
from data_manipulator import DataManipulator

class DataInserter:
    """
    
    A class to insert data to Google Sheets.
    
    """
    set_categories = []   

    def __init__(self, client, spreadsheet_name: str, chosen_csv_files_paths: list, budgets_df) -> None:
        self.client = client
        self.spreadsheet_name = spreadsheet_name
        self.chosen_csv_files_paths = chosen_csv_files_paths
        self.selected_columns = [0, 1, 5]
        self.budgets_df = budgets_df  

    @staticmethod
    def prepare_data_for_google_sheets(df) -> list:
        columns = [df.columns.values.tolist()]
        values = df.values.tolist()
        return columns, values
    
    def create_df_categories_total(self, df, dm) -> pd.DataFrame:
        df_categories_total = dm.calculate_total_sum_per_category(df)
        df_categories_total = df_categories_total[df_categories_total['Kategoria'] != 'Tulo']
        df_categories_total = pd.merge(self.budgets_df, df_categories_total, on='Kategoria', how='left').fillna(0)
        df_categories_total = df_categories_total[['Kategoria', 'Budget', 'Määrä']]
        df_categories_total['+-'] = df_categories_total['Budget'] + df_categories_total['Määrä']
        dm.set_savings_to_positive(df_categories_total)

        return df_categories_total
    
    @staticmethod
    def create_df_total(df, dm, column1, column2) -> pd.DataFrame:
        total_sum = dm.calculate_total_sum(df, column1)
        df_monthly_total = pd.DataFrame({column2: [total_sum]})
        return df_monthly_total
    
    @staticmethod
    def create_df_income_total(df, dm) -> pd.DataFrame:
        income_total_sum = dm.calculate_total_income_sum(df)
        df_income_total = pd.DataFrame({'Tulo': [income_total_sum]})
        return df_income_total
    

    def insert_data_to_google_sheets(self, data_manipulator) -> None:
        dm = data_manipulator
        for i in range(len(self.chosen_csv_files_paths)):
            df = dm.load_csv_file(self.chosen_csv_files_paths[i], self.selected_columns)
            df.Määrä = df.Määrä.str.replace(',', '.').astype(float)
            set_categories = dm.set_transaction_categories(df)
            df['Kategoria'] = set_categories
                
            df_categories_total = self.create_df_categories_total(df, dm)
            df_monthly_total = self.create_df_total(df, dm, 'Määrä', 'Total')
            df_budget_total = self.create_df_total(df_categories_total, dm, '+-', 'Budget Total')
            df_income_total = self.create_df_income_total(df, dm)
            df_expenses_total = self.create_df_total(df_categories_total, dm, 'Määrä', 'Menot')

            df_combined = pd.concat([df_income_total, df_expenses_total, df_monthly_total], axis=1)
    
            columns = self.prepare_data_for_google_sheets(df)[0]
            values = self.prepare_data_for_google_sheets(df)[1]
            categories_total_columns = self.prepare_data_for_google_sheets(df_categories_total)[0]
            categories_total_values = self.prepare_data_for_google_sheets(df_categories_total)[1]
            budget_total_column = self.prepare_data_for_google_sheets(df_budget_total)[0]
            budget_total_values = self.prepare_data_for_google_sheets(df_budget_total)[1]
            total_combined_columns = self.prepare_data_for_google_sheets(df_combined)[0]
            total_combined_values = self.prepare_data_for_google_sheets(df_combined)[1]
    
            file_name_stripped = self.chosen_csv_files_paths[i].split('\\')[-1].split('.')[0]
            worksheet_name = re.findall(r'\d+-\d+', file_name_stripped)[0]
            spreadsheet = self.client.open(self.spreadsheet_name)
            if worksheet_name in [sheet.title for sheet in spreadsheet.worksheets()]:
                worksheet = spreadsheet.worksheet(worksheet_name)
            else:    
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows='100', cols='20')
            worksheet.update(columns + values)
            worksheet.update(categories_total_columns + categories_total_values, 'G5')
            worksheet.update(budget_total_column + budget_total_values, 'J12')
            worksheet.update(total_combined_columns + total_combined_values, 'G12')

            worksheet.update([['Toteutunut']], 'G3')
            print(f'Data for {worksheet_name} has been successfully imported to Google Sheets.')
    
            set_categories.clear()