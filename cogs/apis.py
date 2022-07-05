import discord
import requests
import random
import locale
import os
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

from datetime import datetime
from discord.ext import commands
from utils import lists, permissions, http, default

apikey = os.getenv("APIKEY")
if os.getenv("APIKEY") == None:
    apikey = "DEMO_KEY"
else:
    apikey = os.getenv("APIKEY")

class apis(commands.Cog):
    """The new location for the API stuff"""
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, "https://random-d.uk/api/v1/random", "url")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Find the 'best' definition to your words """
        async with ctx.channel.typing():
            try:
                url = await http.get(f"https://api.urbandictionary.com/v0/define?term={search}", res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url["list"]):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")

    @commands.command()
    async def tot(self, ctx):
        """This or that"""
        #just defining some things
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        embed = discord.Embed(title="This or That?", colour=embedcolor)
        r = requests.get("http://itsthisforthat.com/api.php?json")

        embed.add_field(name="This:", value=r.json()['this'], inline=False)
        embed.add_field(name="Or", value="‎", inline=False) #the unicode char is just an empty char because discord gets fussy
        embed.add_field(name="That:", value=r.json()['that'])
        await ctx.send(embed=embed)

    @commands.command(aliases=["ye"])
    async def kanye(self, ctx):
        """a Kanye quote"""
        r = requests.get("https://api.kanye.rest/")
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        embed = discord.Embed(title="Kanye quote", colour=embedcolor)

        embed.add_field(name="Kanye says:", value=r.json()["quote"])
        await ctx.send(embed=embed)

#source: https://github.com/Eddy-Arch/Hentai-discord-bot/blob/master/index.py heavily modded
    @commands.command(aliases=["covidstat", "covid", "covid-19"])
    @commands.check(permissions.is_owner)
    async def coronavirus(self, ctx, otext=''):
        """Gives you covid-19 stats on a country (must be a valid name or abreviation)"""

        def getCountryList():
            res = requests.get('https://corona-stats.online?format=json')
            json = res.json()
            data = json['data']
            countryCodes = []
            for i in range(len(data)):
                cc = data[i]['countryCode']
                name = data[i]['country']

                if cc == '' or cc == None:
                    full = name
                else:
                    full = f"{cc} {name} :flag_{cc.lower()}:"
                
                countryCodes.append(f"- {full}")

            sortedCodes = sorted(countryCodes)

            return sortedCodes # 225 countries

        if otext == 'list':
            countryList = getCountryList()
            embedContent = ''

            for i in range(25):
                embedContent += countryList[i] + '\n'

            embed = discord.Embed(title='Available Countries')
            embed.add_field(value=embedContent, name="First 25", inline=False)

            msg = await ctx.send(embed=embed)

            await msg.add_reaction('◀️')
            await msg.add_reaction('▶️')

            return

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
        #random color if in guild
        r = random.randint(0, 255);b = random.randint(0, 255);g = random.randint(0, 255)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = discord.Color.from_rgb(r,g,b)
        else:
            #color white if in DM
            embedColour = discord.Color.from_rgb(255,255,255)

        r = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={apikey}')
        embed.set_author(name=r.json()['title'])
        #embed.add_field(name="Copyright:", value=r.json()['copyright'])
        embed.add_field(name="Date:", value=r.json()['date'])
        embed.set_image(url=r.json()['url'])
        #embed.add_field(name="Photo Description:", value=r.json()['explanation'], inline=True)
        embed.set_footer(text=f"API supplied by NASA, requested by {ctx.author.name}")
        await ctx.send(embed=embed)

#commands below are not tested and most likely doesn't work. Will fix when able
    @commands.command()
    async def ISS(self, ctx):
        r = requests.get("http://api.open-notify.org/iss-now.json")
        loclong = r.json()["iss_position"]["longitude"]
        loclat = r.json()["iss_position"]["latitude"]
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        embed=discord.Embed(title="ISS Location", colour=embedcolor)
        embed.add_field(name="Longitude:", value=loclong, inline=False)
        embed.add_field(name="Latitude:", value=longlat, inline=False)
        embed.add_field(name="Location:", value="W.I.P", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def coffee(self, ctx):
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        r = requests.get("https://coffee.alexflipnote.dev/random.json")
        embed=discord.Embed(title="Here is your image!", colour=embedcolor)
        embed.image(url=r.json()["file"])
        await ctx.send(embed=embed)

    @commands.command()
    async def weather(self, ctx, city: str):
        r = requests.get(f"https://goweather.herokuapp.com/weather/{city}")
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        if city == "":
            city = "Seattle"
        else:
            embed = discord.Embed(title=f"Weather for {city}", colour=embedcolor)
            embed.add_field(name="Current temp (C):", value=r.json()["temperature"])
            embed.add_field(name="Wind speed (Km/h):", value=r.json()["wind"])
            embed.add_field(name="Weather description:", value=r.json()["description"])
            await ctx.send(embed=embed)

    @commands.command(aliases=["breakingbadquote"])
    async def bbquote(self, ctx):
        r = requests.get("https://api.breakingbadquotes.xyz/v1/quotes/1")
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        embed=discord.Embed(title="Breaking bad quote", colour=embedcolor)
        embed.add_field(name=f"Here is your quote:", value=r.json()["quote"])
        await ctx.send(embed=embed)

    @commands.command() # I am terrible at coding if this doesn't work
    async def idsearch(self, ctx, userid: discord.member.id = None):
        r = requests.get(f"https://discord-api.microwavebot.tech/discord/user/{userid}")
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        embedcolor = discord.Color.from_rgb(a,b,c)
        if userid == None:
            await ctx.send("Please add an ID (or a valid one)")
        else:
            embed=discord.Embed(title=f"ID search", colour=embedcolor, thumbnail=r.json()["url"])
            embed.add_field(name="Username:", value=r.json()["username"])
            embed.add_field(name="Discrim:", value=r.json()["discriminator"])
            embed.add_field(name="Are they a bot:", value=r.json()["Bot"])
            embed.set_footer(text="Tada!")
        await ctx.send(embed=embed)

    @commands.command() #this command has a like 90% chance of working
    async def advice(self, ctx):
        """Ya need some advice? Here you go."""
        r = requests.get("https://api.adviceslip.com/advice")
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        color = discord.Color.from_rgb(a,b,c)
        embed = discord.Embed(title="You need some **random** advice", colour=color)
        embed.add_field(name="Advice:", value=r.json()["slip"]["advice"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(apis(bot))