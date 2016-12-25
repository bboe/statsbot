"""statsbot.bot module."""
import logging
import re

from prawcore.exceptions import PrawcoreException
from prawtools.stats import SubredditStats
import praw.exceptions


logger = logging.getLogger(__package__)


class Bot(object):
    """Bot manages submissions made to a given subreddit.

    This bot handles all submissions to the subreddit. Request titles are
    prefixed with "[request]". Stats submissions are prefixed with "Subreddit
    Stats". All other submissions will be labeled "other".

    """

    FLAIR_EXCEPTION = 'BUG'
    FLAIR_IN_PROGRESS = 'IN PROGRESS'
    FLAIR_INVALID = 'UNSATISFIABLE'
    FLAIR_SATISFIED = 'SATISFIED'
    FLAIR_STATS = 'STATS'
    FLAIR_UNKNOWN = 'OTHER'

    INVALID_MESSAGE = """Oops! Your request cannot be satisfied due to
unrecognized syntax. Please ensure your title is of the following format and
try again:

    [request] SUBREDDIT_NAME VIEW

Where `SUBREDDIT_NAME` is the name of the subreddit to run the stats on, and
`VIEW` is either a __number__, or one of _all_, _day_, _hour_, _month_, _week_,
or _year_. When `VIEW` is a __number__, it number represents the number of past
days to collect submissions for using the _new_ listing. Otherwise, `VIEW`
represents the respective _top_ listing.

Note: `SUBREDDIT_NAME` cannot be a special subreddit (e.g., all) and must be
accessible to the redditor from whom this message originates.

Examples:

    [request] redditdev all
    [request] subreddit_stats 730

---

If this message is in error please file a bug at
https://github.com/bboe/statsbot/issues after using GitHub's search to ensure a
similar issue does not already exist. Thanks!

"""

    RE_REQUEST = re.compile(r'^\[request\] (?:/?r/)?(?P<subreddit>\w+) '
                            r'(?P<view>\d+|all|day|hour|month|week|year)'
                            r'(?: -c ?(?P<commenters>\d+))?'
                            r'(?: -s ?(?P<submitters>\d+))?$',
                            re.IGNORECASE)

    @classmethod
    def parse_request_title(cls, title):
        """Return the subreddit and view for the request."""
        match = cls.RE_REQUEST.match(title)
        return match.groupdict() if match else None

    def __init__(self, subreddit, site):
        """Initialize an instance of Bot.

        :param subreddit: The subreddit to monitor for new submissions.
        :param site: The site name used to initialize subreddit_stats.
        """
        self.site = site
        self.subreddit = subreddit

    def _handle_request(self, submission):
        logger.debug('PARSING: {}'.format(submission.title))
        permalink = self._permalink(submission)
        params = self.parse_request_title(submission.title)

        if params:  # validate subreddit
            try:
                self.subreddit._reddit.subreddit(params['subreddit']).name
            except (praw.exceptions.APIException, PrawcoreException):
                params = None

        if params is None:
            logger.info('INVALID: {}'.format(permalink))
            self.subreddit.flair.set(submission, self.FLAIR_INVALID)
            self._safe_reply(submission, self.INVALID_MESSAGE)
        else:
            self._run_subreddit_stats(submission, params['subreddit'],
                                      params['view'].lower(),
                                      params['commenters'],
                                      params['submitters'])

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
            self._handle_request(submission)
        elif lower_title.startswith('subreddit stats:'):
            self._handle_stats(submission)
        else:
            self._handle_unknown(submission)

    def _run_subreddit_stats(self, submission, subreddit, view, commenters,
                             submitters):
        logger.info('RUNNING: {} {}'.format(subreddit, view))
        self.subreddit.flair.set(submission, self.FLAIR_IN_PROGRESS)
        stats = SubredditStats(subreddit, site=self.site, distinguished=False)
        stats.submit_subreddit = self.subreddit
        result = stats.run(view, int(submitters) if submitters else 10,
                           int(commenters) if commenters else 10)
        if result is None:
            flair = self.FLAIR_EXCEPTION
            reply = ('An issue occurred handling this request. '
                     'Please fix me /u/bboe.')
        else:
            self.subreddit.flair.set(result, self.FLAIR_STATS)
            flair = self.FLAIR_SATISFIED
            reply = 'Request satisfied: {}'.format(result.permalink)
        self._safe_reply(submission, reply)
        self.subreddit.flair.set(submission, flair)

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
        running = True
        while running:
            try:
                for submission in self.subreddit.stream.submissions():
                    if submission.link_flair_text:
                        continue
                    self._process_based_on_title(submission)
            except KeyboardInterrupt:
                logger.info('Termination received. Goodbye!')
                running = False
            except PrawcoreException:
                logger.exception('run loop')
        return 0
