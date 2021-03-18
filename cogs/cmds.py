import discord
from aiohttp import request
from discord.colour import Color
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx): 
        embed = discord.Embed(title="Help is here!", description=f"Characters inside `<>` are variables, enter the variable without `<>`", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        embed.add_field(name="?source", value="My Github source code!")
        embed.add_field(name="?leaderboard", value="Leaderboard for [CashoutCookie](https://cashoutcookie.com/rank)!")
        embed.add_field(name="?profile `<username>`", value="User profile from [CashoutCookie](https://cashoutcookie.com)!", inline=False)
        embed.add_field(name="?emergency", value="Use this command **only** when there is a huge bug/mistake or any major problem, if it's some small bug or issue then directly ping @team", inline=False)
        embed.add_field(name="?battleship", value="Starts a battleship game!", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(title="Github Source Code", description="[CashOutCookie - CookieBot](https://github.com/CashOutCookie/CookieBot)", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/octicons/1024/mark-github-512.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def emergency(self, ctx):
        modchannel = self.bot.get_channel(812560533428502531)
        embed = discord.Embed(title="Spam Ping Started..", description=f"Busy spam pinging the team in DMs for your help {ctx.author.name}", color=discord.Color.orange())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        await ctx.send(embed=embed)
        await modchannel.send("EMERGENCY SLOTHS! SOMEONE NEEDS YOUR HELP <@&819944514558492673>")
        await modchannel.send(f"<@&819944514558492673> user which used the command is {ctx.author.name} btw")
        await modchannel.send(f"<@&819944514558492673> this is their id {ctx.author.id}")
        await modchannel.send(f"<@&819944514558492673> Help them!")
        await modchannel.send("<@&819944514558492673>")
        await modchannel.send("<@&819944514558492673>")
def setup(bot):
    bot.add_cog(Commands(bot))
