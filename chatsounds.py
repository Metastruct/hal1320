from willie.module import commands

import urllib

@commands('cs')
def chatsounds(bot, trigger):
    bot.say('http://cs.3kelv.in/?s=%s' % (urllib.quote_plus(' '.join(trigger.args[3:]))))