"""statsbot setup.py."""

import re
from codecs import open
from os import path
from setuptools import setup


PACKAGE_NAME = 'statsbot'
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, 'const.py'),
          encoding='utf-8') as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)


setup(name=PACKAGE_NAME,
      author='Bryce Boe',
      author_email='bbzbryce@gmail.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython'],
      description='Monitors and satisfies requests for subreddit_stats.',
      entry_points={'console_scripts': ['statsbot = statsbot.cli:main']},
      install_requires=['docopt >=0.6.2, <1', 'prawtools >=0.21.0'],
      keywords='reddit subreddit stats',
      license='Simplified BSD License',
      long_description=README,
      packages=[PACKAGE_NAME],
      url='https://github.com/bboe/statsbot',
      version=VERSION)
