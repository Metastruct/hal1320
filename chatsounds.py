# coding=utf8
from __future__ import unicode_literals
from willie.module import rule, priority, thread

import urllib

@willie.module.commands('cs')
def chatsounds(bot, trigger):
    bot.say('http://cs.3kelv.in/?s=%s!' % (urllib.quote_plus(trigger.args)))