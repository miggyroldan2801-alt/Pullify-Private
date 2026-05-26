import os
import sys
import discord
from discord.ext import commands

# 1. Debugging: This prints to the Runtime logs so you know if it even starts
print("DEBUG: Application starting...")

# 2. Token Handling
# Ensure your environment variable matches the one set in your dashboard
TOKEN = os.getenv("DISCORD_TOKEN") 

if not TOKEN:
    print("CRITICAL: DISCORD_TOKEN is not set in the environment variables.")
    sys.exit(1) # Exit with error code to prevent 'Completed' status on success

# 3. Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot successfully logged in as {bot.user}")

# 4. Blocking Execution
if __name__ == "__main__":
    try:
        # bot.run() is the correct, blocking way to start a discord.py bot
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("CRITICAL: Invalid token. Please check your Discord Developer Portal.")
        sys.exit(1)
    except Exception as e:
        print(f"CRITICAL: Bot crashed: {e}")
        sys.exit(1)