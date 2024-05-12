from move_finance_files import FileMover
from rename_finance_files import FileRenamer
from finance_tracker import FinanceTracker
from data_manipulator import DataManipulator
from data_inserter import DataInserter
import os


def main():
    source_dir = r'C:\Users\sambu\Downloads'
    dest_dir = r'E:\PythonAutomation\FinanceTracker\Files'
    rename_files_dir = os.getcwd() + r'\Files'

    bank_name = 'Nordea'
    file_prefix = 'KÄYTTÖTILI'
    file_extension = '.csv'

    credentials_file_path =  os.getenv('credentials_path')
    spreadsheet_name = 'Automated Finance Tracker'
    categories = {"Säästö": [os.getenv('saving_account')],
                "Tulo": [os.getenv('salary')],
                "Ruoka": ["LIDL", "K-MARKET", "K-CITYMARKET", "PRISMA", "S-MARKET", "K-SUPERMARKET", "ALEPA", "SALE"], 
                "Laskut": ["ELISA", "SATS", "VIHREÄ ÄLYENERGIA", "DNA", "SPOTIFY", "INSINÖÖRILIITTO", "Keskinäinen Vakuutusyhtiö", "Helen Oy", "SANOMA"],
                "Vuokra": [os.getenv('rent')],
                "Muu": []
                }
    finance_file_folder = os.getcwd() + '\Files'
    file_mover = FileMover(source_dir, dest_dir)
    file_renamer = FileRenamer(rename_files_dir, bank_name)
    file_mover.move_files(file_extension, file_prefix)
    file_renamer.rename_file(file_prefix)

    finance_tracker = FinanceTracker(credentials_file_path, spreadsheet_name, categories)
    client = finance_tracker.initialize_client()
    budgets = finance_tracker.define_budgets()
    budgets_df = finance_tracker.create_budgets_df()

    data_manipulator = DataManipulator(categories, budgets, finance_file_folder)
    chosen_csv_files_paths = data_manipulator.csv_files_to_manipulate()
    data_inserter = DataInserter(client, spreadsheet_name, chosen_csv_files_paths, budgets_df)
    data_inserter.insert_data_to_google_sheets(data_manipulator)

if __name__ == '__main__':
    main()