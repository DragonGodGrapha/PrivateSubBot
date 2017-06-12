import json
import os
import sys

import praw

import config
import helpers
import main


def replace(old_un, new_un):
    user_list_fp = os.path.join(helpers.folder_path(), 'data', 'user_list.json')
    with open(user_list_fp, 'r') as f:
        users = json.load(f)
    users[users.index(old_un)] = new_un
    with open(user_list_fp, 'w') as f:
        json.dump(users, f)

    reddit = helpers.initialize_reddit()
    if not config.testing:
        try:
            reddit.subreddit(config.target_subreddit).flair.set(
                redditor=old_un,
                text='Moved to /u/%s' % new_un, )
            reddit.subreddit(config.target_subreddit).contributor.remove(old_un)
        except praw.exceptions.APIException:
            # Deleted user, most likely
            pass
        main.flair_users([new_un], reddit, config.flair_normal, number_adjustment=users.index(new_un))
        main.add_users([new_un], reddit)
    else:
        print('Flaired and removed /u/%s; Flaired and added /u/%s') % (old_un, new_un)


def process_input():
    if len(sys.argv) == 3:
        old_un, new_un = sys.argv[1], sys.argv[2]
    else:
        old_un = input('Enter the exact username of the user to be removed: ')
        new_un = input('Enter the exact username of the user to replace them: ')

    replace(old_un, new_un)


if __name__ == '__main__':
    process_input()
