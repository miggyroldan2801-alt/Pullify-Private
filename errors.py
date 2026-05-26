import discord

async def handle_api_error(interaction: discord.Interaction, error: Exception):
    print(f"API Error: {error}")
    embed = discord.Embed(
        title="Error",
        description="A service error occurred. Please try again later.",
        color=discord.Color.red()
    )
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)