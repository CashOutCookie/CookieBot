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
    async def emergency(self, ctx):
        modchannel = self.bot.get_channel(812560533428502531)
        embed = discord.Embed(title="Spam Ping Started..", description=f"Busy spam pinging the team in DMs for your help {ctx.author.name}", color=discord.Color.orange())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/807140294764003350/818505400449761351/cookiemoney.png")
        await ctx.send(embed=embed)
        await modchannel.send("EMERGENCY SLOTHS! SOMEONE NEEDS YOUR HELP <@&819944514558492673>")
        await modchannel.send(f"<@&819944514558492673> user which used the command is {ctx.author.name} btw")
        await modchannel.send(f"<@&819944514558492673> this is their id {ctx.author.id}")
        await modchannel.send(f"<@&819944514558492673> Help them!")
        await modchannel.send("<@&819944514558492673>")
        await modchannel.send("<@&819944514558492673>")


def setup(bot):
    bot.add_cog(Commands(bot))
