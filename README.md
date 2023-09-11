# FindGeoLocation

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

'''```.ipynb``` --> forming those graphs

## NUMERICAL DATA:

### With Guess:
With all 3 methods used on a cumulative way, 150 404 users' location info was gathered.

(Cumulative way as in, if one user data was gathered with the first method, skip that user when using the second method)

With the first method alone, 117 343 users' location info was gathered.

With the second method alone, 48 172 users' location info was gathered.

With the third method alone, 22 050 users' location info was gathered.

### Without Guess:
With all 3 methods used on a cumulative way, 149 913 users' location info was gathered.

(Cumulative way as in, if one user data was gathered with the first method, skip that user when using the second method)

With the first method alone, 116 814 users' location info was gathered.

With the second method alone, 47 993 users' location info was gathered.

The third method has no guess feature since it is again 22 050 users.