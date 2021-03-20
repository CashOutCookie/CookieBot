import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    @has_permissions(manage_messages=True)
    async def embed(self, ctx, color=None):
        if color is not None:
            questions = ["In which channel do you wanna send the embed?",
                        "Title?",
                        "Description?"]
            answers = []

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            for i in questions:
                await ctx.send(i)
                try: 
                    msg = await self.bot.wait_for('message', timeout=100.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Command expires after 100 seconds. Be more quick 🦥')
                    return
                else:
                    answers.append(msg.content)
            try:
                channel_id = int(answers[0][2:-1])
            except:
                await ctx.send('You didn\'t mentioned the channel properly 😂')
                return

            channel = self.bot.get_channel(channel_id)
            title = answers[1]
            des = answers[2]
            embed = discord.Embed(title=f'{title}',
                                description=f'{des}',
                                color=getattr(discord.Colour, color)())
            embed.set_thumbnail(url = ctx.guild.icon_url)

            await channel.send(embed=embed)
            msgd = await ctx.send(f'Embed for {channel.mention} sent')
            await msgd.add_reaction("🗑")
            await asyncio.sleep(1)
            def check(reaction, user):
                return str(reaction.emoji) == '🗑' and reaction.message == msgd
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            await msgd.delete()
        else:
            await ctx.send("__You must specify a colour value!__\n *React to the 🎨 emoji in staff help message to get all the values*")


    @commands.command()
    @has_permissions(manage_messages=True)
    async def cookies(self, ctx):
        await ctx.send(self.bot.listcookies)

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clearcookies(self, ctx):
        self.bot.listcookies.clear()
        await ctx.send("Done")

    @commands.command()
    @has_permissions(manage_messages=True)
    async def addcookies(self, ctx, *, name:str=None, userid:int=None):
        self.bot.listcookies.append((name, userid))
        await ctx.send("Added data for user" + name)



def setup(bot):
    bot.add_cog(Mod(bot))
