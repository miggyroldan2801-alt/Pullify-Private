import discord
from discord.ext import commands
import os
import json

# Use minimal intents to avoid 'PrivilegedIntentsRequired' error
# This does not require toggling switches in the Developer Portal
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    # Load your config
    # Ensure private_config.json exists with {"ALLOWED_GUILD_IDS": [1508388382948982898]}
    with open('private_config.json', 'r') as f:
        config = json.load(f)
        
    # Start the bot
    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())