import os
import threading
import datetime
import requests
import discord
from discord.ext import commands, tasks
from flask import Flask

# Environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
APP_ID = os.getenv("APP_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Minimal Flask web server
app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>kaneda</title>
  <style>
    body {
      background-color: #000;
      color: #0f0;
      font-family: "Courier New", Courier, monospace;
      padding: 40px;
      white-space: pre;
    }
  </style>
</head>
<body>
{made_by}

{pill_art}
</body>
</html>
'''.replace('{made_by}', r'''
 __  __     ______     __   __     ______     _____     ______    
/\ \/ /    /\  __ \   /\ "-.\ \   /\  ___\   /\  __-.  /\  __ \   
\ \  _"-.  \ \  __ \  \ \ \-.  \  \ \  __\   \ \ \/\ \ \ \  __ \  
 \ \_\ \_\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \ \____-  \ \_\ \_\ 
  \/_/\/_/   \/_/\/_/   \/_/ \/_/   \/_____/   \/____/   \/_/\/_/ 

             made by : kaneda
''').replace('{pill_art}', r'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠶⠛⠛⠛⠶⣤⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠟⠋⢁⣠⣴⣶⣶⣶⣬⣿⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠟⠉⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⠋⠁⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
⠀⠀⠀⠀⢀⣴⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
⠀⠀⢀⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀
⠀⢀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⠿⢿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀
⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡾⠛⢉⣠⣴⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢿⡄⠐⢦⣤⣤⣴⣾⠿⠛⣁⣤⡾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠻⢦⣄⣀⠉⣉⣀⣴⠾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
''')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server).start()

@tasks.loop(hours=360)
async def auto_ping():
    print("well...")
    print('''
"I’ve seen things… seen things you little people wouldn’t believe.
Attack ships on fire off the shoulder of Orion bright as magnesium…
I rode on the back decks of a blinker and watched C-beams glitter in the dark near the Tannhäuser Gate.
All those moments… they’ll be gone."
    ''')

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
    print(f"[{datetime.datetime.now()}] Auto-ping response: {response.status_code} {response.text}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not auto_ping.is_running():
        auto_ping.start()

@bot.slash_command(name="ping", description="Test the bot's identity", guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.respond("Is this a Voigt-Kampff test?")

bot.run(TOKEN)
