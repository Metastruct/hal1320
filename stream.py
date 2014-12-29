from willie.module import commands
from willie.config import ConfigurationError

import urllib, json

def configure(config):
    if config.option('Configure stream URLs', False):
        config.add_section('stream')
        config.interactive_add(
            'stream', 'url',
            'URL for listening to the stream.',
            default='http://test.com:8000/hello.ogg'
        )
        config.interactive_add(
            'stream', 'statsurl',
            'URL for retreiving stream stats.',
            default='http://test.com/stats.php'
        )

def setup(bot):
    if not getattr(bot.config, 'stream', None):
        raise ConfigurationError('Stream is not configured')
    if not getattr(bot.config.stream, 'url', None):
        raise ConfigurationError('Stream URL is not defined')
    if not getattr(bot.config.stream, 'statsurl', None):
        raise ConfigurationError('Stream stats URL is not defined')

@commands('stream')
def stream(bot, trigger):
    resp = urllib.urlopen(bot.config.stream.statsurl)

    if not resp:
        bot.say('Failed to request stream stats.')
    else:
        data = json.loads(resp.read())

        if not data or data.offline:
            bot.say('Stream is offline.')
        else:
            plural = 's'
            if data.listeners == 1:
                plural = ''

            bot.say('Now playing: {0} - {1} | {2} listener{3} | {4}'.format(data.artist, data.title, data.listeners, plural, bot.config.stream.url))
