import discord
from discord.ext import commands
from base import EmbedFactory

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=EmbedFactory.error_embed("You lack permissions for this action."))
        else:
            await ctx.send(embed=EmbedFactory.error_embed(f"An unexpected error occurred: {str(error)}"))

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))