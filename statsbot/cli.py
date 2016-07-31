"""statsbot command line tool.

Usage:
  statsbot unlabeled

Options:
  -h --help  Output this message.
  --version  Output statsbot's version string.

"""
from __future__ import print_function

from docopt import docopt
import praw

from .const import __version__


def command_unlabeled(subreddit, _):
    """Output submissions without a label newest first."""
    for submission in subreddit.new(limit=None):
        if submission.link_flair_text:
            continue
        print(submission.title)
        print('    {}'.format(submission.url))


def main():
    """Provide the entry point to the statsbot command."""
    args = docopt(__doc__, version='statsbot v{}'.format(__version__))
    reddit = praw.Reddit('subreddit_stats',
                         user_agent='statsbot/{}'.format(__version__))
    subreddit = reddit.subreddit('subreddit_stats')

    if args['unlabeled']:
        command_unlabeled(subreddit, args)
    return 0
