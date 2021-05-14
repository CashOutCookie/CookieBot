import os, discord
from pymongo import MongoClient
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix = '?')
bot.remove_command('help')

client = MongoClient(os.environ.get("MONGO_URL"))
db = client['discord']

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="https://cashoutcookie.com | ?help"))
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
bot.run(token)
