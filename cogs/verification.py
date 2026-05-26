import discord
from discord.ext import commands
from errors import handle_api_error

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        await ctx.send("Pullify Security System: Active.")

async def setup(bot):
    await bot.add_cog(Verification(bot))