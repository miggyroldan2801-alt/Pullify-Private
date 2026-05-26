import discord
from discord.ext import commands
from errors import handle_api_error  # This imports from root

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Your existing commands/modals go here...
    @commands.command()
    async def verify(self, ctx):
        await ctx.send("Verification system ready.")

# THIS IS THE REQUIRED ENTRY POINT
async def setup(bot):
    await bot.add_cog(Verification(bot))