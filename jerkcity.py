from sopel.module import commands
from sopel.config import ConfigurationError
from sopel.config.types import StaticSection, ValidatedAttribute

import random

class JerkCitySection(StaticSection):
    path = ValidatedAttribute('path', default='/home/hal1320/.sopel/jerkcity.txt')

def setup(bot):
    bot.config.define_section('jerkcity', JerkCitySection)

def configure(config):
    config.define_section('jerkcity', JerkCitySection, validate=False)
    config.jerkcity.configure_setting('path', 'Path to Jerkcity text file.')

@commands('jerkcity')
def jerkcity(bot, trigger):
    """Posts a random Jerkcity line."""
    bot.say(random.choice(list(open(bot.config.jerkcity.path))))