import gzip 
import json
from tqdm import tqdm
from unidecode import unidecode
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
PATH = "C:/Users/alpye/OneDrive/Desktop/DATA/coalition_3.gz"

cityList = []

with open("data/main_cities_finished_2_WO_guess.json", "r") as file:
    city_data = json.load(file)

with open("data/cities.txt", "r", encoding = "utf-8") as file:
    for line in file:
        line = unidecode(line)
        line = line.strip().lower()
        cityList.append(line)

df = pd.read_excel('data/city_street.xlsx')

ilce_dict = {}
semt_dict = {}
mah_dict = {}

for i, row in df.iterrows():
    main_key = unidecode(row['il'].strip().lower())
    sub_key = unidecode(row['ilçe'].strip().lower())
    sub_sub_key = unidecode(row['semt_bucak_belde'].strip().lower())
    value = (unidecode(row["Mahalle"].strip().lower()))[:-4] # Exlude MAH

    ilce_dict.setdefault(main_key, {}).setdefault(sub_key, 0)
    semt_dict.setdefault(main_key, {}).setdefault(sub_sub_key, 0)
    mah_dict.setdefault(main_key, {}).setdefault(value, 0)

# DISCLAIMER: The values of these dictionaries were useless.
# I realized that while I was making progress...

# Make 3 seperate lists to check in the future

ilce_list = []
semt_list = []
mah_list = []


for i, row in df.iterrows():
    ilce = unidecode(row['ilçe'].strip().lower())
    semt = unidecode(row['semt_bucak_belde'].strip().lower())
    mah = (unidecode(row["Mahalle"].strip().lower()))[:-4] # Exlude the MAH

    if ilce not in ilce_list:
        ilce_list.append(ilce)
    if semt not in semt_list:
        semt_list.append(semt)
    if mah not in mah_list:
        mah_list.append(mah)

def find_main_key(nested_dict, middle_key):
    for main_key, inner_dict in nested_dict.items():
        if middle_key in inner_dict:
            return main_key
    return None


with open('data/user_list_WO_guess.txt', 'r') as file:
    user_list = [int(line.strip()) for line in file]

with open('data/user_list_place_WO_guess.txt', 'r') as file:
    user_place_id = [int(line.strip()) for line in file]

user_geo_id = []


df = gpd.read_file("data/turkey.geojson")

geoCnt = 0
place_idx = 0
userloc_idx = 0
cnt = 0
with gzip.open(PATH, "rt") as fh:
    pbar = tqdm(fh)
    for i in pbar:
        uid, data = i.split("\t") 
        data = json.loads(data) # Makes the json into a Python dictionary
        user_dict = {key: 0 for key in cityList}
        went_in = False
        for tweet in data:
            if user_list[userloc_idx] == tweet["user"]["id"]:
                if userloc_idx < 117677:
                    userloc_idx += 1
                break
            if user_place_id[place_idx] == tweet["user"]["id"]:
                if place_idx < 29218:
                    place_idx += 1
                break
            if tweet["geo"] is not None:
                new_dict = {}
                new_dict["type"] = "Point"
                new_dict["coordinates"] = []
                new_dict["coordinates"].append(tweet["geo"]["coordinates"][1])
                new_dict["coordinates"].append(tweet["geo"]["coordinates"][0])
                
                geometry = Point(new_dict['coordinates'])

                pt = gpd.GeoDataFrame({'geometry': [geometry]})
                pt = pt.set_crs('epsg:4326')

                intersections = gpd.overlay(pt, df, how='intersection', keep_geom_type=False)
                name = intersections["name"]
                if name.empty is False:
                    city = name.iloc[0]
                    city = unidecode(city)
                    city = city.lower()
                    user_dict[city] += 1
                    to_be_appended = tweet["user"]["id"]
                    went_in = True
                    

        if went_in:           
            city = max(user_dict, key = user_dict.get)
            city_data[city] += 1
            geoCnt += 1
            user_geo_id.append(to_be_appended)
            went_in = False
        cnt += 1
        pbar.set_postfix({"Count": cnt, "Successful Count": geoCnt, "UserBioLoc idx": userloc_idx, "TweetPlace idx": place_idx})



with open('data/user_list_geo_WO_guess.txt', 'w') as file:
    for item in user_geo_id:
        file.write(str(item) + '\n')

file_path = 'data/main_cities_finished_3_WO_guess.json'
with open(file_path, 'w') as file:
    json.dump(city_data, file, indent=4)