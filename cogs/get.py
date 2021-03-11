import discord
from aiohttp import request
from discord.ext import commands

class GetAPIData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def leaderboard(self, ctx):
        URL = "https://cookieapi-development.up.railway.app/api/leaderboard/"
        embed = discord.Embed(title="CashOutCookie Leaderboard",
                             description=f"[Check the full leaderboard here](https://cashoutcookie.com/rank)",
                             color=discord.Colour.teal())

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                i = 1
                for data in data:
                    username = data['username']
                    balance = data['balance']
                    embed.add_field(name=f"{i}: {username}", value=f'[Total Balance: {balance}](https://cashoutcookie.com/profile/{username})', inline=False)
                    i += 1
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} reponse")


    @commands.command()
    async def profile(self, ctx, *, username=None): 
        if username is not None:
            URL = f"https://cookieapi-development.up.railway.app/api/profile/{username}/"
            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    accountid = data['accountid']
                    balance = data['balance']
                    date_joined = data['date_joined']
                    emailhash = data['emailhash']

                    embed = discord.Embed(title=f"{username}'s profile", description=f"[More info](https://cashoutcookie.com/profile/{username})", color=discord.Color.green())
                    embed.add_field(name='Account Id:', value=accountid, inline=False)
                    embed.add_field(name='balance:', value=balance, inline=False)
                    embed.add_field(name='date_joined:', value=date_joined, inline=False)
                    embed.set_thumbnail(url=f"https://gravatar.com/avatar/{emailhash}?d=mp&size=100")
                    await ctx.send(embed=embed)
                    
                else:
                    await ctx.send(f"The user **'{username}'** doesn't exist.")
        else:
            await ctx.send("You need to enter a username to view their profile :D\n ```!profile <username>```")

def setup(bot):
    bot.add_cog(GetAPIData(bot))
