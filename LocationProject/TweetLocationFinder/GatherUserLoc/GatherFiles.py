import json
from unidecode import unidecode
import pandas as pd

class GatherFiles:
    '''Gathers the files necessary for the search'''

    def __init__(self):
        self.ilce_dict = {}
        self.semt_dict = {}
        self.mah_dict = {} # only usage is in EntityExtractor

    def city_parts(self, pathXLSX):
        '''Fills up the 3 empty dictionaries of the initialized GatherFiles object.\n
        Needs path to an xlsx file with 4 columns, named and filled accordingly:\n
        il, ilçe, semt_bucak_belde, Mahalle\n
        This excel sheet can be found on the Github repo
        '''
        df = pd.read_excel(pathXLSX)

        for i, row in df.iterrows():
            main_key = unidecode(row['il'].strip().lower())
            sub_key = unidecode(row['ilçe'].strip().lower())
            sub_sub_key = unidecode(row['semt_bucak_belde'].strip().lower())

            value = (unidecode(row["Mahalle"].strip().lower())) # Exlude MAH + things like "X MAH (A KÖYÜ)"
            idx = value.find("(")
            if idx > -1:
                value = value[:idx]
                value = value[:-1]
                if value[:-1] == " ":
                    value = value[:-1]
            value = value[:-4]

            self.ilce_dict.setdefault(main_key, {}).setdefault(sub_key, 0)
            self.semt_dict.setdefault(main_key, {}).setdefault(sub_sub_key, 0)
            self.mah_dict.setdefault(main_key, {}).setdefault(value, 0)
        
        return

    def city_list_and_data(self, cities_path, data_path_json = None):
        '''Returns a list with all city names, writes into a JSON file with all cities as keys and all their values to 0'''
        cityList = []
        with open(cities_path, "r", encoding = "utf-8") as file:
            for line in file:
                line = unidecode(line)
                line = line.strip().lower()
                cityList.append(line)
        
        if data_path_json is not None:
            data_dict = {key: 0 for key in cityList}
            with open(data_path_json, 'w') as file:
                json.dump(data_dict, file, indent=4)

        return cityList

    # To get that city data dictionary
    def get_city_data(self, path):
        '''Getter function for city data\n
        Note: city data is a json file/dictionary which has cities as keys and\n
        an integer (user count) as value'''
        with open(path, "r") as file:
            city_data = json.load(file)
        return city_data