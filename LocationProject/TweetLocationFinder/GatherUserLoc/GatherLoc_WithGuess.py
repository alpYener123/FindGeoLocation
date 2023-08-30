from .GatherFiles import find_city, get_populations, create_city_list, process_kwargs, find_cities, lower_unidecode
import gzip 
import json
from tqdm import tqdm
from unidecode import unidecode
from shapely.geometry import Point
import geopandas as gpd

class GatherLoc_Guess:

    def __init__(self, ilce_dict, semt_dict, mah_dict, populationPATH, cityPATH):
        self.ilce_dict = ilce_dict
        self.semt_dict = semt_dict
        self.mah_dict = mah_dict
        self.populations = get_populations(populationPATH)
        self.cityList = create_city_list(cityPATH)
    
    @staticmethod
    def _guess(self, l):
        final = 0
        final_idx = -1
        for i in l:
            idx = self.cityList.index(i)
            pop = self.populations[idx]["population"]
            if final < pop:
                final = pop
                final_idx = idx
        city = self.cityList[final_idx]
        return city


    # Gets the location data on the ["user"]["location"] part of the metadata
    @staticmethod
    def get_user_loc(self, city_data, PATH, result_path_JSON, gathered_user_list_path_TXT, **kwargs):
        
        kwargs_count = len(kwargs)
        if kwargs_count > 2:
            print("Too many additional arguments. 1 or 2 lists are allowed!")
            return
        
        a = None
        b = None

        check = 0
        if kwargs_count > 0:
            checklist = process_kwargs(**kwargs)
            if checklist is not False:
                if len(checklist) == 2:
                    a = 0
                    check = 1
                else:
                    a = 0
                    b = 0
                    check = 2

        user_list = []
        memberCNT = 0
        cnt = 0

        with gzip.open(PATH, "rt") as fh:
            pbar = tqdm(fh)
            for i in pbar:
                uid, data = i.split("\t") 
                data = json.loads(data) # Makes the json into a Python dictionary
                for tweet in data:

                    if check == 1 or check == 2:
                        if tweet["user"]["id"] == checklist[1][a]:
                            if a < checklist[0]:
                                a += 1
                            break
                    if check == 2:
                        if tweet["user"]["id"] == checklist[3][b]:
                            if b < checklist[2]:
                                b += 1
                            break


                    if tweet["user"]["location"] != '':
                        loc = lower_unidecode(tweet["user"]["location"])

                        common_elements = set(loc).intersection(self.cityList)    
                        if common_elements:
                            city = list(common_elements)[0]
                            city_data[city] += 1
                            memberCNT += 1
                            user_list.append(tweet["user"]["id"])
                            break                                                          
                        
                        else:
                            common_elements = []

                            for item in loc:
                                l = find_cities(self.ilce_dict, item)
                                if isinstance(l, list):
                                    common_elements += l
                            
                            if len(common_elements) > 0:
                                if len(common_elements) > 1:
                                    city = self._guess(self, common_elements)
                                else:
                                    city = common_elements[0]
                                
                                city_data[city] += 1
                                memberCNT += 1
                                user_list.append(tweet["user"]["id"])
                                break
                            
                            else:
                                common_elements = []

                                for item in loc:
                                    l = find_cities(self.semt_dict, item)
                                    if isinstance(l, list):
                                        common_elements += l
                                
                                if len(common_elements) > 0:
                                    if len(common_elements) > 1:
                                        city = self._guess(self, common_elements)
                                    else:
                                        city = common_elements[0]
                                    
                                    city_data[city] += 1
                                    memberCNT += 1
                                    user_list.append(tweet["user"]["id"])
                                    break

                                else:
                                    common_elements = []

                                    for item in loc:
                                        l = find_cities(self.mah_dict, item)
                                        if isinstance(l, list):
                                            common_elements += l
                                    
                                    if len(common_elements) > 0:
                                        if len(common_elements) > 1:
                                            city = self._guess(self, common_elements)
                                        else:
                                            city = common_elements[0]
                                        
                                        city_data[city] += 1
                                        memberCNT += 1
                                        user_list.append(tweet["user"]["id"])
                                        break
                    
                cnt += 1
                pbar.set_postfix({"Count": cnt, "Successful Count": memberCNT , "List1 idx": a, "List2 idx":b })

        with open(result_path_JSON, 'w') as file:
            json.dump(city_data, file, indent=4)

        with open(gathered_user_list_path_TXT, 'w') as file:
            for item in user_list:
                file.write(str(item) + '\n')


    # Gets the location data on the ["place"]["full_name"] part of the metadata
    @staticmethod
    def get_tweet_loc(self, city_data, PATH, result_path_JSON, gathered_user_list_path_TXT, **kwargs):
        user_place_id = []
        
        kwargs_count = len(kwargs)
        if kwargs_count > 2:
            print("Too many additional arguments. 1 or 2 lists are allowed!")
            return

        a = None
        b = None

        check = 0
        if kwargs_count > 0:
            checklist = self._process_kwargs(**kwargs)
            if checklist is not False:
                if len(checklist) == 2:
                    a = 0
                    check = 1
                else:
                    a = 0
                    b = 0
                    check = 2

        memberCNT = 0
        cnt = 0
        with gzip.open(PATH, "rt") as fh:
            pbar = tqdm(fh)
            for i in pbar:
                uid, data = i.split("\t") 
                data = json.loads(data) # Makes the json into a Python dictionary
                user_dict = {key: 0 for key in self.cityList}
                went_in = False
                for tweet in data:

                    if check == 1 or check == 2:
                        if tweet["user"]["id"] == checklist[1][a]:
                            if a < checklist[0]:
                                a += 1
                            break
                    if check == 2:
                        if tweet["user"]["id"] == checklist[3][b]:
                            if b < checklist[2]:
                                b += 1
                            break

                    else:
                        if tweet["place"] is not None:
                            loc = lower_unidecode(tweet["user"]["location"])


                            common_elements = set(loc).intersection(self.cityList)
                            if common_elements:
                                city = list(common_elements)[0]
                                user_dict[city] += 1
                                went_in = True
                                to_be_appended = tweet["user"]["id"]
                                
                            else:
                                common_elements = []

                                for item in loc:
                                    l = find_cities(self.ilce_dict, item)
                                    if isinstance(l, list):
                                        common_elements += l
                                
                                if len(common_elements) > 0:
                                    if len(common_elements) > 1:
                                        city = self._guess(self, common_elements)
                                    else:
                                        city = common_elements[0]
                                    
                                    user_dict[city] += 1
                                    went_in = True
                                    to_be_appended = tweet["user"]["id"]
                                
                                else:
                                    common_elements = []

                                    for item in loc:
                                        l = find_cities(self.semt_dict, item)
                                        if isinstance(l, list):
                                            common_elements += l
                                    
                                    if len(common_elements) > 0:
                                        if len(common_elements) > 1:
                                            city = self._guess(self, common_elements)
                                        else:
                                            city = common_elements[0]
                                        
                                        user_dict[city] += 1
                                        went_in = True
                                        to_be_appended = tweet["user"]["id"]
                                        

                                    else:
                                        common_elements = []

                                        for item in loc:
                                            l = find_cities(self.mah_dict, item)
                                            if isinstance(l, list):
                                                common_elements += l
                                        
                                        if len(common_elements) > 0:
                                            if len(common_elements) > 1:
                                                city = self._guess(self, common_elements)
                                            else:
                                                city = common_elements[0]
                                            
                                            user_dict[city] += 1
                                            went_in = True
                                            to_be_appended = tweet["user"]["id"]


                if went_in:           
                    city = max(user_dict, key = user_dict.get)
                    city_data[city] += 1
                    memberCNT += 1
                    user_place_id.append(to_be_appended)
                    went_in = False                            
                                        
                cnt += 1
                pbar.set_postfix({"Count": cnt, "Successful Count": memberCNT, "List1 idx": a, "List2 idx":b })  
        
        with open(result_path_JSON, 'w') as file:
            json.dump(city_data, file, indent=4)

        with open(gathered_user_list_path_TXT, 'w') as file:
            for item in user_place_id:
                file.write(str(item) + '\n')

    # Gets the location data on the ["geo"] part of the metadata
    @staticmethod
    def get_tweet_coord(self, city_data, PATH, turkey_geoJSON_path, result_path_JSON, gathered_user_list_path_TXT, **kwargs): 
        user_geo_id = []

        df = gpd.read_file(turkey_geoJSON_path)

        kwargs_count = len(kwargs)
        if kwargs_count > 2:
            print("Too many additional arguments. 1 or 2 lists are allowed!")
            return
        
        a = None
        b = None
        
        check = 0
        if kwargs_count > 0:
            checklist = self._process_kwargs(**kwargs)
            if checklist is not False:
                if len(checklist) == 2:
                    a = 0
                    check = 1
                else:
                    a = 0
                    b = 0
                    check = 2

        geoCnt = 0
        cnt = 0
        with gzip.open(PATH, "rt") as fh:
            pbar = tqdm(fh)
            for i in pbar:
                uid, data = i.split("\t") 
                data = json.loads(data) # Makes the json into a Python dictionary
                user_dict = {key: 0 for key in self.cityList}
                went_in = False
                for tweet in data:
                    if check == 1 or check == 2:
                        if tweet["user"]["id"] == checklist[1][a]:
                            if a < checklist[0]:
                                a += 1
                            break
                    if check == 2:
                        if tweet["user"]["id"] == checklist[3][b]:
                            if b < checklist[2]:
                                b += 1
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
                pbar.set_postfix({"Count": cnt, "Successful Count": geoCnt, "List1 idx": a, "List2 idx": b })
        
        with open(result_path_JSON, 'w') as file:
            json.dump(city_data, file, indent=4)

        with open(gathered_user_list_path_TXT, 'w') as file:
            for item in user_geo_id:
                file.write(str(item) + '\n')

