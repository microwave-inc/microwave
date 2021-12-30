import time
import discord
import psutil
import os
import requests

from datetime import datetime
from discord.ext import commands
from utils import default


class Information(commands.Cog):
    """Useful stuff"""
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=["invme", "botinvite"])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(f"**{ctx.author.name}**, use this URL to invite me\n<{discord.utils.oauth_url(self.bot.user.id)}>")

    @commands.command(aliases=["info", "stats", "status"])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(
            name=f"Developer/Owner{'' if len(self.config['owners']) == 1 else 's'}",
            value=", ".join([str(self.bot.get_user(x)) for x in self.config["owners"]]),
            inline=True
        )
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} (avg: {avgmembers:,.2f} users/server)", inline=True)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name='Website', value="http://microwavebot.tk", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{self.config['version']}** | updated: **{self.config['lastupdate']}**", embed=embed)

#source https://stackoverflow.com/questions/66653523/discord-py-how-to-make-a-bot-message-the-server-prefix-when-its-pinged
    @commands.Cog.listener()
    async def on_message(self, message):
        """Used for showing the user who pinged the bot the prefix"""
        if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
            await message.channel.send("My prefix is `m!` (not case sensitive)")

    @commands.command(aliases=["cl", "changes"])
    async def changelog(self, ctx):
        """Used for the changelog"""
        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name=f"Changelog for version {self.config['version']} (Date updated: {self.config['lastupdate']}", value= "Owner only: \n Eval command added \n Fixed reboot command \n\n Public changes: \n Added more 8ball responses", inline=True)

        await ctx.send(embed=embed)

#source: https://github.com/Eddy-Arch/Hentai-discord-bot/blob/master/index.py
    @commands.command(aliases=["covidstat", "covid", "covid-19"])
    async def coronavirus(self, ctx):


        embedColour = discord.Embed.Empty
        embed = discord.Embed(colour=embedColour)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour
        
        r = requests.get('https://corona-stats.online/' + '?format=json')
        stats = r.json()['data'][0]['country'], r.json()['data'][0]['cases']
        world = "worldwide cases:", r.json()['worldStats']['cases'], " cases today: ", r.json()['worldStats']['todayCases'] , " deaths: ", r.json()['worldStats']['deaths'], " died today", r.json()['worldStats']['todayDeaths'], " recovered: ", r.json()['worldStats']['recovered'], " critical: ", r.json()['worldStats']['critical'], " cases per one million: ", r.json()['worldStats']['casesPerOneMillion']
        embed.set_author(name=r.json()['data'][0]['country'])
        embed.add_field(value='cases:', name="===========================", inline=False)
        embed.add_field(value='cases today:', name=r.json()['data'][0]['cases'], inline=False)
        embed.add_field(value="recovered:", name=r.json()['data'][0]['todayCases'], inline=False)
        embed.add_field(value="deaths:", name=r.json()['data'][0]['recovered'], inline=False)
        embed.add_field(value="died today:", name=r.json()['data'][0]['deaths'], inline=False)
        embed.add_field(value="active:", name=r.json()['data'][0]['todayDeaths'], inline=False)
        embed.add_field(value="critical condition:", name=r.json()['data'][0]['active'], inline=False)
        embed.add_field(value=world, name=r.json()['data'][0]['critical'], inline=False)
        embed.set_author(name=r.json()['data'][0]['country'], icon_url=r.json()['data'][0]['countryInfo']['flag'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
