import json
from unidecode import unidecode
import pandas as pd

class GatherFiles:

    def __init__(self):
        self.ilce_dict = {}
        self.semt_dict = {}
        self.mah_dict = {}
        
        self.ilce_list = []
        self.semt_list = []
        self.mah_list = []

    # An excel with with il, ilçe, semt, mahalle information for each row, for each mahalle
    def city_parts(self, pathXLSX): # ---> OK
        df = pd.read_excel(pathXLSX)

        for i, row in df.iterrows():
            main_key = unidecode(row['il'].strip().lower())
            sub_key = unidecode(row['ilçe'].strip().lower())
            sub_sub_key = unidecode(row['semt_bucak_belde'].strip().lower())
            value = (unidecode(row["Mahalle"].strip().lower()))[:-4] # Exlude MAH

            self.ilce_dict.setdefault(main_key, {}).setdefault(sub_key, 0)
            self.semt_dict.setdefault(main_key, {}).setdefault(sub_sub_key, 0)
            self.mah_dict.setdefault(main_key, {}).setdefault(value, 0)

            if sub_key not in self.ilce_list:
                self.ilce_list.append(sub_key)
            if sub_sub_key not in self.semt_list:
                self.semt_list.append(sub_sub_key)
            if value not in self.mah_list:
                self.mah_list.append(value)
        
        return
    


#Find the main key in a nested dictionary (of 2 dictionaries)
def find_city(nested_dict, middle_key): # --> OK
    for main_key, inner_dict in nested_dict.items():
        if middle_key in inner_dict:
            return main_key
    return None

# Reads and turns the JSON file into a dictionary. The file can be found at "/data/populations.json"
def get_populations(pathJSON): # --> OK
    with open(pathJSON, "r", encoding="utf-8") as file:
        populations = json.load(file)
    return populations


# Get a file with the cities, one city per line
# Writes a JSON file with the cities, all valued to 0
# Returns that JSON file as a dictionary
def create_city_list(pathTXT): # --> OK
    cityList = []
    with open(pathTXT, "r", encoding = "utf-8") as file:
        for line in file:
            line = unidecode(line)
            line = line.strip().lower()
            cityList.append(line)
    return cityList

def create_city_data(cityList, pathJSON):
    data_dict = {key: 0 for key in cityList}
    with open(pathJSON, 'w') as file:
        json.dump(data_dict, file, indent=4)
    return data_dict

def get_city_data(path):
    with open(path, "r") as file:
        city_data = json.load(file)
    return city_data