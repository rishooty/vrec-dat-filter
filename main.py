from reddit_functions import RedditRelevancyChecker
import functions
import argh
import os

"""
The main method which automatically cleans up a dat file based on the default
or given url, the main game system page, and optional subpages.

1. The page and subpages separated by commas are first parsed into a list of urls,
which are then scraped one at a time by the spider. All the results are then 
written to a csv file.

2. Then each set of results in the csv is concatenated into one list.

3. A dat file is parsed, and checks each rom entry against this list.

4. Every rom entry that fails to fuzzy match any item in the list is
removed from the final, filtered dat file.

5. This dat file is then written and ready for use in any rom manager of 
your choice, allowing you to delete all roms you probably don't want.

6. If you're having issues with the rom manager, you can also specify
a directory to delete all non matching roms from. However, this should
be a last resort as it's dangerous if used with the wrong directory.

"""

default_url = 'http://vsrecommendedgames.wikia.com/wiki/'
default_csv = 'listTemp.csv'
default_accuracy = 90


def main(system, dat_in, main_url=default_url, reddit_filter=None, reddit_system=None, accuracy=default_accuracy, rm_from=None):
    """Filters a dat file based on a v's recommended wiki page."""
    # Scrape the url(s) into a csv.
    functions.generate_vrec_csv(system, main_url)

    # Parse the csv into a list.
    roms_to_keep = functions.parse_vrec_csv()

    # If specified, pass roms_to_keep through reddit filter.
    if reddit_system is None:
        reddit_system = system

    if reddit_filter is not None:
        reddit = RedditRelevancyChecker(reddit_system, reddit_filter)
        roms_to_keep = reddit.reddit_list_filter(roms_to_keep)

    # Create a filtered dat file using the above list.
    dat_out = os.path.splitext(dat_in)[0] + "clean.dat"
    functions.dat_clean(roms_to_keep, dat_in, dat_out, accuracy)

    # If specified, delete files not in the cleaned dat from a given directory.
    if rm_from is not None:
        functions.dir_clean(rm_from, dat_out)


def scrape(system, main_url=default_url, csv_out=default_csv):
    # Scrape the url(s) into a csv.
    functions.generate_vrec_csv(system, main_url, csv_out)


def clean(dat_in, dat_out=None, csv_in=default_csv, reddit_filter=None, reddit_system=' video game', accuracy=default_accuracy, rm_from=None):
    # Set default cleaned dat output path if none is set.
    # This is necessary because it depends on the dat_in arg.
    if dat_out is None:
        dat_out = os.path.splitext(dat_in)[0] + "clean.dat"

    # Parse input file into list depending on extension.
    name, ext = os.path.splitext(csv_in)
    if ext == '.csv':
        roms_to_keep = functions.parse_vrec_csv(csv_in)
    else:
        roms_to_keep = functions.parse_custom(csv_in)

    # If specified, pass roms_to_keep through reddit filter.
    if reddit_filter is not None:
        reddit = RedditRelevancyChecker(reddit_system, reddit_filter)
        roms_to_keep = reddit.reddit_list_filter(roms_to_keep)

    # Create a filtered dat file using the above list.
    functions.dat_clean(roms_to_keep, dat_in, dat_out, accuracy)

    # If specified, delete files not in the cleaned dat from a given directory.
    if rm_from is not None:
        functions.dir_clean(rm_from, dat_out)


def dir_clean(clean_dat, rm_from):
    # Delete files not in cleaned dat from given directory.
    functions.dir_clean(rm_from, clean_dat)

argh.dispatch_commands([main, scrape, clean, dir_clean])
