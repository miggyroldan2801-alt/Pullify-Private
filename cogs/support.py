import discord
from discord import app_commands
from discord.ext import commands
from base import EmbedFactory

class Support(commands.Cog):
    @app_commands.command(name="log", description="Log a moderator note")
    async def log_note(self, interaction: discord.Interaction, member: discord.Member, note: str):
        # Log to DB and post embedded log
        await interaction.response.send_message(embed=EmbedFactory.create_embed("Moderator Log", f"Note added for {member.mention}: {note}"), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Support(bot))