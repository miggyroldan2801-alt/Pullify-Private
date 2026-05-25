import discord
from discord import app_commands
from discord.ext import commands
import json
import logging
from database import DBManager # Assuming DBManager methods: create_ticket, update_ticket

logger = logging.getLogger("pullify.tickets")

with open("private_config.json", "r") as f:
    ALLOWED_GUILDS = json.load(f)["ALLOWED_GUILD_IDS"]

class TicketModal(discord.ui.Modal, title='Support Ticket Request'):
    reason = discord.ui.TextInput(
        label='Reason for contact',
        style=discord.TextStyle.paragraph,
        placeholder='Describe your issue clearly...',
        required=True,
        min_length=10,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.guild.id not in ALLOWED_GUILDS:
            return

        # Create thread
        thread = await interaction.channel.create_thread(
            name=f"ticket-{interaction.user.name}",
            type=discord.ChannelType.private_thread
        )
        
        # Database Integration
        ticket_id = await DBManager.create_ticket(interaction.user.id, thread.id, self.reason.value)
        
        await thread.send(f"**Ticket ID:** {ticket_id}\n**Opened by:** {interaction.user.mention}\n**Reason:** {self.reason.value}", 
                          view=TicketManagementView())
        await interaction.response.send_message(f"Ticket created: {thread.mention}", ephemeral=True)

class TicketManagementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary, custom_id="ticket_claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Ticket claimed by {interaction.user.mention}", ephemeral=True)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await DBManager.update_ticket_status(interaction.channel_id, "closed")
        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Support Ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.id not in ALLOWED_GUILDS:
            await interaction.response.send_message("Unauthorized server.", ephemeral=True)
            return
        await interaction.response.send_modal(TicketModal())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketView())
        self.bot.add_view(TicketManagementView())
        logger.info("Ticket views synchronized.")

    @app_commands.command(name="setup-tickets", description="Initialize ticket system")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        if interaction.guild.id not in ALLOWED_GUILDS:
            return
        await interaction.response.send_message("Ticket System Initialized.", view=TicketView())

async def setup(bot):
    await bot.add_cog(Tickets(bot))