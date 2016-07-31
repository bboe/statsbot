"""statsbot.cli module."""
from .const import __version__


def main():
    """Provide the entry point to the statsbot command."""
    print('statsbot v{}'.format(__version__))
    return 0
