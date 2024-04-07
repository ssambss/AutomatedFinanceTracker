from pathlib import Path
from datetime import datetime as dt
import re

root_dir = Path(str(Path.cwd()) + r'\Files')
bank_name = 'Nordea'

def rename_file() -> None:

    for file in root_dir.iterdir():
        if file.name.startswith('KÄYTTÖTILI'):
            year_and_month = re.findall(r'\d+-\d+', file.name)
            new_stem = f'{bank_name}' + '-' +  year_and_month[0]
            new_name = new_stem + file.suffix
            new_filepath = file.with_name(new_name)
            file.rename(new_filepath)
            print(f'{file.name} renamed to {new_name}')


rename_file()