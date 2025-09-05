import discord
import datetime
from discord.ext import commands, tasks
import requests
import os
import random
import asyncio
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import json

#CONFIG FILE AND ITS FUNCTION
#####################################################
CONFIG_FILE = "config.json"

def save_config(playlist_url, channel_id):
    data = {
        "playlist_url": playlist_url,
        "discord_text_channel": channel_id
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None, None
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data.get("playlist_url"), data.get("discord_text_channel")
    
playlist_url, discord_text_channel = load_config()
#####################################################


def createInteraction(ctx:commands.Context,member:discord.Member,title: str, description: str, color: discord.Color, urls: list[str], footerText:str,):
    imageID = random.randint(0,len(urls)-1)
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_image(url=urls[imageID])
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=footerText, icon_url=ctx.author.avatar.url)

    return embed



load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

intents = discord.Intents.default()
intents.message_content = True        
intents.members = True                 
intents.guilds = True                  
intents.reactions = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await daily_song()

#INTERACTION COMMANDS
#####################################################
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
async def hug(ctx:commands.Context, member: discord.Member):
    urls = ["https://i.pinimg.com/originals/6d/b5/4c/6db54c4d6dad5f1f2863d878cfb2d8df.gif"]
    embed = createInteraction(ctx,member,"Warm Hugs!",f"{ctx.author.mention} gives a warm hug to {member.mention}<3",discord.Color.pink(),urls,f"Hugged by {ctx.author.display_name}")

    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx:commands.Context, member: discord.Member):
    urls = ["https://i.pinimg.com/originals/10/5a/7a/105a7ad7edbe74e5ca834348025cc650.gif"]
    embed = createInteraction(ctx,member,"Someone got kissed!",f"{member.mention} gets a tons of love!",discord.Color.yellow(),urls,f"Kissed by {ctx.author.display_name}")

    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx:commands.Context, member: discord.Member):
    urls = ["https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG5iOTdlemtrM2NwOHJvd3RscTBnZjgzNmVuM2pkYWQ3cTBlN3lvYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11HeubLHnQJSAU/giphy.gif"]
    embed = createInteraction(ctx,member, title="Someone got killed!", description=f"{member.mention} cannot breath anymore!",color=discord.Color.red(),urls=urls, footerText=f"Killed by {member.display_name}")

    await ctx.send(embed=embed)

@bot.command()
async def slap(ctx:commands.Context, member: discord.Member):
    urls =["https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2M4Nng5bzQ5NTRxZjJ5dmZreTd1ZTZpbmxncG12cHl1anVzc2kxZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Gf3AUz3eBNbTW/giphy.gif"]
    embed = createInteraction(ctx, member, "Slapped!", f"{member.mention} got slapped",discord.Color.dark_gold(),urls,f"Slapped by {ctx.author.display_name}")

    await ctx.send(embed=embed)

@bot.command()
async def marry(ctx:commands.Context, member: discord.Member):
    urls = ["https://i.pinimg.com/originals/01/91/f9/0191f989bab551e76a452b5c2fdf8c34.gif"]
    embed = createInteraction(ctx, member,"Ohh, it's getting serious!", f"{member.mention} do you accept it?",discord.Color.blurple(),urls,f"{ctx.author.display_name} proposes you something special")

    message = await ctx.send(embed=embed)

    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reaction:discord.Reaction, user:discord.Member):
        return (user.id == member.id and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id)
    
    try:
        reactionUser: tuple[discord.Reaction, discord.User]= await bot.wait_for("reaction_add",timeout=60.0, check=check)
        reaction, user = reactionUser

        if str(reaction.emoji) == "✅":
            await ctx.send(f"Congratulation! {member.mention} accepted your proposal!")
        else:
            await ctx.send(f"I'm sorry... {member.mention} don't accepted your proposal :c")
    except asyncio.TimeoutError:
         await ctx.send(f"{member.mention} didn't respond in time.")
#####################################################

#ADMINISTRATION COMMANDS
#####################################################
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

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx:commands.Context, user:discord.Member, *, role:str):
    targetRole = discord.utils.get(ctx.guild.roles, name=role)

    if not targetRole:
        await ctx.send(f"There is no {role} role.")
        return
    if targetRole not in user.roles:
        await ctx.send(f"{user.name} does not have {targetRole} role.")
        return

    try:
        await user.remove_roles(targetRole)
        await ctx.send(f"{targetRole} role has been removed.")
    except discord.Forbidden:
        await ctx.send("I don't have permissions to remove this role.")
    except discord. HTTPException:
        await ctx.send("Something went wrong while removing this role.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx:commands.Context, user:discord.Member):
    if user is None:
        await ctx.send(f"This member do not exist.")
        return

    try:
        await user.ban()
        await ctx.send(f"{user.mention} has been banned")
    except discord.Forbidden:
        await ctx.send("I don't have permissions to ban this user.")
    except discord.HTTPException:
        await ctx.send("Something went wrong...")
    
@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx: commands.Context, user: str):
    bannedUsers = []

    async for banEntry in ctx.guild.bans():
        bannedUsers.append(banEntry)


    for banEntry in bannedUsers:
        bannedUser = banEntry.user

        if bannedUser.name == user:
            await ctx.guild.unban(bannedUser)
            await ctx.send(f"{user} has been unbanned.")
            return
    
    await ctx.send(f"There isn't {user} in banned members.")
#####################################################

@bot.command()
async def set_daily_playlist(ctx: commands.Context, link: str):
    global playlist_url

    if link is None:
        await ctx.send("Please select your playlist!")
        return
    
    playlist_url = link
    save_config(playlist_url, discord_text_channel)
    await ctx.send(f"Playlist link is set to {playlist_url}")

@bot.command()
async def set_daily_playlist_channel(ctx: commands.Context, channel_name):
    global discord_text_channel

    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            discord_text_channel = channel.id
            save_config(playlist_url, discord_text_channel)
            break
    
    
@tasks.loop(hours=24)
async def daily_song():
    global playlist_url, discord_text_channel

    if not playlist_url or not discord_text_channel:
        print("there no playlist or channel")
        return
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
    }

    songs = []

    try:

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' not in info:
                print("not a playlist")
                return

            for entry in info['entries']:
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                songs.append(video_url)

        song_url = random.choice(songs)
        song_id = song_url.split("v=")[-1].split("&")[0] if "v=" in song_url else song_url.split("/")[-1]

        def get_title(url):
            try:
                response = requests.get(url)
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
                return soup.title.string.strip()
            except Exception as e:
                print(f"Error fetching title: {e}")
                return("Song of the day!")
            
        title = get_title(song_url)

        embed = discord.Embed(title="Song of the day!",description=f"**{title}**\n[Watch on YouTube]({song_url})", color=discord.Color.blue(),url=song_url)
        embed.set_image(url=f"https://img.youtube.com/vi/{song_id}/maxresdefault.jpg")
        embed.set_footer(text="Your daily dose of music!")

        channel = bot.get_channel(discord_text_channel)
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Error in daily song function")

bot.run(DISCORD_TOKEN)

