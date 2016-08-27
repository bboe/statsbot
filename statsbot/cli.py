"""statsbot command line tool.

Usage:
  statsbot help <command>
  statsbot [options] run
  statsbot [options] unlabeled

Options:
  -S <site> --site=<site>       Site name in praw.ini
                                [default: subreddit_stats].
  -s <name> --subreddit=<name>  The name of the subreddit to monitor for stats
                                requests [default: subreddit_stats].
  -h --help                     Output this message.
  -D --debug                    Show debugging messages.
  --version                     Output statsbot's version string.

"""
from __future__ import print_function
import sys

from docopt import docopt
from update_checker import update_check
import praw

from .bot import Bot
from .const import __version__
from .util import prepare_logger


def command_help(command, available_commands):
    """Output usage information for <command>.

    Usage: statsbot help <command>
    """
    if command not in available_commands:
        sys.stderr.write('Invalid command: {}\n'.format(command))
        return 1
    print('Help for command {}:\n'.format(command))
    print(available_commands[command].__doc__)
    return 0


def command_run(subreddit, args):
    """Run the statsbot indefinitely.

    Usage: statsbot run
    """
    return Bot(subreddit, site=args['--site']).run()


def command_unlabeled(subreddit, _):
    """Output submissions without a label newest first.

    Usage: statsbot unlabeled
    """
    for submission in subreddit.new(limit=None):
        if submission.link_flair_text:
            continue
        print(submission.title)
        print('    {}'.format(submission.url))
    return 0


def main():
    """Provide the entry point to the statsbot command."""
    args = docopt(__doc__, version='statsbot v{}'.format(__version__))
    prepare_logger('DEBUG' if args['--debug'] else 'INFO')

    commands = {'help': command_help, 'run': command_run,
                'unlabeled': command_unlabeled}

    if args['help']:
        return command_help(args['<command>'], commands)

    update_check(__package__, __version__)

    reddit = praw.Reddit(args['--site'], check_for_updates=False,
                         user_agent='statsbot/{}'.format(__version__))
    subreddit = reddit.subreddit(args['--subreddit'])
    for command in commands:
        if args[command]:
            return commands[command](subreddit, args)
    print('Oops, that command does not appear to be supported.')
    return 1
