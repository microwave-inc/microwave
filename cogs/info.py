import time
import discord
import psutil
import os
import requests
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

from datetime import datetime
from discord.ext import commands
from utils import default

apikey = os.getenv("APIKEY")


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
            name=f"Developer{'' if len(self.config['devs']) == 1 else 's'}",
            value=", ".join([str(self.bot.get_user(x)) for x in self.config["devs"]]),
            inline=True
        )
        embed.add_field(
            name=f"Owner{'' if len(self.config['trueowners']) == 1 else 's'}",
            value=", ".join([str(self.bot.get_user(x)) for x in self.config["trueowners"]]),
            inline=True
        )
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} (avg: {avgmembers:,.2f} users/server)", inline=True)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name='Website', value="[click here](https://microwavebot.tech)", inline=True)

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
        embed.add_field(name=f"Changelog for version {self.config['version']} (Date updated: {self.config['lastupdate']}", value= "Added Astrology Picture of The Day command (thank you NASA for the API)", inline=True)

        await ctx.send(embed=embed)

#source: https://github.com/Eddy-Arch/Hentai-discord-bot/blob/master/index.py heavily modded
    @commands.command(aliases=["covidstat", "covid", "covid-19"])
    async def coronavirus(self, ctx, otext=''):
        """Gives you covid-19 stats on a country (must be a valid name or abreviation"""

        if otext == '': text = 'USA'
        else: text = otext

        embedColour = discord.Embed.Empty
        embed = discord.Embed(colour=embedColour)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour
    
        r = requests.get(f'https://corona-stats.online/{text}?format=json')
        # stats = r.json()['data'][0]['country'], r.json()['data'][0]['cases']
        # world = "worldwide cases:", r.json()['worldStats']['cases'], " cases today: ", r.json()['worldStats']['todayCases'] , " deaths: ", r.json()['worldStats']['deaths'], " died today", r.json()['worldStats']['todayDeaths'], " recovered: ", r.json()['worldStats']['recovered'], " critical: ", r.json()['worldStats']['critical'], " cases per one million: ", r.json()['worldStats']['casesPerOneMillion']
        embed.set_author(name=r.json()['data'][0]['country'], icon_url=r.json()['data'][0]['countryInfo']['flag'])
        embed.add_field(value='cases:', name="===========================", inline=False)
        embed.add_field(value='cases today:', name=locale.format("%d", r.json()['data'][0]['cases'], grouping=True), inline=False)
        embed.add_field(value="recovered:", name=locale.format("%d", r.json()['data'][0]['todayCases'], grouping=True), inline=False)
        embed.add_field(value="deaths:", name=locale.format("%d", r.json()['data'][0]['recovered'], grouping=True), inline=False)
        embed.add_field(value="died today:", name=locale.format("%d", r.json()['data'][0]['deaths'], grouping=True), inline=False)
        embed.add_field(value="active:", name=locale.format("%d", r.json()['data'][0]['todayDeaths'], grouping=True), inline=False)
        embed.add_field(value="critical condition:", name=locale.format("%d", r.json()['data'][0]['active'], grouping=True), inline=False)
        embed.add_field(value='world cases:', name=locale.format("%d", r.json()['data'][0]['critical'], grouping=True), inline=False)
        embed.set_footer(text=locale.format("%d", r.json()['worldStats']['cases'], grouping=True))
        await ctx.send(embed=embed)

    @commands.command(aliases=["nasa", "spacepics"])
    async def apod(self, ctx):
        embedColour = discord.Embed.Empty
        embed = discord.Embed(colour=embedColour)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        r = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={apikey}')
        embed.set_author(name=r.json()['title'])
        embed.add_field(name="Copyright:", value=r.json()['copyright'])
        embed.add_field(name="Date:", value=r.json()['date'])
        embed.set_image(url=r.json()['url'])
        embed.add_field(name="Photo Description:", value=r.json()['explanation'], inline=True)
        embed.set_footer(text="API supplied by nasa")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
