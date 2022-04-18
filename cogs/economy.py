from utils import permissions, default, lists
import asyncio
import random

import discord
from discord.ext import commands

from DiscordEconomy.Sqlite import Economy

eco = Economy(database_name='economy.db')

async def is_registered(ctx):
    r = await eco.is_registered(ctx.message.author.id)
    return r

is_registered = commands.check(is_registered)


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
            await ctx.send("yeah I think you fucked the command")

    @commands.command()
    @is_registered
    @commands.cooldown(1, 10)
    @commands.guild_only()
    async def work(self, ctx):
        """A simple work command"""
        money = random.randint(10,100)
        user = ctx.author
        await eco.is_registered(user.id)
        bank = await eco.get_user(user.id)
        job = random.choice(lists.work)
        await eco.add_money(user.id, "bank", money)
        embed=discord.Embed(title=f"Work", color=discord.Color.from_rgb(255, 255, 255))
        embed.add_field(name="You worked as a:", value=f"{job}")
        embed.add_field(name=f"from working as a {job} you gained:", value=f"{money}!")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))