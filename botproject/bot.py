
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:17:58 2022

@author: rayane
"""
# bot.py
import os
import json
import discord
import requests
import re
from dotenv import load_dotenv
from random import random
from serveurlist import servelist

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    r = requests.get('http://arkdedicated.com/xbox/cache/officialserverlist.json')
    f1 = open("serveurinfo.json", "w")
    f1.write(r.text)
    f1.close
    f1 = open("serveurinfo.json", "r")
    
    serv=json.load(f1)
    
    f1.close



    p=re.compile('^(\?xo )[0-9]*$')
    if p.match(message.content):
        numero = servelist(int(message.content[4:]))
        response = "serveur name : ",serv[int(numero)]['Name'],"players online : ",serv[int(numero)]['NumPlayers']
        await message.channel.send(response)
    


client.run(TOKEN)

