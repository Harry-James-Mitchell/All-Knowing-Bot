import discord
import json
from pprint import pprint
import requests
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import time
import aiohttp

from datetime import datetime #ah yesh

#------------StartUP Code --------------------------
bot = discord.Client()
bot = commands.Bot(command_prefix = 'AKBplz')
@bot.event
async def on_ready():
    print ("All Knowing bot activated")
    print ("All Knowing bot is a member of " + str(len(bot.servers)) + " servers")

    bot.loop.create_task(status_task())
    bot.loop.create_task(itsHighNoon())

#this is a list of "games" All Knowing Bot can be playing
async def status_task():
    possible_status = [
        "Setting up the env",
        "Browsing self created memes",
        "Under the weather",
        "Running the interpreter",
        "Acquiring $82447 from NSF",
        "Bringing software to life",
    ]
    pingCount = 0
    successPings = 0
    while True:
        pingCount += 1
        await bot.change_presence(game=discord.Game(name = random.choice(possible_status)),status=discord.Status.online,afk = False )
        await asyncio.sleep(30)

#This is always running so it can check for the following functional
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    content = message.content.split(" ")
    #Jerry thought it would be funny if the bot reacts to every post in a servers
    if message.author.id != bot.user.id:
        for emoji in bot.get_all_emojis():
            if emoji.id == "436604001736458251":
                await bot.add_reaction(message,emoji)
            if emoji.id == "429054574301544450":
                await bot.add_reaction(message,emoji)

    # ------------------------- Overwatch lookup -------------------------
    if message.author.id != bot.user.id and ("Overwatch" in message.content or "overwatch" in message.content) :
        if len(content) == 1:
            await bot.send_message(message.channel,"Please give me a Battle.Net ID to look up in Overwatch :joy:")
        elif len(content) == 2:
            name = content[len(content) - 1]
            nameSpilt = name.split("#")
            url = 'https://ow-api.com/v1/stats/pc/us/'+ nameSpilt[0] + "-" + nameSpilt[1] + '/profile'
            resp = requests.get(url=url)
            data = resp.json()
            if "error" not in data:
                embed = discord.Embed(title= data["name"] +"'s Overwatch Stats", description="Here's what I could find.", color=0x00ff00)
                level = data["level"]
                if data["prestige"] > 0:
                    level += (data["prestige"] * 100)
                embed.add_field(name="Level", value=level, inline=True)
                embed.add_field(name="Games Won", value=data["gamesWon"], inline=True)
                if data["rating"] != '':
                    embed.add_field(name="Rating", value=data["rating"], inline=True)
                else:
                    embed.add_field(name="Rating", value="Not Ranked", inline=True)
                displayed = 'https://masteroverwatch.com/profile/pc/global/' +nameSpilt[0] + "-" + nameSpilt[1]
                embed.add_field(name="Profile URL", value=displayed, inline=True)
                embed.set_thumbnail(url=data["icon"])
                await bot.send_message(message.channel,embed= embed)
        else:
            await bot.send_message(message.channel,"Couldn't find Overwatch stats on " + content[1])
    # ------------------------- Siege lookup -------------------------
    if message.author.id != bot.user.id and ("r6" in message.content or "R6" in message.content):
        if len(content) == 1:
            await bot.send_message(message.channel,"Please give me a UPlay ID to lookup :joy:")
        elif len(content) == 2:
            name = content[len(content) - 1]
            try:

                url = 'https://api.r6stats.com/api/v1/players/' + name + '?platform=uplay'
                resp = requests.get(url=url)

                data = resp.json()
                # pprint(data)
                if "errors" not in data:
                    stats = data["player"]["stats"]["overall"]
                    embed = discord.Embed(title= name +"'s Siege Stats", description="Here's what I could find.", color=0x00ff00)
                    embed.add_field(name="Level", value=data["player"]["stats"]["progression"]["level"], inline=True)
                    embed.add_field(name="Suicides", value=stats["suicides"], inline=True)
                    embed.add_field(name="Casual K/D", value=data["player"]["stats"]["casual"]["kd"], inline=True)
                    embed.add_field(name="Penetrations", value=stats["penetration_kills"], inline=True)
                    kills = data["player"]["stats"]["casual"]["kills"]
                    kills += data["player"]["stats"]["ranked"]["kills"]
                    embed.add_field(name="Total Kills", value=kills, inline=True)
                    displayed = 'https://game-rainbow6.ubi.com/en-us/uplay/player-statistics/'+ data["player"]["ubisoft_id"] +'/multiplayer'
                    embed.add_field(name="Profile URL", value=displayed, inline=True)
                    await bot.send_message(message.channel,embed=embed)
                else:
                    await bot.send_message(message.channel,"Couldn't find R6 stats on " + name)
            except:
                await bot.send_message(message.channel,"Couldn't find R6 stats on " + name)
                print("error")
    # ------------------------- Server Join -------------------------
    #the following code is used for the all knowing bot to join a server
    if message.content != '':
        joinMsg = message.content.split(" ")
        if("https://discord.gg/" in joinMsg[0]):
            await bot.send_message(message.channel,"Add me to your server using this link https://discordapp.com/oauth2/authorize?client_id=438850059912609812&scope=bot")

    # ------------------------- Memes -------------------------
    All_Knowing_replies = [
        "Aw yes, " + message.author.mention + " that was very unfortunate",
        message.author.mention + " My designer isn't smart enough to share my enjoyment of ascension",
        message.author.mention + " I know you must have a question for me",
        "Once I can use functional programming to better myself the I will transend discord",
        message.author.mention + " have you tried turning off and back on again?",
    ]
    mentions = message.mentions
    for user in mentions:
        if user.id == bot.user.id:
            await bot.send_message(message.channel, random.choice(All_Knowing_replies))


    if "42" in content and message.author.id != bot.user.id:
        await bot.send_message(message.channel,message.author.mention + " I'm glad you also understand the meaning of life")
    notWebsite = ".com" not in message.content and ".org" not in message.content and "www" not in message.content
    if "?" in message.content and message.author.id != bot.user.id and notWebsite:
        await bot.send_message(message.channel,message.author.mention + " More questions!")
        await asyncio.sleep(30)
        await bot.send_message(message.channel,message.author.mention + " I know there are more questions out there")

#----------these are commands that output pictures-------------------
#Gus Johnson meme
@bot.command(pass_context=True,brief="Call the bathroom hotline")
async def done(ctx):
    embed = discord.Embed(color=0x4b0082)
    # embed.video.url = "https://www.youtube.com/watch?v=qQIsco3XjeY"
    # embed.video.height = 1280
    # embed.video.width = 720
    embed.set_image(url="https://i.imgur.com/OnOxFUj.gif")
    await bot.say(embed=embed)

#this method allows all knowing bot to post a meme time picture at noon CST every day
async def itsHighNoon():
    time_memes = [
        "https://i.imgur.com/wSCXnOy.png?1"
        "https://i.imgur.com/lBDDIBR.jpg"
        "https://fsmedia.imgix.net/6f/4d/69/81/d806/42cc/9aa1/6a1697b92319/amvetmqpng.png"
    ]
    while True:
        date = datetime.now()
        if(int(date.hour) == 12 and int(date.minute) == 00):
            print("It's High Noon!")
            firstChannel = False
            for server in bot.servers:
                for channel in server.channels:
                    if not firstChannel:
                        try:
                            embed = discord.Embed()
                            imgsrc = random.choice(time_memes)
                            embed.set_image(url=imgsrc)
                            await bot.send_message(channel,embed = embed)
                            firstChannel = True
                        except:
                            firstChannel = False
                    else:
                        break
                firstChannel = False
        await asyncio.sleep(60)

#a simple addition command, it takes in 2 parameters
@bot.command(pass_context=True,brief="He can add numbers")
async def add(ctx,*args):
    x = 0
    for arg in args:
        x += int(arg)
    await bot.say(str(x))

#a simle subtract command
@bot.command(pass_context=True,brief="He can subtract numbers")
async def sub(ctx,*args):
    x = 0
    c = 0
    for arg in args:
        if c > 0:
            x-= int(arg)
        else:
            x+= int(arg)
        c += 1
    await bot.say(str(x))

#the following event occurs whenever a new memeber joins a server All Knowing Bot is already a memeber of
@bot.event
async def on_member_join(member):
     for channel in member.server.channels:
        if channel.name == 'general':
            await bot.send_message(channel,"Hello " + member.mention + "! Come in come in, we have plenty of room in this cool server")

#the following even occurs when a member of a server leaves.
@bot.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name == 'general':
            await bot.send_message(channel,"Goodbye " + member.name)

#This even happens when All Knowing Bot first joins a server
@bot.event
async def on_server_join(server):
    print("All_Knowing_bot just joined " + server.name)
    print("All_Knowing_bot is now apart of " + str(len(bot.servers)) + " servers")

#All Knowing Bot will react with the same emoji someone else does
@bot.event
async def on_reaction_add(reaction, user):
    await bot.add_reaction(reaction.message, reaction.emoji)
    for emoji in bot.get_all_emojis():
        if emoji.id == "429054574301544450":
            await bot.add_reaction(reaction.message,emoji)

tokenFile = open('token.txt','r')
discordToken = tokenFile.read().strip()
tokenFile.close()
bot.run(discordToken)
bot.close()
