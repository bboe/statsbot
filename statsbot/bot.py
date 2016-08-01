"""statsbot.bot module."""
import logging

import praw.exceptions


logger = logging.getLogger(__package__)


class Bot(object):
    """Bot manages submissions made to a given subreddit.

    This bot handles all submissions to the subreddit. Request titles are
    prefixed with "[request]". Stats submissions are prefixed with "Subreddit
    Stats". All other submissions will be labeled "other".

    """

    FLAIR_STATS = 'STATS'
    FLAIR_UNKNOWN = 'OTHER'

    def __init__(self, subreddit):
        """Initialize an instance of Bot.

        :param subreddit: The subreddit to monitor for new submissions.
        """
        self.subreddit = subreddit

    def _handle_stats(self, submission):
        logger.info('STATS: {}'.format(self._permalink(submission)))
        self.subreddit.flair.set(submission, self.FLAIR_STATS)

    def _handle_unknown(self, submission):
        logger.info('UNKNOWN: {}'.format(self._permalink(submission)))
        self.subreddit.flair.set(submission, self.FLAIR_UNKNOWN)
        self._safe_reply(submission,
                         'This does not appear to be a valid request.')

    def _permalink(self, submission):
        return 'https://www.reddit.com{}'.format(submission.permalink)

    def _process_based_on_title(self, submission):
        logger.debug('FOUND: {}'.format(submission.title))
        lower_title = submission.title.lower()
        if lower_title.startswith('[request]'):
            logger.info('REQUEST')
        elif lower_title.startswith('subreddit stats:'):
            self._handle_stats(submission)
        else:
            self._handle_unknown(submission)

    def _safe_reply(self, submission, message):
        permalink = self._permalink(submission)
        try:
            submission.reply(message)
        except praw.exceptions.APIException as exc:
            if exc.error_type != 'TOO_OLD':
                raise
            logger.info('REPLY FAIL: {} {}'.format(exc.error_type, permalink))
            return False
        logger.debug('REPLIED TO: {}'.format(permalink))
        return True

    def run(self):
        """Run the bot indefinitely."""
        try:
            for submission in self.subreddit.stream.submissions():
                if submission.link_flair_text:
                    continue
                self._process_based_on_title(submission)
        except KeyboardInterrupt:
            logger.info('Termination received. Goodbye!')
        return 0
