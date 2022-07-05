import discord
import psutil
import os
import random

from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import errors
from utils import default, lists


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            error = default.traceback_maker(err.original)

            if "2000 or fewer" in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send(
                    "You attempted to make the command display more than 2,000 characters...\n"
                    "Both error and command will be ignored."
                )

            await ctx.send(f"There was an error processing the command ;-;\nplease email help@microwavebot.tech a screenshot of the error and we will fix it asap\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send("You've reached max capacity of command usage at once, please finish the previous one...")

        elif isinstance(err, errors.CommandOnCooldown):
            #await ctx.send(f"This command is on cooldown... try again in {round(error.retry_after, 2)} seconds.")
            embed = discord.Embed(title="You're on a cooldown!", color=discord.Color.blue()) #https://stackoverflow.com/questions/64569898/how-do-i-make-cooldown-display-in-minsseconds-discord-py
            
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)

            embed.add_field(name="\u200b", value=f"Slow down will ya?\nWait for {self.leadingZero(minutes)}:{self.leadingZero(seconds)}.")
            await ctx.send(embed=embed)

            def leadingZero(self, time: str):
                if len(time) > 1:
                    return time

                return "0" + time

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not self.config["join_message"]:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config["join_message"])

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            print(f"Private message > {ctx.author} > {ctx.message.clean_content}")
        if ctx.author.id in lists.blacklistedids:
            return await ctx.send("You are blacklisted from using this bot. If you think this is a mistake, please contact us at blacklists@microwavebot.tech")
        else:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        """ The function that activates when boot was completed """
        
        if not hasattr(self.bot, "uptime"):
            self.bot.uptime = datetime.utcnow()

        status = random.choice(lists.listeningstatus)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        
        # Indicate that the bot has successfully booted up
        print(f"Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Users: {len(self.bot.users)} | Version: {self.config['version']} | Last Update: {self.config['lastupdate']}")


def setup(bot):
    bot.add_cog(Events(bot))
