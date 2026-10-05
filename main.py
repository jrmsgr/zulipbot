#!/usr/bin/env python3

import json
import os
import os.path
import sys

import praw
from zulip import Client

from zulipbot.bot import ZulipBot
from zulipbot.commands import *


# --------------------------------------------------------------
# functions
# --------------------------------------------------------------
def assert_file_exists(path):
    if not os.path.isfile(path):
        print("ERROR: file '{}' wasn't found\nSee README.md".format(path),
              file=sys.stderr)
        exit(1)


# --------------------------------------------------------------
# execution
# --------------------------------------------------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))
assert_file_exists("./zuliprc")
assert_file_exists("./msg_filters.json")
client = Client(config_file="./zuliprc")
with open('./msg_filters.json') as f:
    msg_filters = json.load(f)
if isinstance(msg_filters, dict):
    msg_filters = [msg_filters]

bot = ZulipBot(client, msg_filters)
bot.add_cmd(ZulipBotCmdGnagnagna())
bot.add_cmd(ZulipBotCmdWeather())
bot.add_cmd(ZulipBotCmdSpeak())
bot.add_cmd(ZulipBotCmdAudio())
bot.add_cmd(ZulipBotCmdVolume())
bot.add_cmd(ZulipBotCmdPlay())
bot.add_cmd(ZulipBotCmdRecord())
bot.add_cmd(ZulipBotCmdStop())
# reddit commands are optional: they need a praw.ini with valid API credentials
if os.path.isfile("./praw.ini"):
    reddit = praw.Reddit("zulipbot")
    bot.add_cmd(ZulipBotCmdJoke(reddit))
    bot.add_cmd(ZulipBotCmdAww(reddit))
    bot.add_cmd(ZulipBotCmdGif(reddit))
    bot.add_cmd(ZulipBotCmdRedPost(reddit))
    bot.add_cmd(ZulipBotCmdRedPic(reddit))
    bot.add_cmd(ZulipBotCmdRedGif(reddit))
    bot.add_cmd(ZulipBotCmdRedPlay(reddit))
else:
    print("WARNING: praw.ini not found, reddit commands are disabled",
          file=sys.stderr)
bot.add_cmd(ZulipBotCmdLunch())
bot.add_cmd(ZulipBotCmdZenQuote())
bot.run()
