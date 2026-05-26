import os
import discord
import json
from discord.ext import commands

# Load configuration
with open('private_config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['token'])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())