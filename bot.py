
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
import time
from dotenv import load_dotenv
from random import random
from selenium import webdriver
from PIL import Image  
import PIL  
from discord.ext import tasks
from PIL import Image
from PIL import ImageChops
import shutil
from selenium.webdriver.common.by import By

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

r = webdriver.Firefox()
url = "https://trouverunlogement.lescrous.fr/tools/flow/27/search?bounds=2.1991_49.0516_2.5285_48.7718&page=1&price=60000"


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
    print(message.content)
    # bot dont reply to himself
    if message.author == client.user:
        return
    #restrict to bot channel
    if message.channel.name != "bot":
        return
    
    p=re.compile('^start$')
    if p.match(message.content):
        while True:
            
            r.get(url)
            time.sleep(5)

            my_filename = "./screenshot.png"
            
            r.get_screenshot_as_file(my_filename)
            
            with open(my_filename, "rb") as fh:
                f = discord.File(fh, filename=my_filename)
            
            await message.channel.send(time.ctime())
            await message.channel.send(file=f)
            time.sleep(5)


@tasks.loop(minutes=2)
async def sendmessage():

    channel = client.get_channel(1062475822952353882)
    
    r.get(url)
    time.sleep(5)

    my_filename = "./screenshot.png"
    my_filename2 = "./text.txt"

    r.get_screenshot_as_file(my_filename)
    
    f = open(my_filename2, "r")
    old = f.readline()
    f.close()
    print(old)
    
    
    results_list = r.find_elements(By.XPATH, "//ul[@id='SearchResultsList']/li[@class='SearchResults-item']")
    f = open(my_filename2, "w")
    f.write(str(len(results_list)))
    f.close()

    print(len(results_list))
    
    if int(old) != len(results_list):
        await channel.send("@everyone")
    
    with open(my_filename, "rb") as fh:
        f = discord.File(fh, filename=my_filename)
            
    await channel.send(time.ctime())
    await channel.send(file=f)


@client.event
async def on_ready():
    
    sendmessage.start()
    
client.run(TOKEN)
