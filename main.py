from move_finance_files import FileMover
from rename_finance_files import FileRenamer
from finance_tracker import FinanceTracker
from data_manipulator import DataManipulator
from data_inserter import DataInserter
from config import Config
import os
import time

def main():
    cfg = Config()

    if os.path.exists(cfg.config_file):
        config_values = cfg.read_config(cfg.config_file)
    else:
        cfg.create_config(cfg.config_file)
        time.sleep(1)
        config_values = cfg.read_config(cfg.config_file)
    
    source_dir = config_values.get('source_dir')  
    dest_dir = config_values.get('dest_dir')
    rename_files_dir = os.getcwd() + r'\Files'

    bank_name = config_values.get('bank_name')
    file_prefix = config_values.get('file_prefix')
    file_extension = config_values.get('file_extension')

    credentials_file_path =  config_values.get('credentials_file_path')
    spreadsheet_name = config_values.get('spreadsheet_name')
    categories = eval(config_values.get('categories'))
    finance_file_folder = os.getcwd() + '\Files'
    file_mover = FileMover(source_dir, dest_dir)
    file_renamer = FileRenamer(rename_files_dir, bank_name)
    file_mover.move_files(file_extension, file_prefix)
    file_renamer.rename_file(file_prefix)

    finance_tracker = FinanceTracker(credentials_file_path, spreadsheet_name, categories)
    client = finance_tracker.initialize_client()
    finance_tracker.budgets = eval(config_values.get('budgets'))
    budgets_df = finance_tracker.create_budgets_df()
    data_manipulator = DataManipulator(categories, finance_file_folder)
    chosen_csv_files_paths = data_manipulator.csv_files_to_manipulate()
    data_inserter = DataInserter(client, spreadsheet_name, chosen_csv_files_paths, budgets_df)
    data_inserter.insert_data_to_google_sheets(data_manipulator)

if __name__ == '__main__':
    main()