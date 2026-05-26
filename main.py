import os
import discord
import json
from discord.ext import commands

# 1. Try to get token from Environment Variable, otherwise load from file
token = os.getenv('DISCORD_TOKEN')

if not token:
    try:
        with open('private_config.json', 'r') as f:
            config = json.load(f)
            token = config.get('token')
    except FileNotFoundError:
        print("Error: No token found in environment or config file.")
        exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    # Only load files from cogs folder
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())