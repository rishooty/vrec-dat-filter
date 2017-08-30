import Functions
import argparse
import os
import sys

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

# Handle cli input, get initial argument for action to perform.
parser = argparse.ArgumentParser(description='Filter a dat file based on v\'s recommended wiki')
parser.add_argument('action', type=str, choices=['main', 'scrape', 'clean', 'dir_clean'], help='Action to perform.')
initial_arg = parser.parse_args(sys.argv[1:2])


def main():
    # Handle cli input, add arguments and options according to initial argument.
    parser.add_argument('system', type=str, help='System name and optional subsections. Ex: "NES,Famicom"',
                        metavar='system(s)')
    parser.add_argument('dat_in', type=str, help='Path to datfile.', metavar='path_to_dat')
    parser.add_argument('--main_url', type=str, default='http://vsrecommendedgames.wikia.com/wiki/',
                        help='Primary V\'s url in case default is broken.', metavar='vrecwiki_homepage')
    parser.add_argument('--accuracy', type=int, default='90', choices=range(1, 101), metavar='1-100',
                        help='Acceptable positive match percentage, 0 to 100.')
    parser.add_argument('--rm_from', type=str, help='Directory to delete non-matches from, skips dat cleaning.',
                        metavar='path_to_roms')
    args = parser.parse_args()

    # Scrape the url(s) into a csv.
    Functions.generate_vrec_csv(args.system, args.main_url)

    # Parse the csv into a list.
    roms_to_keep = Functions.parse_vrec_csv()

    # Create a filtered dat file using the above list.
    dat_out = os.path.splitext(args.dat_in)[0] + "clean.dat"
    Functions.dat_clean(roms_to_keep, args.dat_in, dat_out, args.accuracy)

    # If specified, delete files not in the cleaned dat from a given directory.
    if args.rm_from is not None:
        Functions.dir_clean(args.rm_from, dat_out)


def scrape():
    # Handle cli input, add arguments and options according to initial argument.
    parser.add_argument('system', type=str, help='System name and optional subsections. Ex: "NES,Famicom"',
                        metavar='system(s)')
    parser.add_argument('--main_url', type=str, default='http://vsrecommendedgames.wikia.com/wiki/',
                        help='Primary V\'s url in case default is broken.', metavar='vrecwiki_homepage')
    parser.add_argument('--csv_out', type=str, default='listTemp.csv', help='Output csv path.', metavar='path_to_csv')
    args = parser.parse_args()

    # Scrape the url(s) into a csv.
    Functions.generate_vrec_csv(args.system, args.main_url, args.csv_out)


def clean():
    # Handle cli input, add arguments and options according to initial argument.
    parser.add_argument('dat_in', type=str, help='Path to datfile.')
    parser.add_argument('--accuracy', type=int, default='90', choices=range(1, 101), metavar='1-100',
                        help='Acceptable positive match percentage, 0 to 100.')
    parser.add_argument('--rm_from', type=str, help='Directory to delete non-matches from, skips dat cleaning.',
                        metavar='path_to_roms')
    parser.add_argument('--csv_in', type=str, default='listTemp.csv', help='Input path for file w/ list of roms.',
                        metavar='path_to_csv')
    parser.add_argument('--dat_out', type=str, help='Output cleaned dat path.', metavar='path_to_dat')
    args = parser.parse_args()

    # Set default cleaned dat output path if none is set.
    # This is necessary because it depends on the dat_in arg.
    if args.dat_out is None:
        args.dat_out = os.path.splitext(args.dat_in)[0] + "clean.dat"

    # Parse input file into list depending on extension.
    name, ext = os.path.splitext(args.csv_in)
    if ext == '.csv':
        roms_to_keep = Functions.parse_vrec_csv(args.csv_in)
    else:
        roms_to_keep = Functions.parse_custom(args.csv_in)

    # Create a filtered dat file using the above list.
    Functions.dat_clean(roms_to_keep, args.dat_in, args.dat_out, args.accuracy)

    # If specified, delete files not in the cleaned dat from a given directory.
    if args.rm_from is not None:
        Functions.dir_clean(args.rm_from, args.dat_out)


def dir_clean():
    # Handle cli input, add arguments and options according to initial argument.
    parser.add_argument('clean_dat', type=str, help='Path to cleaned datfile.', metavar='path_to_dat')
    parser.add_argument('rm_from', type=str, help='Directory to delete non-matches from, skips dat cleaning.',
                        metavar='path_to_roms')
    args = parser.parse_args()

    Functions.dir_clean(args.rm_from, args.clean_dat)

# Execute action based on initial argument.
arg_switch = {
    'main': main,
    'scrape': scrape,
    'clean': clean,
    'dir_clean': dir_clean
}

arg_switch[initial_arg.action]()
