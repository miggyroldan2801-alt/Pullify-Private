from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        await ctx.send("Contact the support team here: [Link]")

async def setup(bot):
    await bot.add_cog(Support(bot))