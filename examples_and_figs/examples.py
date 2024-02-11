from src.TPS import GatherFiles, GatherLoc
from paths import *

# Example 1: API V1 with retweet and user-based search

## With bias
gather_fils = GatherFiles("src/data/city_mapper.xlsx", "src/data/cities.txt")
tps_finder = GatherLoc(gather_fils, population_path="src/data/populations.json")

tps_finder.get_locations(
    data_path=ex1_data_path,
    verbose=0,
    output_dir="examples_and_figs/example_1/results/pop_bias_ON",
    pop_bias=True,
    keep_retweets=True,
    user=True,
    search_keyword=None,
    date_window=None,
    gpd_path="src/data/turkey.geojson",
    priority_queue="user_bio,tweet,coordinates",
)

## Without bias
gather_fils = GatherFiles("src/data/city_mapper.xlsx", "src/data/cities.txt")
tps_finder = GatherLoc(gather_fils)

tps_finder.get_locations(
    data_path=ex1_data_path,
    verbose=0,
    output_dir="examples_and_figs/example_1/results/pop_bias_OFF",
    pop_bias=False,
    keep_retweets=True,
    user=True,
    search_keyword=None,
    date_window=None,
    gpd_path="src/data/turkey.geojson",
    priority_queue="user_bio,tweet,coordinates",
)

# Example 2: API V2 without retweet and tweet-based search

## With bias
gather_fils = GatherFiles("src/data/city_mapper.xlsx", "src/data/cities.txt")
tps_finder = GatherLoc(gather_fils, population_path="src/data/populations.json")

tps_finder.get_locations(
    data_path=ex2_data_path,
    verbose=0,
    output_dir="examples_and_figs/example_2/results/pop_bias_ON",
    pop_bias=True,
    keep_retweets=False,
    user=False,
    search_keyword=None,
    date_window=None,
    gpd_path="src/data/turkey.geojson",
    priority_queue="tweet,user_bio",
)


## Without bias
gather_fils = GatherFiles("src/data/city_mapper.xlsx", "src/data/cities.txt")
tps_finder = GatherLoc(gather_fils)

tps_finder.get_locations(
    data_path=ex2_data_path,
    verbose=0,
    output_dir="examples_and_figs/example_2/results/pop_bias_OFF",
    pop_bias=False,
    keep_retweets=False,
    user=False,
    search_keyword=None,
    date_window=None,
    gpd_path="src/data/turkey.geojson",
    priority_queue="user_bio,tweet",
)