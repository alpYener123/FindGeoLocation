# FindGeoLocation

Finds city-level locations of tweets that were collected via Twitter API v1.

3 ways to get the location from the metadata
- ["user"]["location"]
- ["place"]["full_name"]
- ["geo"]

2 main ways: To guess or not to guess
- Guess: If a person has entered a district name that is included in multiple cities, estimate that the person is from the city with the larger population
- No guess: If multiple cities are found, skip that district and search for a more specific (smaller) one

Districts searched:
- City name
- "Ilçe" name (smaller part of a city)
- "Semt" name (smaller part of an ilçe)

## Example

```python
>>from TweetLocationFinder import GatherFiles and GatherLoc
>>files = GatherFiles()
>>files.city_parts(path_excel)
>>city_list = files.city_list_and_data(cities_path=city_list_path, datapathJSON=empty_data_path)
>>city_data = files.get_city_data(empty_data_path)
# Gather the files needed to create GatherLoc object

>>guess_accumulate = GatherLoc(city_list=city_list, files=files)
>>guess_accumulate.get_user_loc(city_data=city_data, main_data_path=main_data_path, result_path_JSON=result_path)
```
### Explanation
```city_parts``` fills up the empty dictionaries of ```GatherFiles``` object.
- ```path_excel``` example: ```data/city_street.xlsx```
 <br />
 
```city_list_and_data``` returns a list of cities. Also saves a json file as all city names as keys and all values defaultly set to 0.
- ```cities_path``` example: ```data/cities.txt```
- ```datapathJSON``` a json path which the json file is written onto.
<br />

```get_user_loc``` searches through the data and gets the user locations of users that have legitimate location info in ```[user][location]``` part of the metadata
- Arguments:
    - ```city_data``` a dictionary with city names as keys and some integer value as values.
    - ```main_data_path``` path to the main data (that is, data collected via Twitter API v1)
    - ```result_path_JSON``` path which the end result of city_data will be written to. Must be JSON format

Example output of the function:
```
515098it [31:21, 273.72it/s, Count=515098, Successful Count=117343, List1 idx=None, List2 idx=None]
```

More functions and their usage examples are on ```trial_data.ipynb```

## Info

```data``` --> Necessary files for the search. Can be updated/altered if needed.

```LocationProject``` --> package for finding locations of tweets. ```GatherUserLoc``` includes all the necessary packages.
    ```trial_data.ipynb``` --> Gathers the data in all possible ways and stores it in ```trial_data_gathered'''```
        1) Accumulation: Using all 3 ways back to back, building up on each other. Hence, we get a total profile of people with accessible location data.
        Order of operation: user bio, tweet bio, tweet coordinate.
        2) Individual: Used all 3 methods individually to see how many users had what info.
    ```GatherFiles``` --> gathers the files needed in a usable data type
    ```GatherLoc``` --> actually gathers the location info via the 3 ways explained above
    ```EntityExtractor``` --> Extracts the location entities on the given sentence via language models. Then, finds (if there is) a corresponding city and displays it.

```graphs``` --> the graphs of the data gathered

```extracting_graphs.ipynb``` --> forming those graphs

## Links Used

```data/city_street.xlsx``` --> https://postakodu.ptt.gov.tr/
```data/cities.txt``` --> https://engelsizdestek.org/iller
```data/populations.json``` --> https://gist.github.com/ozdemirburak/4821a26db048cc0972c1beee48a408de
```data/turkey.geojson``` --> https://github.com/alpers/Turkey-Maps-GeoJSON
```graphs/explanation/overestimated_cities.png``` --> http://160.75.25.161/index.php/itudergisi_a/article/viewFile/1060/1009