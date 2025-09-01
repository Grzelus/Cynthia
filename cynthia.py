import discord
from discord.ext import commands, tasks
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

