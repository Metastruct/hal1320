from willie.module import commands
from willie.config import ConfigurationError

import random

def configure(config):
    if config.option('Configure BOFH', False):
        config.add_section('bofh')
        config.interactive_add(
            'bofh', 'path',
            'Path to BOFH text file.',
            default='/home/hal1320/.willie/bofh.txt'
        )

def setup(bot):
    if not bot.config.has_section('bofh'):
        raise ConfigurationError('BOFH is not configured')
    if not bot.config.has_option('bofh', 'path'):
        raise ConfigurationError('BOFH path is not defined')

@commands('bofh')
def bofh(bot, trigger):
    """Posts a random BOFH excuse."""
    bot.say(random.choice(list(open(bot.config.bofh.path))))