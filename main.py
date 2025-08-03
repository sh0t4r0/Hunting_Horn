import os
import discord
from discord.ext import commands, tasks
from discord import option
import requests
import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
APP_ID = os.getenv("APP_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Where to run slash command

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")
    if not auto_ping.is_running():
        auto_ping.start()

@bot.slash_command(name="ping", description="Replies with Pong!", guild_ids=[int(GUILD_ID)])
async def ping(ctx):
    await ctx.respond("🏓 Pong!")

@tasks.loop(hours=360)  # Every 15 days (approx)
async def auto_ping():
    url = "https://discord.com/api/v10/interactions"
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
    response = requests.post(url, headers=headers, json=payload)
    print(f"[{datetime.datetime.now()}] Auto ping: {response.status_code} - {response.text}")

bot.run(TOKEN)
