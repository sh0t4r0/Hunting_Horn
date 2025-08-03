import os
import threading
import datetime
import requests
import discord
from discord.ext import commands, tasks
from flask import Flask

# Environment variables (set in Render dashboard)
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
APP_ID = os.getenv("APP_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Setup bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Minimal Flask web server to keep Render Web Service alive
app = Flask(__name__)

@app.route('/')
def index():
    return "🤖 Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Start web server in background thread
threading.Thread(target=run_web_server).start()

# Run auto-ping every 15 days
@tasks.loop(hours=360)  # adjust to smaller value for testing if needed
async def auto_ping():
    print("⚡ Auto-ping triggered...")
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

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    if not auto_ping.is_running():
        auto_ping.start()

# Slash command
@bot.slash_command(name="ping", description="Replies with Pong!", guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.respond("🏓 Pong!")

# Start bot
bot.run(TOKEN)
