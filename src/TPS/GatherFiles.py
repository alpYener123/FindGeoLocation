import json
from unidecode import unidecode
import pandas as pd


class GatherFiles:
    """Gathers the files necessary for the search"""

    def __init__(self, path_excel, cities_path):
        self.path_excel = path_excel
        self.cities_path = cities_path

        self.ilce_dict = {}
        self.semt_dict = {}

        self.create_district_mappings(path_excel)
        self.cities = self.get_preprocessed_city_names(cities_path)

    def create_district_mappings(self, path_excel):
        """Fills up the 3 empty dictionaries of the initialized GatherFiles object.\n
        Needs path to an xlsx file with 4 columns, named and filled accordingly:\n
        il, ilçe, semt_bucak_belde, Mahalle\n
        This excel sheet can be found on the Github repo
        """
        df = pd.read_excel(path_excel)

        for _, row in df.iterrows():
            main_key = unidecode(row["il"].strip().lower())
            sub_key = unidecode(row["ilçe"].strip().lower())
            sub_sub_key = unidecode(row["semt_bucak_belde"].strip().lower())

            value = unidecode(
                row["Mahalle"].strip().lower()
            )  # Exlude MAH + things like "X MAH (A KÖYÜ)"
            idx = value.find("(")
            if idx > -1:
                value = value[:idx]
                value = value[:-1]
                if value[:-1] == " ":
                    value = value[:-1]
            value = value[:-4]

            self.ilce_dict.setdefault(main_key, {}).setdefault(sub_key, 0)
            self.semt_dict.setdefault(main_key, {}).setdefault(sub_sub_key, 0)

    def get_preprocessed_city_names(self, cities_path):
        """Returns a list with all preprocessed city names"""
        cities = []
        with open(cities_path, "r", encoding="utf-8") as file:
            for line in file:
                line = unidecode(line)
                line = line.strip().lower()
                cities.append(line)
        return cities
