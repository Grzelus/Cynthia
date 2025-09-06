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

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

intents = discord.Intents.default()
intents.message_content = True        
intents.members = True                 
intents.guilds = True                  
intents.reactions = True
bot = commands.Bot(command_prefix="$", intents=intents)

#CONFIG FILE AND ITS FUNCTION
#####################################################
CONFIG_FILE = "config.json"

def save_config(guild:discord.Guild, playlist_url=None, channel_id= None, post_time = None):
    guild_id = guild.id
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            servers_config = json.load(f)
    else:
        servers_config = {}


    guild_id = str(guild_id)
    if guild_id not in servers_config:
        servers_config[guild_id]= {}
        

    if playlist_url is not None:
        servers_config[guild_id]["playlist_url"] = playlist_url
    if channel_id is not None:
        servers_config[guild_id]["channel_id"] = channel_id
    if post_time is not None:
        servers_config[guild_id]["post_time"] = post_time
    with open(CONFIG_FILE, "w") as f:
        json.dump(servers_config,f,indent=4)


    
def load_config(guild):
    guild_id = str(guild.id)

    if not os.path.exists(CONFIG_FILE):
        return {"playlist_url": None, "channel_id": None}

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    return data.get(guild_id, {"playlist_url": None, "channel_id": None})

@bot.event
async def on_guild_join(guild: discord.Guild):
    guild_id = guild.id
    try:
        with open(CONFIG_FILE, "r") as f:
            server_config = json.load(f)
    except FileNotFoundError:
            server_config = {}

    if guild_id not in server_config:
        server_config[guild_id] = {
            "playlist_url": None,
            "channel_id": None,
            "post_time": 12
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(server_config, f, indent=4)
#####################################################


def createInteraction(ctx:commands.Context,member:discord.Member,title: str, description: str, color: discord.Color, urls: list[str], footerText:str,):
    imageID = random.randint(0,len(urls)-1)
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_image(url=urls[imageID])
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=footerText, icon_url=ctx.author.avatar.url)

    return embed


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
    if not link:
        await ctx.send("Please select your playlist!")
        return

    config = load_config(ctx.guild)
    config["playlist_url"] = link

    save_config(ctx.guild, config["playlist_url"], config["channel_id"])
    await ctx.send(f"Playlist link is set to: {link}")


@bot.command()
async def set_daily_playlist_channel(ctx: commands.Context, channel_name: str):
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            config = load_config(ctx.guild)
            config["channel_id"] = channel.id

            save_config(ctx.guild, config["playlist_url"], config["channel_id"])
            await ctx.send(f"Channel set to: {channel.name}")
            return

    await ctx.send("Channel not found.")

    
    
@tasks.loop(hours=24)
async def daily_song():
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
    }

    for guild in bot.guilds:
        config = load_config(guild)
        playlist_url = config.get("playlist_url")
        channel_id = config.get("channel_id")

        if not playlist_url or not channel_id:
            print(f"No playlist or channel set for guild: {guild.name}")
            continue

        songs = []

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                if 'entries' not in info:
                    print(f"Not a playlist for guild: {guild.name}")
                    continue

                for entry in info['entries']:
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    songs.append(video_url)

            if not songs:
                print(f"No songs found in playlist for guild: {guild.name}")
                continue

            song_url = random.choice(songs)
            song_id = song_url.split("v=")[-1].split("&")[0] if "v=" in song_url else song_url.split("/")[-1]

            def get_title(url):
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    return soup.title.string.strip()
                except Exception as e:
                    print(f"Error fetching title: {e}")
                    return "Song of the day!"

            title = get_title(song_url)

            embed = discord.Embed(
                title="Song of the day!",
                description=f"**{title}**\n[Watch on YouTube]({song_url})",
                color=discord.Color.blue(),
                url=song_url
            )
            embed.set_image(url=f"https://img.youtube.com/vi/{song_id}/maxresdefault.jpg")
            embed.set_footer(text="Your daily dose of music!")

            channel = guild.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed)
            else:
                print(f"Channel ID {channel_id} not found in guild: {guild.name}")

        except Exception as e:
            print(f"Error in daily song function for guild {guild.name}: {e}")


bot.run(DISCORD_TOKEN)

