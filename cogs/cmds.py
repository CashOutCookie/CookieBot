import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(title="Github Source Code", description="[CashOutCookie - CookieBot](https://github.com/CashOutCookie/CookieBot)", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/octicons/1024/mark-github-512.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def idea(self, ctx, *, ideadesc=None):
        if ideadesc is not None:
            channel = self.bot.get_channel(819150553032556574)
            embed = discord.Embed(title=f"{ctx.author.name}'s idea", description=f"This idea came from server **{ctx.author.guild.name}**!", color=discord.Color.teal())
            embed.add_field(name="Suggestion", value=ideadesc)
            msg = await channel.send(embed=embed)
            msg.add_reaction("✅")
            msg.add_reaction("❌")
        else:
            await ctx.send("You need to describe your idea too! This is the format: ```?idea <YourIdeaDescription>```")

    @commands.command()
    async def flag(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(title="k3VhWLcG7NupoOOR", description="Good job!",color=discord.Color.teal())
            embed.add_field(name="Description", value="Now enter this in flag at [CashOut Cookie](https://cashoutcookie.com/ctf) to proceed!")
            embed.add_field(name="Addtional", value="none")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))
