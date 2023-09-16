# FindGeoLocation

## Example

```
from TweetLocationFinder import GatherFiles and GatherLoc
files = GatherFiles()
files.city_parts(path_excel)
city_list = files.city_list_and_data(city_list_path, datapathJSON=empty_data_path)
city_data = files.get_city_data(empty_data_path)

guess_accumulate = GatherLoc(city_list, files, populationPATH=pop_path)
guess_accumulate.get_user_loc(city_data, main_data_path, result_path, result_txt_path, guess=True)
```


## Info

Finds city-level locations of tweets that were collected via Twitter API v1.

3 ways to get the location: from user bio, tweet bio or tweet coordinates

2 main ways: To guess or not to guess
    - If a person has entered a district name that is included in multiple cities, estimate that the person is from the city with the larger population

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