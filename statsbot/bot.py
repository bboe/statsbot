"""statsbot.bot module."""


class Bot(object):
    """Bot manages submissions made to a given subreddit.

    This bot handles all submissions to the subreddit. Request titles are
    prefixed with "[request]". Stats submissions are prefixed with "Subreddit
    Stats". All other submissions will be labeled "other".

    """

    def __init__(self, subreddit):
        """Initialize an instance of Bot.

        :param subreddit: The subreddit to monitor for new submissions.
        """
        self.subreddit = subreddit

    def _process_based_on_title(self, submission):
        print(submission.title)
        lower_title = submission.title.lower()
        if lower_title.startswith('[request]'):
            print('  request')
        elif lower_title.startswith('subreddit stats:'):
            print('  stats')
        else:
            print('  unknown')

    def run(self):
        """Run the bot indefinitely."""
        try:
            for submission in self.subreddit.stream.submissions():
                if submission.link_flair_text:
                    continue
                self._process_based_on_title(submission)
        except KeyboardInterrupt:
            print('\nTermination received. Goodbye!')
        return 0
