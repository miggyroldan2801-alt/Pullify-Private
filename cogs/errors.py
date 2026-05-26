from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"An error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Errors(bot))