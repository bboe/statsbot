"""statsbot.bot module."""
import praw.exceptions


class Bot(object):
    """Bot manages submissions made to a given subreddit.

    This bot handles all submissions to the subreddit. Request titles are
    prefixed with "[request]". Stats submissions are prefixed with "Subreddit
    Stats". All other submissions will be labeled "other".

    """

    FLAIR_UNKNOWN = 'OTHER'

    def __init__(self, subreddit):
        """Initialize an instance of Bot.

        :param subreddit: The subreddit to monitor for new submissions.
        """
        self.subreddit = subreddit

    def _handle_unknown(self, submission):
        self.subreddit.flair.set(submission, self.FLAIR_UNKNOWN)
        self._safe_reply(submission,
                         'This does not appear to be a valid request.')
        print('UNKNOWN: {}'.format(self._permalink(submission)))

    def _permalink(self, submission):
        return 'https://www.reddit.com{}'.format(submission.permalink)

    def _process_based_on_title(self, submission):
        print(submission.title)
        lower_title = submission.title.lower()
        if lower_title.startswith('[request]'):
            print('  request')
        elif lower_title.startswith('subreddit stats:'):
            print('  stats')
        else:
            self._handle_unknown(submission)

    def _safe_reply(self, submission, message):
        try:
            submission.reply(message)
        except praw.exceptions.APIException as exc:
            if exc.error_type != 'TOO_OLD':
                raise
            return False
        return True

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
