"""statsbot command line tool.

Usage:
  statsbot [options]

Options:
  -h --help  Output this message.
  --version  Output statsbot's version string.

"""
from __future__ import print_function

from docopt import docopt

from .const import __version__


def main():
    """Provide the entry point to the statsbot command."""
    docopt(__doc__, version='statsbot v{}'.format(__version__))
    return 0
