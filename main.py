import discord
from discord.ext import commands
import os
import json
import asyncio

# 1. Setup minimal intents
intents = discord.Intents.default()

# 2. Setup the bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # 3. Load the server ID from your config
    with open('private_config.json', 'r') as f:
        config = json.load(f)
        guild_id = config['ALLOWED_GUILD_IDS'][0]
    
    # 4. Sync the commands to the specific server
    target_guild = discord.Object(id=guild_id)
    bot.tree.copy_global_to(guild=target_guild)
    await bot.tree.sync(guild=target_guild)
    print(f"Synced commands to {guild_id}")

async def load_extensions():
    # Looks for .py files in a 'cogs' folder
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())