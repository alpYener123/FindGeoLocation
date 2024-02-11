import argparse
from pathlib import Path
from src.TPS import GatherFiles, GatherLoc

# Parse arguments
parser = argparse.ArgumentParser(
    prog="TPS",
    description="Find city-level locations of Twitter users or tweets themselves",
)

parser.add_argument("-cm", "--city_mapper_path", default="src/data/city_mapper.xlsx",
                    help="Excel file which includes city and district names as columns. Check src/data/city_mapper.xlsx")
parser.add_argument("-c", "--cities_path", default="src/data/city_street.xlsx",
                    help="Text file which has one city per line. Check src/data/cities.txt")
parser.add_argument("-p", "--populations_path", default="None",
                    help="JSON file which also has the populations of cities. Check src/data/populations.json")
parser.add_argument("-o", "--output_dir", default="./",
                    help="Directory where the outputs are going to be written onto.")
parser.add_argument("-d", "--data_path", required=True,
                    help="Path to the API data")
parser.add_argument("-v", "--verbose", default=0,
                    help="To also save the tweet/user information gathered as a JSON file. 0 for no, 1 for yes")
parser.add_argument("-pb", "--population_bias", default=False,
                    help="Whether to add population bias or not. Bool value.")
parser.add_argument("-rt", "--keep_retweets", default=True,
                    help="Whether to keep retweets or filter out them. Bool value.")
parser.add_argument("-u", "--user_search", default=True,
                    help="Whether to search via user-based or tweet-based. Bool value.")
parser.add_argument("-kw", "--search_keyword", default=None,
                    help="If not none, only gathers tweets with the given keyword in its text.")
parser.add_argument("-dw", "--date_window", default=None,
                    help="Whether to only get tweets from a specific window. [[YYYY,M,D], X]. X is the length/2 of the interval.")
parser.add_argument("-gpd", "--geopandas_path", default="src/data/turkey.geojson",
                    help="If coordinates are also in the search, a geojson path of the country's shape is needed. Check src/data/turkey.geojson.")
parser.add_argument("-pr", "--priority_queue", default="coordinates,user_bio,tweet",
                    help="Which metadata to search for. Format: \"coordinates,user_bio,tweet\"")

parser.print_help()
args = parser.parse_args()
Path(args.output_dir).mkdir(parents=True, exist_ok=True)

# Run the search function
gather_fils = GatherFiles(args.city_mapper_path, args.cities_path)
tps_finder = GatherLoc(gather_fils, population_path=args.populations_path)

tps_finder.get_locations(
    data_path=args.data_path,
    verbose=args.verbose,
    output_dir=args.output_dir,
    pop_bias=args.population_bias,
    keep_retweets=args.keep_retweets,
    user=args.user_search,
    search_keyword=args.search_keyword,
    date_window=args.date_window,
    gpd_path=args.geopandas_path,
    priority_queue=args.priority_queue,
)
