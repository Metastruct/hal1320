from sopel.module import commands
from sopel.config import ConfigurationError
from sopel.config.types import StaticSection, ValidatedAttribute

import urllib, json

class StreamSection(StaticSection):
    url = ValidatedAttribute('url', default='http://example.com:8000/hello.ogg')
    statsurl = ValidatedAttribute('statsurl', default='http://example.com/stats.php')

def setup(bot):
    bot.config.define_section('stream', StreamSection)

def configure(config):
    config.define_section('stream', StreamSection, validate=False)
    config.stream.configure_setting('url', 'URL for listening to the stream.')
    config.stream.configure_setting('statsurl', 'URL for retreiving stream stats.')

@commands('stream')
def stream(bot, trigger):
    resp = urllib.urlopen(bot.config.stream.statsurl)

    if not resp:
        bot.say('Failed to request stream stats.')
    else:
        data = json.loads(resp.read())

        if not data or 'offline' in data:
            bot.say('Stream is offline.')
        else:
            plural = 's'
            if data['listeners'] == 1:
                plural = ''

            bot.say('Now playing: {0} - {1} | {2} listener{3} | {4}'.format(data['artist'], data['title'], data['listeners'], plural, bot.config.stream.url))
