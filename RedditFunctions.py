import praw


class RedditRelevancyChecker:
    """ Class containing all reddit related methods."""

    def __init__(self, system, time='month', client_id='JWw9vCj6-fEBfQ'):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=None,
                                  user_agent='vRec Dat Filter')
        self.system = system
        self.time = time

    def is_relevant(self, search):
        """
        Searches a single game for any recent reddit discussions.
        If the game hasn't been discussed within x amount of time,
        it will return false.

        :param search:
        :return:
        """

        for submission in self.reddit.subreddit('all').search(search+self.system, time_filter=self.time, limit=1):
            return True
        return False

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
