import gzip 
import json
from tqdm import tqdm
from unidecode import unidecode
from shapely.geometry import Point
import geopandas as gpd
import os
from datetime import datetime, timedelta
from collections import defaultdict
import re
from glob import glob

class GatherLoc:
    """Gathers locations of twitter users\n
    Data has to be collected via Twitter API v1\n
    3 main methods to obtain 3 different possible location information in the metadata\n
    get_user_loc --> Gets the location data on the ["user"]["location"] part of the metadata\n
    get_tweet_loc --> Gets the location data on the ["place"]["full_name"] part of the metadata\n
    get_tweet_coord --> Gets the location data on the ["geo"] part of the metadata by reverse geocoding\n
    Important notes: The tweets from a user must be sequential for V1 (explain better). And, kwargs must be gathered from the same dataset\n
    """

    def __init__(self, gather_files, population_path=None):
        """If guess feature is going to be used, population_path cannot be None\n
        Example population_path file is on Github"""
        self.ilce2city_mapper = gather_files.ilce_dict
        self.semt2city_mapper = gather_files.semt_dict
        if population_path is not None:
            self.city2population = self._get_populations(population_path)
        self.city_data = {key: 0 for key in gather_files.cities}

    # Check if the path exists and is readable
    def _is_valid_read_path(self, path):
        return os.path.exists(path) and os.access(path, os.R_OK)

    # Check if the path is writable (create a temporary file)
    def _is_valid_write_path(self, path):
        # Check if the path is writable (create a temporary file)
        try:
            with open(path, "w"):
                pass
            os.remove(path)  # Remove the temporary file
            return True
        except (PermissionError, FileNotFoundError):
            return False

    # Will be used if pop_bias=True
    # Guesses which city the user is according to the city population
    def _guess(self, possible_city_names: list):
        selected_cities = [(c, self.city2population[c]) for c in possible_city_names]
        selected_cities.sort(key=lambda x: x[1])
        return selected_cities[-1][0]

    def _get_populations(self, pathJSON):

        # A getter function for populations
        with open(pathJSON, "r", encoding="utf-8") as file:
            populations = json.load(file)

        city2population = {unidecode(item["name"]).lower(): item["population"] for item in populations}

        return city2population

    def _city_search(self, mapping, location_candidates):
        found_cities = set()
        for target_string in location_candidates:
            for city, value in mapping.items():
                if target_string in value:
                    found_cities.add(city)
        return found_cities

    def _return_city(self, location_candidates, mapping, use_population_bias):
        found_cities = self._city_search(mapping, location_candidates)
        found_cities = list(found_cities)

        if use_population_bias is True and len(found_cities) > 1:
            return self._guess(found_cities)

        if len(found_cities) == 1:
            return found_cities[0]

        return None

    # If there are kwargs in the user-called function, they are formatted as such
    @staticmethod
    def _process_kwargs(**kwargs):  # TODO CHANGE THIS SHIT
        return_list = []
        for key, value in kwargs.items():
            if isinstance(value, list):
                my_dict = {item: None for item in value}
                return_list.append(len(value) - 1)
                return_list.append(my_dict)
            else:
                return False
        return return_list

    # Normalizes the location information by lowering and unidecoding

    def _lower_unidecode(self, tweet):
        # Styling up the tweet location
        loc = unidecode(tweet.strip())
        loc = loc.lower()
        locations = re.split(r"\/|,|-|\s+", loc)
        locations = [loc for loc in locations if loc != ""]

        # Added this part to find the cities correctly
        location_candidates = []
        for item in locations:
            if "maras" in item and "kahramanmaras" not in item:
                item = item.replace("maras", "kahramanmaras")
            elif "afyon" in item and "afyonkarahisar" not in item:
                item = item.replace("afyon", "afyonkarahisar")
            elif "urfa" in item and "sanliurfa" not in item:
                item = item.replace("urfa", "sanliurfa")

            location_candidates.append(item)

        return location_candidates

    # Date functions
    def _add_sub_date(self, date, is_after, window):
        if is_after:
            new_date = date + timedelta(days=window)
        else:
            new_date = date - timedelta(days=window)

        return new_date

    def _get_dates(self, date, window):
        event_date = datetime(date[0], date[1], date[2])

        after_event_date = self._add_sub_date(event_date, is_after=True, window=window)
        before_event_date = self._add_sub_date(
            event_date, is_after=False, window=window
        )

        return after_event_date, before_event_date

    def _is_in_window(self, tweet_date, middle_date, window):
        tweet_date = datetime(tweet_date[0], tweet_date[1], tweet_date[2])

        date1, date2 = self._get_dates(middle_date, window)

        if date2 <= tweet_date and tweet_date <= date1:
            return True
        else:
            return False

    # If we have a list, write it into a file
    def _write_list(self, path, content_list):
        if len(content_list) > 0 and path != None:
            with open(path, "w", encoding="utf-8") as file:
                for item in content_list:
                    file.write(str(item) + "\n")

    # From each tweet, extract the location data accordingly. Also, make checks if specified in the parameters
    def _extract_place(
        self,
        tweet,
        user,
        keep_retweets,
        collected_ids,
        previous_checks,
        search_keyword,
        date_window,
        api_version,
        loc=None,
    ):


        if api_version == 1:
            if loc == "user_bio":
                place = tweet["user"]["location"]
                if place == None or place == "":
                    return None

            elif loc == "tweet":
                if tweet["place"] is not None:
                    place = tweet["place"]["full_name"]
                    if place == None or place == "":
                        return None
                else:
                    return None

            elif loc == "coordinates":
                if tweet["geo"] is not None:
                    place = tweet["geo"]
                    if place == None or place == "":
                        return None
                else:
                    return None

            text = tweet["full_text"].replace("\n", " ")
            date = tweet["created_at"]

            if date_window != None:
                year = int(date[-4:])
                month = date[4:7]
                month_number = datetime.strptime(month, "%b").month
                day = int(date[8:10])
                tweet_date = [year, month_number, day]

                isOk = self._is_in_window(tweet_date, date_window[0], date_window[1])

                if isOk == False:
                    return None

            if search_keyword != None:
                if search_keyword not in text:
                    return None

            append_info = [place, date, text]

            if keep_retweets == False:
                if tweet.get("retweeted") == True:
                    return None

            if user == True:
                user_id = tweet["user"]["id"]
                tweet_id = int(tweet["id_str"])

                
                counted_before = False
                for check in previous_checks:
                    if check != None:
                        if user_id in check:
                            counted_before = True
                            break

                if counted_before:
                    return None

                elif user_id in collected_ids:
                    if tweet_id not in collected_ids[user_id]:
                        collected_ids[user_id][tweet_id] = append_info

                else:
                    collected_ids[user_id] = {}
                    collected_ids[user_id][tweet_id] = append_info

            else:
                tweet_id = int(tweet["id_str"])

                counted_before = False
                for check in previous_checks:
                    if check != None:
                        if tweet_id in check:
                            counted_before = True
                            break

                if counted_before:
                    return None


                elif tweet_id not in collected_ids:
                    collected_ids[tweet_id] = append_info

        elif api_version == 2:

            if loc == "user_bio":
                place = tweet["includes"]["users"][0].get("location")
                if place == None:
                    return None

            elif loc == "tweet":
                if tweet["includes"].get("places") != None:
                    if tweet["includes"]["places"][0].get("full_name") != None:
                        place = tweet["includes"]["places"][0]["full_name"]
                    else:
                        return None
                else:
                    return None
                
            elif loc=="coordinates":
                return 40

            text = (tweet["data"]["text"]).replace("\n", " ")
            date = str(tweet["data"]["created_at"])

            if search_keyword != None:
                if search_keyword not in text:
                    return None

            if date_window != None:
                clipped_date = date[:10]
                year = int(clipped_date[:4])
                month = clipped_date[5:7]
                if month[0] == "0":
                    month = month[1]

                day = clipped_date[8:]
                if day[0] == "0":
                    day = day[1]
                tweet_date = [year, int(month), int(day)]

                isOk = self._is_in_window(tweet_date, date_window[0], date_window[1])

                if isOk == False:
                    return None

            append_info = [place, date, text]

    
            if keep_retweets == False:
                if tweet["data"].get("referenced_tweets") == None:
                    return None
                elif tweet["data"].get("referenced_tweets") != None:
                    if tweet["data"]["referenced_tweets"][0]["type"] == "retweeted":
                        return None

            if user == True:
                user_id = tweet["data"]["author_id"]

                counted_before = False
                for check in previous_checks:
                    if check != None:
                        if user_id in check:
                            counted_before = True
                            break

                if counted_before:
                    return None


                elif user_id in collected_ids:
                    tweet_id = int(tweet["data"]["id"])
                    if tweet_id not in collected_ids[user_id]:
                        collected_ids[user_id][tweet_id] = append_info
                else:
                    collected_ids[user_id] = {}
                    tweet_id = int(tweet["data"]["id"])
                    collected_ids[user_id][tweet_id] = append_info

            else:
                tweet_id = int(tweet["data"]["id"])

                
                
                counted_before = False
                
                for check in previous_checks:
                    if check != None:
                        if tweet_id in check:
                            counted_before = True
                            break

                if counted_before:
                    return None

                elif tweet_id not in collected_ids:
                    collected_ids[tweet_id] = append_info

    def _map_places_to_data(self, ids, user, guess, use_coordinates=False, gpd_df=None):

        if user:  # user-based search
            for users in tqdm(ids.keys(), position=0, leave=True):
                user_dict = {city: 0 for city in self.city_data}
                if use_coordinates:
                    for tweets in ids[users].keys():
                        if use_coordinates:
                            new_dict = {}
                            new_dict["type"] = "Point"
                            new_dict["coordinates"] = []
                            new_dict["coordinates"].append(
                                ids[users][tweets][0]["coordinates"][1]
                            )
                            new_dict["coordinates"].append(
                                ids[users][tweets][0]["coordinates"][0]
                            )

                            geometry = Point(new_dict["coordinates"])

                            pt = gpd.GeoDataFrame({"geometry": [geometry]})
                            pt = pt.set_crs("epsg:4326")

                            intersections = gpd.overlay(
                                pt, gpd_df, how="intersection", keep_geom_type=False
                            )
                            name = intersections["name"]
                            if name.empty is False:
                                city = name.iloc[0]
                                city = unidecode(city)
                                city = city.lower()
                                user_dict[city] += 1

                    city = max(user_dict, key=user_dict.get)
                    if user_dict[city] > 0:
                        self.city_data[city] += 1

                else:
                    for tweets in ids[users]:

                        location_candidates = self._lower_unidecode(
                            ids[users][tweets][0]
                        )
                        common_elements = set(location_candidates).intersection(
                            set(self.city_data.keys())
                        )
                        if len(list(common_elements)) == 1:
                            city = list(common_elements)[0]
                            user_dict[city] += 1

                        else:
                            city = self._return_city(
                                location_candidates, self.ilce2city_mapper, guess
                            )
                            if city is not None:
                                user_dict[city] += 1


                            else:
                                city = self._return_city(
                                    location_candidates, self.semt2city_mapper, guess
                                )
                                if city is not None:
                                    user_dict[city] += 1


                    city = max(user_dict, key=user_dict.get)
                    if user_dict[city] > 0:
                        self.city_data[city] += 1

        else:  # tweet-based search

            if use_coordinates:

                for tweets in tqdm(ids.keys(), position=0, leave=True):

                    if use_coordinates:
                        new_dict = {}
                        new_dict["type"] = "Point"
                        new_dict["coordinates"] = []
                        new_dict["coordinates"].append(
                            ids[tweets][0]["coordinates"][1]
                        )
                        new_dict["coordinates"].append(
                            ids[tweets][0]["coordinates"][0]
                        )

                        geometry = Point(new_dict["coordinates"])

                        pt = gpd.GeoDataFrame({"geometry": [geometry]})
                        pt = pt.set_crs("epsg:4326")

                        intersections = gpd.overlay(
                            pt, gpd_df, how="intersection", keep_geom_type=False
                        )
                        name = intersections["name"]
                        if name.empty is False:
                            city = name.iloc[0]
                            city = unidecode(city)
                            city = city.lower()
                            self.city_data[city] += 1

            else:

                for tweets in tqdm(ids.keys(), position=0, leave=True):

                    location_candidates = self._lower_unidecode(ids[tweets][0])

                    common_elements = set(location_candidates).intersection(
                        set(self.city_data.keys())
                    )
                    if len(list(common_elements)) == 1:
                        city = list(common_elements)[0]
                        self.city_data[city] += 1

                    else:
                        city = self._return_city(
                            location_candidates, self.ilce2city_mapper, guess
                        )
                        if city is not None:
                            self.city_data[city] += 1

                        else:
                            city = self._return_city(
                                location_candidates, self.semt2city_mapper, guess
                            )
                            if city is not None:
                                self.city_data[city] += 1

    def _try_parse_json(self, json_string):
        try:
            parsed_json = json.loads(json_string)
            return 4
        except json.JSONDecodeError as e:
            return None

    def _fill_city_data(self, all_files, user, keep_retweets, search_keyword, date_window, search_element, pop_bias, df, previous_checks):
        
        total_count = 0  # total tweet count
        first_check = True

        print("NOW ON SEARCH FOR " + search_element)
        print("\n")

        ids = {}  # the id's that we will find. The structure will be:
        # either: ids[user_id][tweet_id] = [place, date, text]
        # OR: ids[tweet_id] = [place, date, text]
        for file_name in all_files:
            with gzip.open(file_name, "rt") as fh:
                
                print("Now on file " + file_name)

                pbar = tqdm(fh)
                for line in pbar:
                    did_load_correctly = self._try_parse_json(line)

                    if did_load_correctly == 4:
                        tweet = json.loads(line)
                        total_count += 1  # dict ids is filled up here
                        
                        if first_check:
                            result = self._extract_place(
                                tweet,
                                user,
                                keep_retweets,
                                ids,
                                previous_checks=previous_checks,
                                search_keyword=search_keyword,
                                date_window=date_window,
                                api_version=2,
                                loc=search_element,
                            )

                            if result == 40:
                                return
                            
                            first_check = False

                        else:
                            self._extract_place(
                                tweet,
                                user,
                                keep_retweets,
                                ids,
                                previous_checks=previous_checks,
                                search_keyword=search_keyword,
                                date_window=date_window,
                                api_version=2,
                                loc=search_element,
                            )
        
                    else:
                        uid, data = line.split("\t")
                        data = json.loads(data)
                        for tweet in data:

                            total_count += 1  # dict ids is filled up here
                            
                            self._extract_place(
                                tweet,
                                user,
                                keep_retweets,
                                ids,
                                previous_checks=previous_checks,
                                search_keyword=search_keyword,
                                date_window=date_window,
                                api_version=1,
                                loc=search_element,
                            )

                    pbar.set_postfix({"Total tweet count": total_count})


        use_coordinates = False
        if search_element == "coordinates":
            use_coordinates=True
        self._map_places_to_data(
            ids, user, pop_bias, use_coordinates=use_coordinates, gpd_df=df
        )


        return ids
    

    # Previous name: get_textual_locations
    def get_locations(
        self,
        data_path,
        verbose=0,
        output_dir="./",
        pop_bias=False,
        keep_retweets=True,
        user=True,
        search_keyword=None,
        date_window=None,
        gpd_path="src/data/turkey.geojson",
        priority_queue="coordinates,user_bio,tweet",    
    ):
        """Gets the textual location information on the tweet\n
        city_data: json file consisting of cities as keys and integers as values\n
        main_data_path: path to the data, zipped in gzip\n
        data_folder_path: path to the folder, containing gzip files\n
        path_result: the json path where the updated city_data will be written onto\n
        all_info_path: json path to write the dictionary where dict[user_id][tweet_id] = [location, date, text] is the format\n
        which_metadata: "user_loc" or "tweet (or "coordinates" if API v1 is used)"\n
        !! If "coordinates" is used, gdp_path must not be empty\n
        other path parameters: txt paths, storing the contect which is what their names suggests\n
        pop_bias: whether to have a population bias or not\n
        retweets: whether to look at retweets or not\n
        user: whether to conduct the search user-based or tweet-based\n
        search_keyword: whether to only get the tweets that include a specific keyword on their text\n
        date_window: format [[2023,10,7], 15]. This means, +-15 days from the date given [year,month,date]\n
        kwargs: lists of user/tweet ids to skip"""

        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            pass
        else:
            print("Directory does not exist.")
            return
        
        if gpd_path != None:
            df = gpd.read_file(gpd_path)
        else:
            gpd_path=None   

        print("Starting to gather place information...")

        all_files = []
        if data_path[-1] == '/':
            all_files = list(glob("/" + data_path.strip("/") + "/*.jsons.gz"))
        else:
            all_files.append(data_path)

        priority_queue = priority_queue.split(',')

        previous_checks = []

        for element in priority_queue:
            ids = self._fill_city_data(all_files, user, keep_retweets, search_keyword, date_window, element, pop_bias, df, previous_checks)

            previous_checks.append(ids)
            
            if verbose == 1:
                with open(output_dir+"all_info_" + element + ".json", "w", encoding="utf-8") as json_file:
                    json.dump(ids, json_file, indent=2)

            with open(output_dir+"results_" + element + ".json", "w") as file:
                json.dump(self.city_data, file, indent=4)
