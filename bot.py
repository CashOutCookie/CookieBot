import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '?')
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="https://cashoutcookie.com"))
    print("I'm Ready!")

async def on_message(message):
    if str(message.channel) == '📃todo' and not message.content.startswith("TO-DO"):
        await message.delete()


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


token = os.environ.get('TOKEN')
bot.run(token) 