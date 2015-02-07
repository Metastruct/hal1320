from willie.module import commands

import urllib

@commands('cs')
def chatsounds(bot, trigger):
    bot.say('http://cs.3kv.in/?s=%s' % (urllib.quote(trigger.group(2))))