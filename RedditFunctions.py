from Functions import del_xml_blocks
import xml.etree.ElementTree as ET
import praw
import os


class RedditRelevancyChecker:
    """ Class containing all reddit related methods."""

    def __init__(self, time='month', client_id='JWw9vCj6-fEBfQ'):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=None,
                                  user_agent='vRec Dat Filter')
        self.time = time

    def is_relevant(self, search):
        """
        Searches a single game for any recent reddit discussions.
        If the game hasn't been discussed within x amount of time,
        it will return false.

        :param search:
        :return:
        """

        for submission in self.reddit.subreddit('all').search(search+' game', time_filter=self.time, limit=1):
            if self.time is 'all':
                print('"' + submission.title + '" was found.')
            else:
                print('"'+submission.title+'" was found in past '+self.time+'.')
            return True
        return False

    def reddit_dat_clean(self, dat_file, dat_out):
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
            if not self.is_relevant(game.get('name')):
                to_delete.append(game)

        # Delete all game xml blocks that were marked for deletion and print final xml.
        del_xml_blocks(to_delete, tree, dat_out)

    def reddit_list_filter(self, roms_to_keep):
        """
        Filters a list of games/roms to keep, usually
        parsed from a scraped csv or user specified txt.

        It's main purpose is to narrow v's recommended wiki
        results even further before cleaning the dat.

        :param roms_to_keep:
        :return:
        """
        for game in roms_to_keep:
            if not self.is_relevant(game):
                roms_to_keep.remove(game)

        return roms_to_keep
