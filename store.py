import os
import sys

import requests
import datetime
import json
from urllib import parse as urlparse

import discord

class Data:
    def __init__(self, bot, store_name, api_key):
        self.bot = bot
        self.store_name = store_name
        

        self.guild_data = json.loads(requests.get(
            f'https://json.psty.io/api_v1/stores/{urlparse.quote_plus(store_name)}', headers={'Api-Key': f'{api_key}'}).text)

    def write_to_remote(self):
        requests.put(f'https://json.psty.io/api_v1/stores/{storeName}', headers={
                     'Api-Key': f'{apiKey}', 'Content-Type': 'application/json'}, data=json.dumps(self.guild_data['data']))

    def check_guilds(self):
        print("check")
        print(self.bot.guilds)
        for guild in self.bot.guilds:
            try:
                print(guildData['data'][f'{guild.id}'])
            except KeyError:
                print("added")
                guildData['data'][f'{guild.id}'] = {
                    "server_name": f"{guild.name}",
                    "serverIcon": f"{guild.icon_url_as(format=None, static_format='png', size=1024)}",
                    "settings": {
                        "minecraft": {
                            "ip": "",
                            "rconPort": 00000,
                            "rconPassword": ""
                        },
                        "prefix": "r!"
                    },
                    "members": {
                        "397570848665632789": {
                            "level": {
                                "current": 13,
                                "part_current": 243,
                                "part_goal": 250
                            },
                            "infractions": [
                                "Warnned"
                            ]
                        }
                    }
                }
                write_to_remote()