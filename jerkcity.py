from willie.module import commands
from willie.config import ConfigurationError

import random

def configure(config):
    if config.option('Configure Jerkcity', False):
        config.add_section('jerkcity')
        config.interactive_add(
            'jerkcity', 'path',
            'Path to Jerkcity text file.',
            default='/home/hal1320/.willie/jerkcity.txt'
        )

def setup(bot):
    if not bot.config.has_section('jerkcity'):
        raise ConfigurationError('Jerkcity is not configured')
    if not bot.config.has_option('jerkcity', 'path'):
        raise ConfigurationError('Jerkcity path is not defined')

@commands('jerkcity')
def jerkcity(bot, trigger):
    """Posts a random Jerkcity line."""
    bot.say(random.choice(list(open(bot.config.jerkcity.path))))