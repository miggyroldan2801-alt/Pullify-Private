import discord
import datetime
import aiohttp
from discord.ext import commands
from database import log_verification, is_banned
from errors import handle_api_error

# Security configuration (Toggleable)
SECURITY_CONFIG = {
    "ban_alts": True,
    "ban_vpns": True,
    "detect_bots": True
}

class VerificationModal(discord.ui.Modal, title='Security Verification'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.ip_field = discord.ui.TextInput(
            label='Confirm IP for Proxy Check', 
            style=discord.TextStyle.short,
            placeholder="Enter IP address here..."
        )
        self.add_item(self.ip_field)

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        ip = self.ip_field.value
        
        # 1. Database Check: Global Ban
        if is_banned(user.id, ip):
            await interaction.response.send_message("Access Denied: User/IP flagged.", ephemeral=True)
            return

        # 2. Bot/Suspicious Detection
        if SECURITY_CONFIG["detect_bots"]:
            is_suspicious = user.bot or (user.avatar is None and (datetime.datetime.utcnow() - user.created_at).days < 1)
            if is_suspicious:
                await interaction.response.send_message("Verification failed: Account flagged as suspicious.", ephemeral=True)
                return

        # 3. Alt Detection (7 days)
        if SECURITY_CONFIG["ban_alts"]:
            if (datetime.datetime.utcnow() - user.created_at).days < 7:
                await self.ban_user_globally(user, "Alt account detected (<7 days)")
                log_verification(ip, user.id, "BANNED_ALT")
                await interaction.response.send_message("Verification failed: Account too young.", ephemeral=True)
                return

        # 4. VPN/Proxy Detection
        if SECURITY_CONFIG["ban_vpns"]:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://v2.api.iphub.info/ip/{ip}") as resp:
                        data = await resp.json()
                        if data.get('block', 0) == 1:
                            await self.ban_user_globally(user, "VPN/Proxy detected")
                            log_verification(ip, user.id, "BANNED_VPN")
                            await interaction.response.send_message("Verification failed: VPN/Proxy usage prohibited.", ephemeral=True)
                            return
            except Exception as e:
                await handle_api_error(interaction, e)
                return

        log_verification(ip, user.id, "SUCCESS")
        await interaction.response.send_message("Verification successful. Welcome!", ephemeral=True)

    async def ban_user_globally(self, user: discord.User, reason: str):
        for guild in self.bot.guilds:
            try:
                member = await guild.fetch_member(user.id)
                await guild.ban(member, reason=reason)
            except (discord.NotFound, discord.Forbidden):
                continue

class VerificationView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Verify Identity', style=discord.ButtonStyle.primary, custom_id='verify_btn')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerificationModal(self.bot))

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_verification(self, ctx: commands.Context):
        view = VerificationView(self.bot)
        await ctx.send("Click below to start security verification:", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Verification(bot))