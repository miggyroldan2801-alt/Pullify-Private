import discord
import os
import asyncio
from discord.ext import commands

# Basic configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    # Only loads valid Cog files
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != 'errors.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start('YOUR_BOT_TOKEN_HERE')

if __name__ == '__main__':
    asyncio.run(main())