# TPS -- Turkey Positioning System

TPS, detects city-level locations of tweets that were collected via Twitter API v1 or v2

Works for Turkish cities only with the default data from src/data. Can be modified for other countries as well.

First, gather the necessary files via class GatherFiles. Then, conduct the search. An example can be found below. The necessary data for the GatherFiles object can be found under ```data/```

Population bias:
- Active: If a district name is included in multiple cities, estimate that the tweet is from the city with the larger population. pop_bias parameter is set to ```False``` by default.
- Inactive: Do not do this

Districts searched:
- City name
- "Ilçe" name (smaller part of a city)
- "Semt" name (smaller part of an ilçe)

## Example

```python
from TPS import GatherFiles, GatherLoc
files = GatherFiles()
files.create_district_mappings(path_excel) # the excel which is named city_street.xlsx on data/
city_list = files.write_data_return_list(cities_path=city_list_path, data_path_json=empty_data_path)
# cities_path: a list of cities. Can be found on data/
# data_path_json: just a regular file name, ending with .json. This is going to be written with the function

city_data = files.get_city_data(empty_data_path)
# Gathered the files needed to create GatherLoc object

tps_finder = GatherLoc(city_list=city_list, files=files)

tps_finder.get_locations(city_data=city_data, data_folder_path=dir_path, which_metadata="user_bio", path_result="v2_trial_tweet-based.json", api_version=2, user=False, retweets=True, path_dates="dates.txt", path_texts=txt_path, search_keyword="@RTErdogan", date_window=[[2023,4,10], 6])
```

## Links Used

```data/city_street.xlsx``` --> https://postakodu.ptt.gov.tr/ <br />

```data/cities.txt``` --> https://engelsizdestek.org/iller <br />

```data/populations.json``` --> https://gist.github.com/ozdemirburak/4821a26db048cc0972c1beee48a408de <br />
The populations here are modified via: ```data/illere-gore-il-nufuslari.xls``` --> https://data.tuik.gov.tr/Bulten/Index?p=49685


```data/turkey.geojson``` --> https://github.com/alpers/Turkey-Maps-GeoJSON <br />

```graphs/explanation/overestimated_cities.png``` --> http://160.75.25.161/index.php/itudergisi_a/article/viewFile/1060/1009
