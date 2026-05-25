import discord
from discord import app_commands
from discord.ext import commands
from base import EmbedFactory

class Utilities(commands.Cog):
    @app_commands.command(name="userinfo", description="Get user details")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = EmbedFactory.create_embed("User Info", f"Name: {member.name}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))