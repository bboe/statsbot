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

    def run(self):
        """Run the bot indefinitely."""
        for submission in self.subreddit.stream.submissions():
            if submission.link_flair_text:
                continue
            print(submission.title)
