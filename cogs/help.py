import discord, random, asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help is here!", description=f"Characters inside `<>` are variables, enter the variable without `<>`", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        embed.add_field(name="?source", value="My Github source code!", inline=False)
        embed.add_field(name="?leaderboard", value="Leaderboard for [CashoutCookie](https://cashoutcookie.com/rank)!", inline=False)
        embed.add_field(name="?profile `<username>`", value="User profile from [CashoutCookie](https://cashoutcookie.com)!", inline=False)
        embed.add_field(name="?login", value="Use the command to login to [CashoutCookie](https://cashoutcookie.com) here!", inline=False)
        embed.add_field(name="?emergency", value="Use this command **only** when there is a huge bug/mistake or any major problem, if it's some small bug or issue then directly ping @team", inline=False)
        embed.set_footer(text="🍪 For CashOut Cookie Games\n🔨 For Staff Commands (Only works for team members)")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction('🍪')
        await helpmsg.add_reaction('🔨')
        await helpmsg.add_reaction('<:delete:810190593338638347>')
        await asyncio.sleep(1)

        gamesembed = discord.Embed(title="Cookie Hunt!", description="```?cookiehunt```",color=discord.Colour.orange())
        gamesembed.add_field(name="Game", value="Play Cookie Hunt with someone! Guess where opponent's cookies are hidden and find them!", inline=False)
        gamesembed.add_field(name="Requirement", value="Login to [CashOut Cookie](https://cashoutcookie.com) on this server using the command `?login`", inline=False)
        gamesembed.add_field(name="Fee", value="100 cookies from both players.", inline=False)
        gamesembed.add_field(name="Rewards", value="200 Cookies for Victoey\n150 Cookies if opponent surrenders\n100 Cookies if opponent gets timed out (Not technically a win so fee amount is given back to the winner)", inline=False)
        gamesembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")


        embedstaff = discord.Embed(title="Staff commands", color=discord.Colour.teal())
        embedstaff.add_field(name="?embed `<colour>`", value="Answer the questions sent by me to make an embed! \n *Reacting to 🎨 will give all colour values*", inline=False)
        embedstaff.add_field(name="?cookies", value="Shows a list of all cookies stored.", inline=False)
        embedstaff.add_field(name="?clearcookies", value="Clears all cookies.", inline=False)
        embedstaff.add_field(name="?addcookies <CashOutCookieUsername> <DiscordUserID>", value="Adds cookies for any user which means they won't be required to log in to play CashOut Cookie Games.", inline=False)
        embedstaff.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        embedstaff.set_footer(text="🎨 Embed color values")


        embedcolours = discord.Embed(title="All embed colour values", description="Make sure to type the colour values in all lowercase letters.", color=discord.Colour.teal())
        embedcolours.add_field(name="teal", value="Colour with a value of 0x1abc9c.")
        embedcolours.add_field(name="green", value="Colour with a value of 0x2ecc71.")
        embedcolours.add_field(name="blue", value="Colour with a value of 0x3498db.")
        embedcolours.add_field(name="purple", value="Colour with a value of 0x9b59b6.")
        embedcolours.add_field(name="magenta", value="Colour with a value of 0xe91e63.")
        embedcolours.add_field(name="gold", value="Colour with a value of 0xf1c40f.")
        embedcolours.add_field(name="orange", value="Colour with a value of 0xe67e22.")
        embedcolours.add_field(name="red", value="Colour with a value of 0xe74c3c.")
        embedcolours.add_field(name="dark_teal", value="Colour with a value of 0x11806a.")
        embedcolours.add_field(name="dark_green", value="Colour with a value of 0x1f8b4c.")
        embedcolours.add_field(name="dark_blue", value="Colour with a value of 0x206694.")
        embedcolours.add_field(name="dark_purple", value="Colour with a value of 0x71368a.")
        embedcolours.add_field(name="dark_magenta", value="Colour with a value of 0xad1457.")
        embedcolours.add_field(name="dark_gold", value="Colour with a value of 0xc27c0e.")
        embedcolours.add_field(name="dark_orange", value="Colour with a value of 0xa84300.")
        embedcolours.add_field(name="dark_red", value="Colour with a value of 0x992d22.")
        embedcolours.add_field(name="light_gray", value="Colour with a value of 0x979c9f.")
        embedcolours.add_field(name="dark_gray", value="Colour with a value of 0x607d8b.")
        gamesembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")

        def check(reaction, user):
            return str(reaction.emoji) == '🍪' or str(reaction.emoji) == '<:delete:810190593338638347>' or str(reaction.emoji) == '🔨' and reaction.message == helpmsg
        reaction, user = await self.bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '🍪':
            await helpmsg.edit(embed=gamesembed)
            await helpmsg.clear_reaction('🍪')
            await helpmsg.clear_reaction('🔨')

        elif str(reaction.emoji) == '🔨' and user.guild_permissions.manage_messages:
            await helpmsg.clear_reactions()
            await helpmsg.add_reaction('🎨')
            await helpmsg.add_reaction('<:delete:810190593338638347>')
            await helpmsg.edit(embed=embedstaff)
        elif str(reaction.emoji) == '🔨' and not user.guild_permissions.manage_messages:
            await ctx.send(f"{user.mention} Sorry but you can't view staff commands as you are not a staff or team member,")

        elif str(reaction.emoji) == '<:delete:810190593338638347>':
            await helpmsg.delete()


        def check(reaction, user):
            return str(reaction.emoji) == '🎨' or str(reaction.emoji) == '<:delete:810190593338638347>' and reaction.message == helpmsg
        reaction, user = await self.bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '🎨':
            await helpmsg.clear_reaction('🎨')
            await helpmsg.edit(embed=embedcolours)
        elif str(reaction.emoji) == '<:delete:810190593338638347>':
            await helpmsg.delete()


        def check(reaction, user):
            return str(reaction.emoji) == '<:delete:810190593338638347>' and reaction.message == helpmsg
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        await helpmsg.delete()


def setup(bot):
    bot.add_cog(Help(bot))

