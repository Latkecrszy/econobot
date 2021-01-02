import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import CommandNotFound, BadArgument, CommandOnCooldown
from discord.ext.commands.errors import CommandInvokeError


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            print("Error: Command not found.")
            await ctx.send(f"I could not find that command, {ctx.author.mention}")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''Error: Missing one or more required argument.''')
        elif isinstance(error, BadArgument):
            await ctx.send("Please enter a proper argument for this command.")
        elif isinstance(error, commands.errors.CheckFailure):
            embed = discord.Embed(
                title=f"This command is currently disabled for you, {ctx.author.mention}!",
                description=None, color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, CommandOnCooldown):
            CmdHr = int(error.retry_after/3600)
            CmdMin = int(int(error.retry_after%3600)/60)
            CmdSec = int(int(error.retry_after%3600)%60)
            embed = discord.Embed(title=f"This command is on cooldown, {ctx.author}.", description=f"Try again in {CmdHr} hours, {CmdMin} minutes, and {CmdSec} seconds.", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(
                title=f"Sorry, I don't have adequate permissions to accomplish that task. Try dragging my role higher in server settings to fix this.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, CommandInvokeError):
            if str(ctx.command) != "rps":
                embed = discord.Embed(title=f"Sorry, something went wrong in the command. Please check that you are inputting correct arguments, and try again!",
                                  color=discord.Color.red())
                await ctx.send(embed=embed)
                raise error
        else:
            raise error


def setup(bot):
    bot.add_cog(ErrorCog(bot))

