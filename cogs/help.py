import discord
import asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx): 
        embed = discord.Embed(title="Help is here!", description=f"Characters inside `<>` are variables, enter the variable without `<>`", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        embed.add_field(name="?source", value="My Github source code!")
        embed.add_field(name="?leaderboard", value="Leaderboard for [CashoutCookie](https://cashoutcookie.com/rank)!")
        embed.add_field(name="?profile `<username>`", value="User profile from [CashoutCookie](https://cashoutcookie.com)!", inline=False)
        embed.add_field(name="?login", value="Use the command to login to [CashoutCookie](https://cashoutcookie.com) here!", inline=False)
        embed.add_field(name="?emergency", value="Use this command **only** when there is a huge bug/mistake or any major problem, if it's some small bug or issue then directly ping @team", inline=False)
        embed.add_field(name="?battleship", value="Starts a battleship game!", inline=False)
        embed.set_footer(text="🍪 For CashOut Cookie Games")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction('🍪')
        await asyncio.sleep(1)

        gamesembed = discord.Embed(title="Fun time boiz", color=discord.Colour.teal())
        gamesembed.add_field(name="?cookiehunt", value="Starts a Cookie Hunt match with someone!\n Requires login to [CashOut Cookie](https://cashoutcookie.com) , use the command `?login` for that.\n Requires 100 cookies to start a match from both players.", inline=False)
        gamesembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")

        def check(reaction, user):
            return str(reaction.emoji) == '🍪'
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        await helpmsg.edit(embed=gamesembed)
        await helpmsg.clear_reaction('🍪')

def setup(bot):
    bot.add_cog(Help(bot))
