# FindGeoLocation

Finds city-level locations of tweets that were collected via Twitter API v1.

3 ways to get the location, from user bio, tweet bio or tweet coordinates

2 main ways: To guess or not to guess
    - If a person has entered a district name that is included in multiple cities, estimate that the person is from the city with the larger population

'data' --> Necessary files for the search. Can be updated/altered if needed.

'LocationProject' --> package for finding locations of tweets
    'gather_data.ipynb' --> Gathers the data in various ways
        1) Using all 3 ways back to back, building up on each other. Hence, we get a total profile of people with accessible location data.
        Order of operation: user bio, tweet bio, tweet coordinate
        2) Operated the first method, user bio, using the "without guess" way to see if any significant difference occured
        (most users can be accessed from the first method)
        3) Used all 3 methods individually to see how many users had what info.

'extract_loc_entities' --> no usage for now

'gathered_data' --> data gathered from 'gather_data.ipynb'

'graphs' --> the graphs of the data gathered

'extracting_graphs.ipynb' --> forming those graphs

## NUMERICAL DATA:

### With Guess:
With all 3 methods used on a cumulative way, 150 953 users' location info was gathered.

(Cumulative way as in, if one user data was gathered with the first method, skip that user when using the second method)

With the first method alone, 117 866 users' location info was gathered.

With the second method alone, 48 197 users' location info was gathered.

With the third method alone, 22 050 users' location info was gathered.

### Without Guess:
With the first method alone, 117 678 users' location info was gathered.

Hence, there is not much of a difference between the switch of guessing or not guessing.