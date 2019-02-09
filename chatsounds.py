from sopel.module import commands

import urllib

@commands('cs')
def chatsounds(bot, trigger):
	if trigger.group(2):
		bot.say('http://cs.3kv.in/?s=%s' % (urllib.parse.quote(trigger.group(2))))
	else:
		bot.say('http://cs.3kv.in')