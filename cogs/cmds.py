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
    async def idea(self, ctx, *, idea):
        if idea is None:
            await ctx.send("You need to describe your idea too! This is the format: ```?idea <YourIdeaDescription>```")
        else:
            channel = self.bot.get_channel(819150553032556574)
            embed = discord.Embed(title=f"{ctx.author.name}'s idea", description=f"This idea came from server **{ctx.author.guild.name}**!", color=discord.Color.teal())
            embed.add_field(name="Suggestion", value=idea)
            msg = await channel.send(embed=embed)
            msg.add_reaction("✅")
            msg.add_reaction("❌")

def setup(bot):
    bot.add_cog(Commands(bot))
