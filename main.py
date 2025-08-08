import os
import threading
import datetime
import discord
from discord.ext import commands
from flask import Flask, request, abort, Response

# Environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
APP_ID = os.getenv("APP_ID")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ensure this is an int
TRIGGER_TOKEN = os.getenv("TRIGGER_TOKEN")  # set this in Render

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Will hold the ping command mention like </ping:1234>
PING_MENTION = "/ping"

# ---------- Minimal Flask web server ----------
app = Flask(__name__)

@app.route("/")
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

@app.get("/remind")
def remind():
    # protected endpoint the cron hits
    token = request.args.get("token", "")
    if not TRIGGER_TOKEN or token != TRIGGER_TOKEN:
        abort(403)

    # Compose reminder with command mention
    blade = (
        "I’ve seen things… seen things you little people wouldn’t believe.\n"
        "Attack ships on fire off the shoulder of Orion bright as magnesium…\n"
        "I rode on the back decks of a blinker and watched C-beams glitter in the dark near the Tannhäuser Gate.\n"
        "All those moments… they’ll be gone."
    )
    content = f"{blade}\n\nClick to run {PING_MENTION}"

    # Send into the configured channel
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        # try fetching if not cached yet
        channel = bot.get_guild(GUILD_ID).get_channel(CHANNEL_ID)

    async def _send():
        try:
            await channel.send(content)
        except Exception as e:
            print(f"remind send error: {e}")

    # Schedule the coroutine on the bot loop
    bot.loop.create_task(_send())

    body = f"reminder queued at {datetime.datetime.utcnow().isoformat()}Z\n"
    return Response(body, mimetype="text/plain")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    # threaded Flask server so bot loop continues
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", port, app, use_reloader=False, threaded=True)

threading.Thread(target=run_web_server, daemon=True).start()

# ---------- Discord bits ----------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Resolve the command mention once (gives </ping:ID>)
    try:
        # py-cord stores app commands here after ready
        cmds = await bot.http.get_global_commands(bot.user.id)
        # try guild override first (if you registered it for guild)
        if GUILD_ID:
            try:
                gcmds = await bot.http.get_guild_commands(bot.user.id, GUILD_ID)
                cmds = gcmds or cmds
            except Exception:
                pass

        ping_cmd_id = None
        for c in cmds:
            if c.get("name") == "ping":
                ping_cmd_id = c.get("id")
                break
        global PING_MENTION
        if ping_cmd_id:
            PING_MENTION = f"</ping:{ping_cmd_id}>"
            print(f"Resolved ping mention: {PING_MENTION}")
        else:
            print("Could not resolve ping command ID; using literal /ping")
    except Exception as e:
        print(f"Error resolving command mention: {e}")

@bot.slash_command(name="ping", description="Test the bot's identity", guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.respond("Is this a Voigt-Kampff test?")

bot.run(TOKEN)
