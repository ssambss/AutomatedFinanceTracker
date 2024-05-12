from pathlib import Path
import re

class FileRenamer:
    """

    Rename transaction csv files in a directory to BANK-YYYY-MM.csv format.
    
    """
    def __init__(self, root_dir: str, bank_name: str) -> None:
        self.root_dir = Path(root_dir)
        self.bank_name = bank_name

    def rename_file(self, file_prefix: str) -> None:
        for file in self.root_dir.iterdir():
            if file.name.startswith(file_prefix):
                year_and_month = re.findall(r'\d+-\d+', file.name)
                new_stem = f'{self.bank_name}' + '-' +  year_and_month[0]
                new_name = new_stem + file.suffix
                new_filepath = file.with_name(new_name)
                file.rename(new_filepath)
                print(f'{file.name} renamed to {new_name}!')
                
        

