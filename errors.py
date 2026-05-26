import discord

async def handle_api_error(interaction: discord.Interaction, error: Exception):
    """
    Handles API exceptions globally. 
    Logs the error to the console and informs the user via an ephemeral embed.
    """
    print(f"API Error detected: {error}")
    
    embed = discord.Embed(
        title="⚠️ Service Error",
        description="A temporary issue occurred while communicating with the security service. Please try again in a few moments.",
        color=discord.Color.red()
    )
    
    # Check if the interaction has already been responded to
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)