import json
from unidecode import unidecode
import pandas as pd

class GatherFiles:

    def __init__(self):
        self.ilce_dict = {}
        self.semt_dict = {}
        self.mah_dict = {}

    # An excel with with il, ilçe, semt, mahalle information for each row, for each mahalle
    def city_parts(self, pathXLSX):
        df = pd.read_excel(pathXLSX)

        for i, row in df.iterrows():
            main_key = unidecode(row['il'].strip().lower())
            sub_key = unidecode(row['ilçe'].strip().lower())
            sub_sub_key = unidecode(row['semt_bucak_belde'].strip().lower())

            value = (unidecode(row["Mahalle"].strip().lower())) # Exlude MAH + things like "X MAH (A KÖYÜ)"
            idx = value.find("(")
            if idx > -1:
                value = value[:idx]
            value = value[:-4]

            self.ilce_dict.setdefault(main_key, {}).setdefault(sub_key, 0)
            self.semt_dict.setdefault(main_key, {}).setdefault(sub_sub_key, 0)
            self.mah_dict.setdefault(main_key, {}).setdefault(value, 0)
        
        return

    # Returns a list with all city names, writes into a JSON file with all cities as keys and all their values to 0
    def city_list_and_data(self, citypathTXT, datapathJSON = None):
        cityList = []
        with open(citypathTXT, "r", encoding = "utf-8") as file:
            for line in file:
                line = unidecode(line)
                line = line.strip().lower()
                cityList.append(line)
        
        if datapathJSON is not None:
            data_dict = {key: 0 for key in cityList}
            with open(datapathJSON, 'w') as file:
                json.dump(data_dict, file, indent=4)

        return cityList

    # To get that city data dictionary
    def get_city_data(self, path):
        with open(path, "r") as file:
            city_data = json.load(file)
        return city_data


def back_to_forward_slash(path):
    correct_path = ""
    for i in path:
        if i == '\\':
            i = '/'
        correct_path += i
    return correct_path