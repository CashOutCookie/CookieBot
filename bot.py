import os, discord
from pymongo import MongoClient
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix = '?')
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="?help"))
    print("I'm Ready!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        

token = os.environ.get('TOKEN')
bot.run(token)
