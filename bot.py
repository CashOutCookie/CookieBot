import os, discord
from pymongo import MongoClient
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix = '?')
bot.remove_command('help')

client = MongoClient("mongodb://mongo:O4gluolSFsk5ZDGa7q1w@containers-us-west-5.railway.app:5790")
db = client['discord']

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="?help | Special command in DMs 👀"))
    print("I'm Ready!")



@tasks.loop(seconds = 2)
async def myLoop():
    bot.listcookies = {}
    for server in db.list_collection_names():
        collection = db[server]
        cookieList = {}
        for user in collection.find():
            cookieList[user["discordId"]] = user["username"]
        bot.listcookies[server] = cookieList


myLoop.start()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        

token = os.environ.get('TOKEN')
bot.run("ODE5NTg5NzM5ODkwODY4MjQ1.YEo0bQ.c4o3fbjnRpOjOVNsXd7Sf-saf08")
