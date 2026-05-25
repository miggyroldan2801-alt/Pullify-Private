import discord
from discord.ext import commands
import json
from base import EmbedFactory

with open("private_config.json", "r") as f:
    ALLOWED_GUILDS = json.load(f)["ALLOWED_GUILD_IDS"]

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(VerificationView())

class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_btn")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Implementation: Assign role or log verification
        await interaction.response.send_message(embed=EmbedFactory.create_embed("Verification", "Access granted."), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Verification(bot))