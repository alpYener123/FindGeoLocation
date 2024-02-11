from src.TPS import GatherFiles, GatherLoc
import argparse
from pathlib import Path
from paths import *


"""parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
)
parser.add_argument("-cm","--city_mapper_path", default="src/data/city_street.xlsx")
parser.add_argument("-c","--cities_path", default="src/data/city_street.xlsx")
parser.add_argument("-p","--populations_path", default="None")

parser.add_argument("-o","--output_dir",  default="./")
parser.add_argument("-d","--data_path", required=True)
parser.add_argument("-v", "--verbose", default=0)
parser.add_argument("-pb", "--population_bias", default=False)
parser.add_argument("-rt", "--keep_retweets", default=True)
parser.add_argument("-u", "--user_search", default=True)
parser.add_argument("-kw", "--search_keyword", default=None)
parser.add_argument("-dw", "--date_window", default=None)
parser.add_argument("-gpd", "--geopandas_path", default="src/data/turkey.geojson")
parser.add_argument("-pr", "--priority_queue", default="coordinates,user_bio,tweet")


Path(parser.output_dir).mkdir(parents=True, exist_ok=True)
"""


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