from sopel.module import commands
from sopel.config import ConfigurationError
from sopel.config.types import StaticSection, ValidatedAttribute

import urllib, json

class LastFMsection(StaticSection):
    path = ValidatedAttribute('apikey')

def setup(bot):
    bot.config.define_section('lastfm', LastFMsection)

def configure(config):
    config.define_section('lastfm', LastFMsection, validate=False)
    config.lastfm.configure_setting('apikey', 'Last.fm API key')

@commands('lastfm')
def lastfm(bot, trigger):
    username = trigger.group(2)

    if not username:
        bot.say('You need to specify a username.')
    else:
        resp = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={0}&api_key={1}&format=json".format(username, bot.config.lastfm.apikey))

        if not resp:
            bot.say('Failed to request last.fm data.')
        else:
            data = json.loads(resp.read())

            if not data:
                bot.say('Failed to parse last.fm data.')
            else:
                if not 'recenttracks' in data or not 'track' in data['recenttracks']:
                    bot.say('Invalid username or no recently played tracks.')
                else:
                    currenttrack = ''

                    for track in data['recenttracks']['track']:
                        if '@attr' in track and track['@attr']['nowplaying']:
                            currenttrack = '{0} - {1}'.format(track['artist']['#text'], track['name']) 
                            break

                    if currenttrack != '':
                        bot.say('{0} is currently listening to: {1} (via last.fm)'.format(username, currenttrack))
                    else:
                        bot.say('%s is not currently listening to anything.' % username)