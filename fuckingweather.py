"""
fuckingweather.py - Willie module for The Fucking Weather
Copyright 2013 Michael Yanovich
Copyright 2013 Edward Powell

Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
# -*- coding: utf-8 -*-
from willie.module import commands, rate, priority, NOLIMIT
from willie import web
import re


@commands('fucking_weather', 'fw')
@rate(30)
@priority('low')
def fucking_weather(bot, trigger):
    text = trigger.group(2)
    if not text:
        bot.reply("INVALID FUCKING PLACE. PLEASE ENTER A FUCKING ZIP CODE, OR A FUCKING CITY-STATE PAIR.")
        return
    text = web.quote(text)
    page = web.get("http://thefuckingweather.com/?where=%s&unit=c" % (text))
    re_mark = re.compile('<p class="remark">(.*?)</p>')
    re_temp = re.compile('<span class="temperature" tempf="(.*)">(.*?)</span>')
    re_flavor = re.compile('<p class="flavor">(.*?)</p>')
    results = re_mark.findall(page)
    temp = re_temp.findall(page)
    flavor = re_flavor.findall(page)
    if results:
        bot.reply(str(temp[0][1])+u"\N{DEGREE SIGN}"+"C?! "+results[0]+" , "+flavor[0])
    else:
        bot.reply("I CAN'T FIND THAT SHIT")
        return bot.NOLIMIT