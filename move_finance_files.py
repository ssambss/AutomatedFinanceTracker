import shutil
from pathlib import Path

class FileMover:    
    """
    
    Move files from the source directory to a destination directory.
    
    """
    
    def __init__(self, source_dir: str, dest_dir: str) -> None:
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
    
    def move_files(self, file_extension: str, file_prefix: str) -> None:
        bank_csv = False
        for file in self.source_dir.glob(f'*{file_extension}'):
            if file.name.startswith(file_prefix):
                shutil.move(file, self.dest_dir)
                print(f'{file} moved to {self.dest_dir}!')
                bank_csv = True
        
        if not bank_csv:
            print(f'No files with prefix {file_prefix} found.')
