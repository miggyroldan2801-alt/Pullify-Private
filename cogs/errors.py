import discord

async def handle_api_error(interaction: discord.Interaction, error: Exception):
    """Handles API failures gracefully."""
    print(f"API Error: {error}")
    embed = discord.Embed(
        title="Error",
        description="A service error occurred. Please try again later.",
        color=discord.Color.red()
    )
    await interaction.followup.send(embed=embed, ephemeral=True)