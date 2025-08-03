import os
import discord
from discord.ext import commands, tasks
import requests
import datetime

# Environment variables from Render dashboard
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
APP_ID = os.getenv("APP_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    if not auto_ping.is_running():
        auto_ping.start()

# Slash command definition
@bot.slash_command(name="ping", description="Replies with Pong!", guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.respond("🏓 Pong!")

# Auto self-ping every 15 days
@tasks.loop(hours=360)
async def auto_ping():
    print("⚡ Auto-ping running...")
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": 2,
        "application_id": APP_ID,
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "data": {
            "name": "ping",
            "type": 1
        }
    }
    response = requests.post("https://discord.com/api/v10/interactions", headers=headers, json=payload)
    print(f"[{datetime.datetime.now()}] Auto-ping: {response.status_code} {response.text}")

# Start the bot
bot.run(TOKEN)
