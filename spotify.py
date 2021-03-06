from sopel import web
from sopel import module
import time
import json
import re

regex = re.compile('(play.spotify.com\/track\/)([\w-]+)')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.WillieMemory()
    bot.memory['url_callbacks'][regex] = spotify

def shutdown(bot):
    del bot.memory['url_callbacks'][regex]

@module.rule('.*(play.spotify.com\/track\/)([\w-]+).*')
def spotify(bot, trigger, found_match=None):
    match = found_match or trigger

    resp = web.get('https://api.spotify.com/v1/tracks/%s' % match.group(2))

    result = json.loads(resp)

    try:
        artist = result['artists'][0]['name']
        title = result['name']
        album = result['album']['name']
        duration = result['duration_ms']

        duration_hms = time.strftime('%H:%M:%S', time.gmtime(duration / 1000))

        bot.say('{0} - {1} [{2}] | {3}'.format(artist, title, album, duration_hms))
    except KeyError:
        bot.say('Track not found.')