import praw
import xml.etree.ElementTree as ET
import os


def get_reddit_object(client_id='JWw9vCj6-fEBfQ'):
    return praw.Reddit(client_id=client_id,
                       client_secret=None,
                       user_agent='vRec Dat Filter')


def is_relevant(reddit, search, time='month'):
    for submission in reddit.subreddit('all').search(search+' game', time_filter=time, limit=1):
        if time is 'all':
            print('"' + submission.title + '" was found.')
        else:
            print('"'+submission.title+'" was found in past '+time+'.')
        return True


def reddit_dat_clean(dat_file, dat_out, reddit, time='month'):
    """
    Searches each rom entry in a dat file against
    recent reddit discussions. If the game hasn't
    been discussed within x amount of time, it will
    be removed from the final dat.

    It then writes a new dat file with only the entries
    that tested positive. This dat file can then be
    imported into the rom manager of your choice
    to delete all roms that were removed from said dat

    :param dat_file:
    :param dat_out:
    :param reddit:
    :param time:
    :return:
    """

    if dat_out is None:
        dat_out = os.path.splitext(dat_file)[0] + "clean.dat"

    # Read in dat file
    tree = ET.parse(dat_file)
    root = tree.getroot()

    # If game.get('name') has no reddit results, mark game for deletion.
    to_delete = []
    for game in root.iter('game'):
        if not is_relevant(reddit, game, time):
            to_delete.append(game)

    # Delete all game xml blocks that were marked for deletion.
    for game in to_delete:
        root.remove(game)

    # Print the final xml to be used in a rom manager.
    tree.write(dat_out)


def reddit_list_filter(romstokeep, reddit, time='month'):
    """
    Filters a list of games/roms to keep, usually
    parsed from a scraped csv or user specified txt.

    It's main purpose is to narrow v's recommended wiki
    results even further before cleaning the dat.

    :param romstokeep:
    :param reddit:
    :param time:
    :return:
    """
    for game in romstokeep:
        if not is_relevant(reddit, game, time):
            romstokeep.remove(game)