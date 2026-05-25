import discord
import logging
import os
import json
import asyncio
from discord.ext import commands
from database import DBManager

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pullify.main")

# Load Config
with open("private_config.json", "r") as f:
    config = json.load(f)

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    extensions = ['cogs.tickets', 'cogs.verification', 'cogs.support', 'cogs.utilities', 'cogs.errors']
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"Loaded {ext}")
        except Exception as e:
            logger.error(f"Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    # Initialize Database on Startup
    await DBManager.initialize()
    logger.info(f"PULLIFY-PRIVATE Online as {bot.user}")
    
    # Sync tree for each allowed guild
    for guild_id in config["ALLOWED_GUILD_IDS"]:
        try:
            await bot.tree.sync(guild=discord.Object(id=guild_id))
            logger.info(f"Synced commands to {guild_id}")
        except Exception as e:
            logger.error(f"Sync failed for {guild_id}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())