from move_finance_files import FileMover
from rename_finance_files import FileRenamer
import os

source_dir = r'C:\Users\sambu\Downloads'
dest_dir = r'E:\PythonAutomation\FinanceTracker\Files'
rename_files_dir = os.getcwd() + r'\Files'

bank_name = 'Nordea'
file_prefix = 'KÄYTTÖTILI'
file_extension = '.csv'

file_mover = FileMover(source_dir, dest_dir)
file_renamer = FileRenamer(rename_files_dir, bank_name)


file_mover.move_files(file_extension, file_prefix)
file_renamer.rename_file(file_prefix)