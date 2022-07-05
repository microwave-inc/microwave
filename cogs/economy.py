from utils import permissions, default, lists, shop
shop = shop.shop
import asyncio
import random
import os
import datetime 
from datetime import datetime
import sqlite3

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
    @is_registered
    @commands.cooldown(1, 10)
    @commands.guild_only()
    async def work(self, ctx):
        """A simple work command"""
        money = random.randint(10,1000)
        user = ctx.author
        await eco.is_registered(user.id)
        job = random.choice(lists.work)
        embed=discord.Embed(title=f"Work", color=discord.Color.from_rgb(255, 255, 255))
        if job == "A Microwave Bot developer": #Just ask the team, they all agreed to volunteer as a dev... I'm not kidding......
            embed.add_field(name="You worked as a:", value=f"{job}", inline=True)
            embed.add_field(name=f"from working as a {job} you gained:", value=f"No money, you volunteered for this smh, no payment", inline=True)
        else:
            await eco.add_money(user.id, "bank", money)
            embed.add_field(name="You worked as a:", value=f"{job}", inline=True)
            embed.add_field(name=f"from working as a {job} you gained:", value=f"{money} dollars!", inline=True)
            if money == "69" or "420":
                embed.add_field(name="Hehe nice!", value="gotta love the funny numbers")
                await ctx.send(embed=embed)
            else:
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
            await ctx.send(f"{slotmachine} All matching, you won! 🎉 1000 Dollars has been added to your account")
            await eco.add_money(user.id, "bank", "1000")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉 500 Dollars has been added to your account")
            await eco.add_money(user.id, "bank", "500")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command(aliases=["lottery", "goodluckonthisonebud"])#I doubt this works
    @is_registered
    @commands.cooldown(1, 3600) #a hours's cooldown
    async def lotto(self, ctx):
        random = random.int(1,100000)
        user = ctx.author
        now = datetime.now()
        time = now.strftime("%m/%d/%Y, %H:%M:%S")

        if (random == "69"):
            await eco.add_money(user.id, "bank" "9999999999")
            await ctx.send("Wow you won a lot of money!")
            print(f"{user.name} won money") #since the chance is so low I want to log if someone wins
            with open('winners.txt', 'w') as f:
                f.write(f"{user.name} won at {time}")
                f.write("\n")
        else:
            await ctx.send("You didn't win, very sad....")
#I doubt anything below works period half of it is just me letting github copilot do it's thing

    @commands.command()
    @is_registered
    async def shop(self, ctx):
        """Lists all items in the shop"""
        embed=discord.Embed(title=f"Shop", color=discord.Color.from_rgb(255, 255, 255))
        for item in shop["items"].items():
            if item[1]["available"]:
              embed.add_field(name=item[1]["name"].capitalize(), value=f"Price: **{item[1]['price']}** \nDescription: **{item[1]['description']}**")
            #taken from https://github.com/Nohet/DiscordEconomy/blob/83808e18ecdd8bea269200d5f37c3f0a666aa863/examples/dpy_base/messageCommands/bot.py#L258
        await ctx.send(content="Here is a list of all items in the shop:", embed=embed)

    @commands.command()
    @is_registered
    async def buy(self, ctx, item: str):
        """Buys an item from the shop"""
        item = item.lower()
        user = ctx.author
        bank = await eco.get_user(user.id)
        if item not in bank.items:
          if item in shop["items"]:
              if shop["items"][item]["available"] == True:
                  if bank.bank >= shop["items"][item]["price"]:
                      await eco.remove_money(user.id, "bank", shop["items"][item]["price"])
                      await eco.add_item(user.id, item)
                      await ctx.send(f"You have bought {item.capitalize()} for {shop['items'][item]['price']} dollars")
                  else:
                      await ctx.send("You don't have enough money")
              else:
                  await ctx.send("This item is not available")
          else:
              await ctx.send("This item does not exist")
        else:
            await ctx.send("You can only own one of each item!")

    @commands.command()
    @is_registered
    async def sell(self, ctx, item: str):
        """Sell an item from your inventory"""
        item = item.lower()
        user = ctx.author
        bank = await eco.get_user(user.id)
        if item in shop["items"]:
            if item not in bank.items:
                await ctx.send("You don't have this item")
            else:
                if shop["items"][item]["price"] > 0:
                    await eco.add_money(user.id, "bank", shop["items"][item]["price"] / 2)
                    await eco.remove_item(user.id, item)
                    await ctx.send(f"You have sold {item.capitalize()} for {shop['items'][item]['price'] / 2} dollars")
                else:
                    await eco.remove_item(user.id, item)
                    await ctx.send(f"You have sold {item.capitalize()} for nothing")
        else:
            await ctx.send("This item does not exist")


    @commands.command(aliases=["inv"])
    @is_registered
    async def inventory(self, ctx):
        """Shows your inventory"""
        user = ctx.author
        inv = await eco.get_user(user.id)
        embed=discord.Embed(title=f"Inventory", color=discord.Color.from_rgb(255, 255, 255))
#        if user != None:
#            if inv.items == None:
#                embed.add_field(name="Hey!", value="They have no items")
#            else:
#                for item in inv.items:
#                    embed.add_field(name=item.capitalize(), value=f"Price: **{shop['items'][item]['price']}** \nDescription: **{shop['items'][item]['description']}**")
#        else:
#            pass
        if inv.items == "":
            embed.add_field(name="Hey!", value="You have no items")
        else:
            pass
        for item in inv.items:
            embed.add_field(name=item.capitalize(), value=f"""Price: **{shop['items'][item]['price']}** \nDescription: **{shop['items'][item]['description']}**""")
        await ctx.send(content="Here is a list of all items in your inventory:", embed=embed)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def additem(self, ctx, item: str, user: discord.member = None):# = discord.member = None):
        """Adds an item to an inventory"""
        item = item.lower()
        if item not in shop["items"]:
            await ctx.send("This item doesn't exist")
        else:
            if user != None:
                await eco.is_registered(user)
                await eco.add_item(user.id, item)
                await ctx.send(f"You have added {item.capitalize()} to {user}'s inventory")
            else:
                await eco.is_registered(user)
                await eco.add_item(ctx.author.id, item)
                await ctx.send(f"You have added {item.capitalize()} to your inventory")

    @commands.command()
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
    async def resetall(self, ctx):
        """Resets all stats"""
        user = ctx.author
        if user.id in config["devs"]:
            if os.path.exists("economy.db"):
                os.remove("economy.db")
                await ctx.send("`economy.db` has been deleted and all progress reset.")
            else:
                await ctx.send("All progress was reset or something went wrong.")
        else:
            await ctx.send("You are not a developer.")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def addmoney(self, ctx, amount: int, bank_wallet_thing: str, user: discord.Member = None):
        """This is an dev only command"""
        if user:
            await eco.is_registered(user.id)
            await eco.add_money(user.id, f"{bank_wallet_thing}", amount)
            await ctx.send(f"added {amount} to {user.name}'s {bank_wallet_thing}")
        else:
            user = ctx.author
            await eco.add_money(ctx.author, f"{bank_wallet_thing}", amount)
            await ctx.send(f"added {amount} to {user.name}'s {bank_wallet_thing}")

#TODO
# - Add a custom cooldown error
# - Possibly add per server economy(?)

#CHANGELOG
# - Added a new group command for all the dev stuff related to economy

def setup(bot):
    bot.add_cog(Economy(bot))
