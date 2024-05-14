import configparser

class Config:

    config_file = 'config.ini'

    def __init__(self):
        self.config = configparser.ConfigParser()
        
        
    def create_config(self, config_file) -> None:
        self.config['DEFAULT'] = {'credentials_file_path': r'path_to_service_account_json_file.json',
                                  'source_dir': r'path_to_source_directory',
                                  'dest_dir': r'path_to_destination_directory',
                                  'spreadsheet_name': 'Automated Finance Tracker',
                                  'bank_name': 'Nordea',
                                  'file_prefix': 'KÄYTTÖTILI',
                                  'file_extension': '.csv',
                                  'budgets': {'Säästö': 0.0, 
                                              'Ruoka': 0.0, 
                                              'Laskut': 0.0, 
                                              'Vuokra': 0.0, 
                                              'Muu': 0.0
                                              },
                                  'categories': {"Säästö": ['<SAVINGS_ACCOUNT_NAME>'],
                                                 "Tulo": ['<INCOME_SOURCE>'],
                                                 "Ruoka": ["<SUPERMARKET-X", "SUPERMARKET-Y", "SUPERMARKET-Z"], 
                                                 "Laskut": ["<PHONE>", "<GYM>", "<ELECTRICITY>", "<INTERNET>"],
                                                 "Vuokra": ['<RENT_RECIPIENT>'],
                                                 "Muu": []
                                                 }
                                  }
        
        with open(config_file, 'w') as configfile:
            self.config.write(configfile)

    def read_config(self, config_file) -> dict:
        self.config.read(config_file, encoding='utf-8')
        
        credentials_file_path = self.config.get('DEFAULT', 'credentials_file_path')
        source_dir = self.config.get('DEFAULT', 'source_dir')
        dest_dir = self.config.get('DEFAULT', 'dest_dir')
        spreadsheet_name = self.config.get('DEFAULT', 'spreadsheet_name')
        bank_name = self.config.get('DEFAULT', 'bank_name')
        file_prefix = self.config.get('DEFAULT', 'file_prefix')
        file_extension = self.config.get('DEFAULT', 'file_extension')
        budgets = self.config.get('DEFAULT', 'budgets')
        categories = self.config.get('DEFAULT', 'categories')
        
        config_values = {'credentials_file_path': credentials_file_path,
                         'source_dir': source_dir,
                         'dest_dir': dest_dir,
                         'spreadsheet_name': spreadsheet_name,
                         'bank_name': bank_name,
                         'file_prefix': file_prefix,
                         'file_extension': file_extension,
                         'budgets': budgets,
                         'categories': categories
                         }

        return config_values

    def update_config(self, config_file, section, key, value) -> None:
        self.config.read(config_file)
        self.config.set(section, key, value)
        with open(config_file, 'w') as configfile:
            self.config.write(configfile)
