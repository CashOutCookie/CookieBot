from aiohttp import request
from pymongo import MongoClient
from discord.ext import commands
import discord, json, asyncio, os

client = MongoClient(os.environ.get("MONGO_URL"))
db = client['discord']


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def login(self, ctx):
        if self.bot.listcookies.get(str(ctx.author.guild.id) != None and ctx.author.id in self.bot.listcookies.get(str(ctx.author.guild.id)).keys()):
            await ctx.send(f"You are already logged in, {ctx.author.name} :eyes:")

        else:
            embed = discord.Embed(title="Login to CashOut Cookie", 
                            description="Enter your login credentials for [CashOut Cookie](https://cashoutcookie.com) here, I promise I will keep it a secret!", 
                            color=discord.Color.teal())
            embed.add_field(name="Format", value="```login <YourUsername> <YourPassword>```")
            embed.set_footer(text="Values inside angle brackets (<>) are variables, replace the default values with your credentials and remove the angle brackets.")

            try:
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                await ctx.send(f"You need to enable your DMs so that I can message you and check your login credentials {ctx.author.name} 🤠")
            
            def check(m):
                return m.author == ctx.author and m.guild is None
            try:
                logindata = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.author.send("You took too long to login ⏲, try again")

            if str(logindata.content.startswith("login")):

                BOT_LOGIN = os.environ.get("BOT_LOGIN")
                data = {"username": logindata.content.split(" ")[1].lower(), "password": logindata.content.split(" ")[2]}
                credentials = json.dumps(data)

                await ctx.author.send("Trying to log in with the credentials provided...")
                async with request("POST", BOT_LOGIN, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
                    if response.status == 202:
                        collection = db[str(ctx.author.guild.id)]
                        loggedIn = False
                        for user in collection.find():
                            if(user["username"] == data["username"]):
                                loggedIn = True
                        if loggedIn:
                            await ctx.author.send(embed=discord.Embed(description="You have already logged into the server, don't try to cheat :eyes:", color=discord.Colour.red()))
                        else:                            
                            user = {"discordId":ctx.author.id,"username":data["username"]}
                            collection.insert_one(user)
                            await ctx.author.send(embed=discord.Embed(title="Successfully logged in to CashOut Cookie!", color=discord.Colour.green()))
                    else:
                        await ctx.author.send(embed=discord.Embed(title="Username or Password are invalid", description="The username and password combination you entered is invalid, try again with the same command (`?login`)", color=discord.Color.red()))

            else:
                await ctx.author.send("You need to use 'login' in the beginning of your message.\n Example: ```login thisismyusername mysecretpassword123``` Try again using.")

    @commands.command()
    async def logout(self, ctx):
        coll = db[str(ctx.author.guild.id)]
        userdata = { "discordId": ctx.author.id }
        coll.delete_one(userdata)
        await ctx.send(embed=discord.Embed(description=f"Done, successfully logged you out of this server from [CashOut Cookie](https://cashoutcookie.com), {ctx.author.name} :)", color=discord.Color.green()))



def setup(bot): 
    bot.add_cog(Auth(bot))

