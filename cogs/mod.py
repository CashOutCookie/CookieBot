from pymongo import MongoClient
import discord, asyncio, os, json
from discord.ext import commands
from discord.ext.commands import has_permissions


client = MongoClient(os.environ.get("MONGO"))
db = client['discord']

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
    async def winners(self, ctx):
        questions = ["Month?",
                    "Winners (Use commas to seperate users)",
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
    
        channel = self.bot.get_channel(819169184930988032)
        month = answers[0]
        winners = answers[1].split(",")
        desc = answers[2]

        embed = discord.Embed(title=f'Winners | Month: {month}',
                            description=desc,
                            color=discord.Color.gold())
        embed.set_thumbnail(url = ctx.guild.icon_url)
        rank = 1
        for i in winners:
            embed.add_field(name=f"Rank {rank}", value=i, inline=False)
            rank += 1
        await channel.send(embed=embed)
        msgd = await ctx.send(f'Winners embed sent')
        await msgd.add_reaction("🗑")
        await asyncio.sleep(1)
        def check(reaction, user):
            return str(reaction.emoji) == '🗑' and reaction.message == msgd
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        await msgd.delete()


    @commands.command()
    @has_permissions(manage_messages=True)
    async def cache(self, ctx, serverid=None):
        if serverid is None:
            await ctx.send(embed=discord.Embed(description=json.dumps(self.bot.listcookies, indent=1), color=discord.Color.teal()))

        else:
            try:
                embed = discord.Embed(title=f"Auth cookies for the server: __{self.bot.get_guild(int(serverid))}__", color=discord.Color.magenta())
                data = self.bot.listcookies.get(str(serverid))
                for i in data:
                    embed.add_field(name=data[i], value=f"UserID: **{i}**", inline=False)
                await ctx.send(embed=embed)
            except Exception:
                await ctx.send("The server doesn't have any users logged in.")



    @commands.command()
    @has_permissions(manage_messages=True)
    async def removeuser(self, ctx, user=None):
        if user is None:
            await ctx.send("You need to define the user to log them out.\n Format: ```?removeuser <cashoutcookieusername>```")
        else:
            coll = db[str(ctx.author.guild.id)]
            userdata = { "username": user }
            coll.delete_one(userdata)
            await ctx.send(embed=discord.Embed(description=f"Done, removed auth cookies for [{user}](https://cashoutcookie.com/profile/{user})", color=discord.Color.green()))



    @commands.command()
    @has_permissions(manage_messages=True)
    async def adduser(self, ctx, name:str=None, *,userid:int=None):
        if name is not None and userid is not None:
            user = {"discordId": userid, "username": name}
            collection = db[str(ctx.author.guild.id)]
            collection.insert_one(user)
            await ctx.send("Added data for user " + name)

        elif name is None and userid is not None:
            await ctx.send("You need to enter CashOut Cookie username for the user first.\n Format: ```?adduser <cashoutcookieusername> <discorduserid>```")
        elif name is not None and userid is None:
            await ctx.send("You need to enter the user's id also.\n Format: ```?adduser <cashoutcookieusername> <discorduserid>```")
        else:
            await ctx.send("You need to specify the user's CashOut Cookie username and Discord User Id.\n Format: ```?adduser <cashoutcookieusername> <discorduserid>```")



async def on_message(message):
    if str(message.channel) == '📃todo' and not message.content.startswith("TO-DO"):
        await message.delete()
        
def setup(bot):
    bot.add_cog(Mod(bot))
