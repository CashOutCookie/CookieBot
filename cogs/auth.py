from aiohttp import request
from discord.ext import commands
import discord, json, asyncio, os


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def login(self, ctx):
            embed = discord.Embed(title="Login to CashOut Cookie", description="Enter your login credentials for [CashOut Cookie](https://cashoutcookie.com) here, I promise I will keep it a secret!", color=discord.Color.teal())
            embed.add_field(name="Format", value="```login <YourUsername> <YourPassword>```")
            embed.set_footer(text="Values inside angle brackets (<>) are variables, replace the default values with your credentials and remove the angle brackets.")

            try:
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                await ctx.send(f"You need to enable DMs so that i can message you and check your login credentials {ctx.author.name}.")
            

            def check(m):
                return m.author == ctx.author and m.guild is None
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.author.send("You took too long to login, try again by using the same command (`?login`)")

            if str(msg.content.startswith("login")):
                try:

                    BOT_LOGIN = os.environ.get("BOT_LOGIN")
                    data = {"username": msg.content.split(" ")[1], "password": msg.content.split(" ")[2]}
                    credentials = json.dumps(data)
                    await ctx.author.send("Trying to log in with the credentials provided...")
                    async with request("POST", BOT_LOGIN, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
                        if response.status == 202:
                            self.bot.listcookies.append((msg.content.split(" ")[1], ctx.author.id))
                            await ctx.author.send(embed=discord.Embed(title="Successfully logged in to CashOut Cookie!", color=discord.Colour.green()))
                        elif response.status == 406:
                            await ctx.author.send(embed=discord.Embed(title="Wrong Password", description="The password you entered is invalid, try again with the same command (`?login`)", color=discord.Color.orange()))
                        else:
                            await ctx.author.send(embed=discord.Embed(title="Username or Password are invalid", description="The username and password combination you entered is invalid, try again with the same command (`?login`)", color=discord.Color.red()))

                except:
                    await ctx.author.send("You need to use 'login' in the beginning of your message,\n Example: ```login myepicusername mysecretpassword123``` Try again using `?login`.")

def setup(bot): 
    bot.add_cog(Auth(bot))

