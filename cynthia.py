import discord
from discord.ext import commands, tasks
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

intents = discord.Intents.default()
intents.message_content=True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx: commands.Context):
    urls = ["https://i.pinimg.com/originals/35/35/00/3535009c4a5e1d6c611dc436183b2be3.gif", "https://i.pinimg.com/originals/b5/99/6b/b5996befa70fc2fdf1379877f4488fec.gif", "https://i.pinimg.com/originals/97/24/d6/9724d6d1ae0f4e5018edc1a61fecafdc.gif"]
    picID = random.randint(0,len(urls)-1)
    embedGif = discord.Embed().set_image(url=urls[picID])
    if ctx.message.mentions:
        await ctx.send(f"{ctx.author.mention} greets {ctx.message.mentions[0].mention}", embed=embedGif)
    else:
        await ctx.send(f"{ctx.author.mention} sends greetings!", embed=embedGif)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx: commands.Context, user: discord.Member, *, roleName: str):
    role = discord.utils.get(ctx.guild.roles, name=roleName)

    if role is None:
        await ctx.send(f"Role '{roleName}' is not found.")
        return
    
    try:
        await user.add_roles(role)
        await ctx.send(f"{role} role has been given to {user.mention}")
    except discord.Forbidden:
        await ctx.send(f"I don't have permision to add {role} role.")
    except discord.HTTPException:
        await ctx.send(f"Something went wrong while assigning the {role} role.")

bot.run(DISCORD_TOKEN)

