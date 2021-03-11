import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '?')
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="https://cashoutcookie.com"))
    print("I'm Ready!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
  
@bot.event
async def on_message(message):
    if str(message.channel) == '📃todo' and not message.content.startswith("TO-DO"):
        await message.delete()


bot.run(TOKEN)