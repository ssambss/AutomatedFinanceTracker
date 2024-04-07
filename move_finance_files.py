import shutil
from pathlib import Path


"""

Move files from the current working directory to a destination directory.

"""
source_dir = Path.cwd()
dest_dir = Path(r'E:\PythonAutomation\FinanceTracker\Files')

for file in source_dir.glob('*.csv'):
    if file.name.startswith('KÄYTTÖTILI'):
        shutil.move(file, dest_dir)
        print(f'{file} moved to {dest_dir}')