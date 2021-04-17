import discord
import asyncio
from discord.ext import commands

teamids = [477723384495603713, 791950104680071188, 510479576259100672, 283312969931292672, 310186020136026115]

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="CookieBot Help", description=f"Characters inside `<>` are variables, enter the variable without `<>`", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        embed.add_field(name="?source", value="My Github source code!", inline=False)
        embed.add_field(name="?leaderboard", value="Leaderboard for [CashoutCookie](https://cashoutcookie.com/rank)!", inline=False)
        embed.add_field(name="?profile `<username>`",value="User profile from [CashoutCookie](https://cashoutcookie.com)!\n *While logged in, just entering `?profile` without any username will show the command user's profile.*", inline=False)
        embed.add_field(name="?login", value="Use the command to login to [CashoutCookie](https://cashoutcookie.com) in the server!", inline=False)
        embed.add_field(name="?logout", value="Use the command to logout of [CashoutCookie](https://cashoutcookie.com) in the server!", inline=False)
        embed.add_field(name="?idea `<youridea>`",value="Use the command to suggest an idea which will be sent in the official [CashOut Cookie Support Server](https://discord.gg/jTCtZ2xv8z)", inline=False)
        embed.set_footer(text="🍪 For CashOut Cookie Games")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction('🍪')
        await helpmsg.add_reaction('🗑')
        await asyncio.sleep(1)

        gamesembed = discord.Embed(title="Cookie Hunt!", description="```?cookiehunt```", color=discord.Colour.orange())
        gamesembed.add_field(name="Game", value="Play Cookie Hunt with someone! Guess where opponent's cookies are hidden and find them!", inline=False)
        gamesembed.add_field(name="Requirement", value="Login to [CashOut Cookie](https://cashoutcookie.com) on this server using the command `?login`", inline=False)
        gamesembed.add_field(name="Fee", value="100 cookies from both players.", inline=False)
        gamesembed.add_field(name="Rewards", value="200 Cookies for Victory\n150 Cookies if opponent surrenders\n100 Cookies if opponent gets timed out (Not technically a win so fee amount is given back to the winner)", inline=False)
        gamesembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")

        def check(reaction, user):
            return str(reaction.emoji) == '🍪' or str(reaction.emoji) == '🗑' and reaction.message == helpmsg
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        
        if str(reaction.emoji) == '🍪' and user == ctx.author:
            await helpmsg.edit(embed=gamesembed)
            await helpmsg.clear_reaction('🍪')
        elif str(reaction.emoji) == '🗑' and user == ctx.author:
            await helpmsg.delete()
        
        def check(reaction, user):
            return str(reaction.emoji) == '🗑' and reaction.message == helpmsg
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        await helpmsg.delete()


    @commands.command()
    async def helpteam(self, ctx):    
        if ctx.author.id in teamids:
            embedteam = discord.Embed(title="Staff commands", color=discord.Colour.teal())
            embedteam.add_field(name="?embed `<colour>`",value="Answer the questions sent by me to make an embed! \n *Reacting to 🎨 will give all colour values*", inline=False)
            embedteam.add_field(name="?cache `<serverid>`",value="Shows auth cookies stored for the server if server id entered, if not entered then shows all auth cookies stored in JSON format.", inline=False)
            embedteam.add_field(name="?adduser `<cashoutcookieusername>` `<discorduserid>`",value="Adds auth cookies for the user inside the server where the command is triggered", inline=False)
            embedteam.add_field(name="?removeuser", value="Clears the user's auth cookie from the Discord Server inside which the command is triggered (Logs out).", inline=False)
            embedteam.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
            embedteam.set_footer(text="🎨 Embed color values")
            await ctx.send(embed=embedteam)

def setup(bot):
    bot.add_cog(Help(bot))
