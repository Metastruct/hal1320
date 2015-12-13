from sopel.module import commands
from sopel.config import ConfigurationError
from sopel.config.types import StaticSection, ValidatedAttribute

import random

class BOFHsection(StaticSection):
    path = ValidatedAttribute('path', default='/home/hal1320/.sopel/bofh.txt')

def setup(bot):
    bot.config.define_section('bofh', BOFHsection)

def configure(config):
    config.define_section('bofh', BOFHsection, validate=False)
    config.bofh.configure_setting('path', 'Path to BOFH text file.')

@commands('bofh')
def bofh(bot, trigger):
    """Posts a random BOFH excuse."""
    bot.say(random.choice(list(open(bot.config.bofh.path))))