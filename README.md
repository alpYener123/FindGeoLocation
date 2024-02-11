# TPS -- Turkey Positioning System

TPS, detects city-level locations of tweets that were collected via Twitter API v1 and v2

Works for Turkish cities only with the default data from ```src/data```. Can be modified for other countries as well.

First, gather the necessary files via class GatherFiles. Then, conduct the search. A sample run can be found in ```main.py```. 2 examples are given in folder ```examples_and_figs```.

Locations searched in order to map the tweet to a city:
- City name
- "Ilçe" name (smaller part of a city)
- "Semt" name (smaller part of an ilçe)

## Usage
One can use this tool via downloading the repository and running main.py.
```main.py``` and ```src/``` are the main contents needed for usage.


## Features
Population bias:
- Active: If a district name is included in multiple cities, estimate that the tweet is from the city with the larger population. pop_bias parameter is set to ```False``` by default.
- Inactive: Do not do this

Retweets:
- It can either filter out or keep retweets during the search

User or tweet based:
- It can either find locations of users or tweets.
- For users, say that the user has 10 tweets, the system maps all the tweets to a city if possible. Then, the user is mapped to the city on which the user has most tweets in.

Keyword search:
- It can filter out tweets such that they need to include a specific phrase in their tweet text. This can be, for example, a popular username.

Date window:
- It can search for tweets coming from a specific time window.
- Examples: [[2023,10,7], 15]. From the specified date (Y/M/D), go +- 15 days. That is the interval.

Priority queue:
- It can search for specific location metadata, by the given order.
- Available location metadata:
    - V1
        - user_bio: ["user"]["location"]
        - tweet: ["place"]["full_name"]
        - coordinates: ["geo"]

    - V2
        - user_bio: ["includes"]["users"][0]["location"]
        - tweet: ["includes"]["places"][0]["full_name"]

## References
Links for the sources that contents in ```src/data/``` were obtained.

```cities.txt```: https://engelsizdestek.org/iller <br />

```city_mapper.xlsx```: https://postakodu.ptt.gov.tr/ <br />

```populations.json```: https://github.com/alpers/Turkey-Maps-GeoJSON. The populations here are updated from ```yillara-gore-il-nufuslari.xls``` <br />

```yillara-gore-il-nufuslari.xls```: https://data.tuik.gov.tr/Bulten/Index?p=49685. Populations for the year 2022 were used. <br />

```data/turkey.geojson``` --> https://github.com/alpers/Turkey-Maps-GeoJSON <br />

Special thanks to Onur Varol and Ali Najafi.