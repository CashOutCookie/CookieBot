import discord
import datetime
from aiohttp import request
from discord.ext import commands

class GetAPIData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def leaderboard(self, ctx):
        URL = "https://api.cashoutcookie.com/api/leaderboard/"
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
                await ctx.send(f"Something went wrong, API returned a {response.status} response 😶")


    @commands.command()
    async def profile(self, ctx, *, username=None): 
        if username is not None:
            userprofile = username.lower()
            URL = f"https://api.cashoutcookie.com/api/profile/{userprofile}/"
            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    accountid = data['accountid']
                    balance = data['balance']
                    image = data['image']
                    date_joined = data['date_joined']

                    monthint = date_joined.split('-')[1]    
                    dayint = date_joined.split('-')[2]

                    year = date_joined.split('-')[0]
                    day = dayint.split("T")[0]
                    month = datetime.date(1900, int(monthint), 1).strftime('%B')


                    embed = discord.Embed(title=f"{userprofile.upper()}'s PROFILE", description=f"[More info](https://cashoutcookie.com/profile/{username})", color=discord.Color.green())
                    embed.add_field(name='Account Id:', value=accountid, inline=False)
                    embed.add_field(name='Balance:', value=balance, inline=False)
                    embed.add_field(name='Date Joined:', value=f"{year} {month} {day[:17]}", inline=False)
                    embed.set_thumbnail(url=image)
                    await ctx.send(embed=embed)
                    
                else:
                    await ctx.send(f"The user **'{username}'** doesn't exist.")

        elif username is None:
            userprofile = self.bot.listcookies.get(str(ctx.author.guild.id)).get(ctx.author.id)

            URL = f"https://api.cashoutcookie.com/api/profile/{userprofile}/"
            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    accountid = data['accountid']
                    balance = data['balance']
                    image = data['image']
                    date_joined = data['date_joined']

                    monthint = date_joined.split('-')[1]    
                    dayint = date_joined.split('-')[2]

                    year = date_joined.split('-')[0]
                    day = dayint.split("T")[0]
                    month = datetime.date(1900, int(monthint), 1).strftime('%B')


                    embed = discord.Embed(title=f"Here is your profile, {ctx.author.name}", description=f"[More info](https://cashoutcookie.com/profile/{username})", color=discord.Color.green())
                    embed.add_field(name='Account Id:', value=accountid, inline=False)
                    embed.add_field(name='Balance:', value=balance, inline=False)
                    embed.add_field(name='Date Joined:', value=f"{year} {month} {day[:17]}", inline=False)
                    embed.set_thumbnail(url=image)
                    await ctx.send(embed=embed)
                    
                else:
                    await ctx.send(f"You need to enter the username of user to view their profile. Format:```?profile <username>```\nYou aren't logged in right now, use the command `?login` to login yourself and view your profile on the command `?profile` without entering your username")



def setup(bot):
    bot.add_cog(GetAPIData(bot))
