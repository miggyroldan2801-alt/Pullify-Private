import discord
from discord.ext import commands
import datetime

# Admin-controlled toggles
SECURITY_CONFIG = {"ban_alts": True, "ban_vpns": True, "detect_bots": True}

class VerificationModal(discord.ui.Modal, title='Security Verification'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        
        # 1. Bot/Suspicious Detection
        if SECURITY_CONFIG["detect_bots"] and (user.bot or (user.avatar is None and (datetime.datetime.now(datetime.timezone.utc) - user.created_at).days < 1)):
            await interaction.response.send_message("Account flagged as suspicious.", ephemeral=True)
            return

        # 2. Alt Detection
        if SECURITY_CONFIG["ban_alts"]:
            if (datetime.datetime.now(datetime.timezone.utc) - user.created_at).days < 7:
                await interaction.response.send_message("Account too young.", ephemeral=True)
                return

        await interaction.response.send_message("Verification passed.", ephemeral=True)

class VerificationView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Verify', style=discord.ButtonStyle.primary, custom_id='verify_btn')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerificationModal(self.bot))

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_verification(self, ctx):
        await ctx.send("Press to verify:", view=VerificationView(self.bot))

async def setup(bot):
    await bot.add_cog(Verification(bot))