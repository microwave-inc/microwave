from utils import permissions, default, lists
import asyncio
import random
import os

import discord
from discord.ext import commands

from DiscordEconomy.Sqlite import Economy

eco = Economy(database_name='economy.db')

async def is_registered(ctx):
    r = await eco.is_registered(ctx.message.author.id)
    return r

is_registered = commands.check(is_registered)

config = default.config()

class Economy(commands.Cog):
    """Economy stuff"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(aliases=["bal", "bank"])
    @commands.guild_only()
    async def balance(self, ctx: commands.Context):
        """This command currently only works on yourself ;-;"""
        user = ctx.author
        #this bit here is directly stol- borrowed from their examples (https://github.com/Nohet/DiscordEconomy/blob/main/examples/dpy_base/messageCommands/bot.py)
        await eco.is_registered(user.id)
        bank = await eco.get_user(user.id)
        
    
        embed=discord.Embed(title=f"{user.name}'s balance", color=discord.Color.from_rgb(255, 255, 255))
        embed.add_field(name="Bank Balance:", value=f"`{bank.bank}`")
        embed.add_field(name="On hand cash:", value=f"`{bank.wallet}`")
        embed.add_field(name="Net worth:", value=f"`{bank.bank + bank.wallet}`")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def addmoney(self, ctx, amount: int, bank_wallet_thing: str, user: discord.Member = None):
        """This is an dev only command"""
        if user:
            await eco.is_registered(user.id)
            await eco.add_money(user.id, f"{bank_wallet_thing}", amount)
            await ctx.send(f"added {amount} to {user.name}'s {bank_wallet_thing}")
        else:
            await eco.add_money(ctx.author, f"{bank_wallet_thing}", amount)

    @commands.command()
    @is_registered
    @commands.cooldown(1, 10)
    @commands.guild_only()
    async def work(self, ctx):
        """A simple work command"""
        money = random.randint(10,3600)
        user = ctx.author
        await eco.is_registered(user.id)
        job = random.choice(lists.work)
        await eco.add_money(user.id, "bank", money)
        embed=discord.Embed(title=f"Work", color=discord.Color.from_rgb(255, 255, 255))
        embed.add_field(name="You worked as a:", value=f"{job}", inline=True)
        embed.add_field(name=f"from working as a {job} you gained:", value=f"{money} dollars!", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @is_registered
    @commands.cooldown(1, 86400)
    @commands.guild_only()
    async def daily(self, ctx):
        """A simple daily command"""
        user = ctx.author
        await eco.is_registered(user.id)
        bank = await eco.get_user(user.id)
        await eco.add_money(user.id, "bank", 1000)
        embed=discord.Embed(title=f"Daily", color=discord.Color.from_rgb(255, 255, 255))
        embed.add_field(name=f"from claiming your daily you gained:", value="1000 dollars")
        await ctx.send(embed=embed)
#these two commands are untested, some bug fixes may need to be made
    @commands.check(permissions.is_owner)
    async def removeuser(self, ctx, user: discord.Member = None):
        """Dev command for removing user info"""
        if user:

            await eco.delete_user_account(user.id)
            await ctx.send(f"User <@{user.id}>'s account info has been deleted")
        else:
            await ctx.send("you **MUST** specify a user or ID")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reset(self, ctx, author: discord.Member = None):
        """Resets all stats"""
        if author.id in config["dev"]:
            if os.path.exists("economy.db"):
                await os.remove("economy.db")
                await ctx.send("`economy.db` has been deleted and all progress reset.")
            else:
                await ctx.send("All progress was reset or something went wrong.")
        else:
            await ctx.send("You are not a developer.")

#might work who knows
    @commands.command(aliases=["slots", "bet"])
    @is_registered
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        user = ctx.author

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
            await eco.add_money(user.id, "bank", "5000")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
            await eco.add_money(user.id, "bank", 1000)
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")
    
#TODO
# - Add a custom cooldown error
# - Add a shop command
# - Add items for said shop command
# - Possibly add per server economy(?)

#CHANGELOG
# - Added a slots command (stolen from fun.py)

def setup(bot):
    bot.add_cog(Economy(bot))
