import discord
from discord import app_commands
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Your User ID is now set
        self.owner_id = 1424069313341554879 

    @app_commands.command(name="sync", description="Force sync slash commands")
    async def sync(self, interaction: discord.Interaction):
        # Check if the person running the command is you
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("You are not the owner!", ephemeral=True)
            return

        # Perform the sync
        synced = await self.bot.tree.sync(guild=interaction.guild)
        await interaction.response.send_message(f"Successfully synced {len(synced)} commands.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Sync(bot))