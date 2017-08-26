import praw


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
