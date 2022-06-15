import discord
import requests
import random

from discord.ext import commands
from utils import lists, permissions, http, default

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

def setup(bot):
    bot.add_cog(apis(bot))
