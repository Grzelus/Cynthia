# Cynthia - Interaction bot

> Lightweight Discord interaction bot written in Python (discord.py). Provides fun interaction commands, simple admin utilities and a configurable daily YouTube playlist post.

---

# Invitation Link

https://discord.com/oauth2/authorize?client_id=1412082281736310815&permissions=8&integration_type=0&scope=bot

---

## Table of contents
- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands & Functions](#commands--functions)
  - [Interaction commands (user-facing)](#interaction-commands-user-facing)
  - [Administration commands](#administration-commands)
  - [Playlist configuration commands](#playlist-configuration-commands)
  - [Helper / internal functions & background tasks](#helper--internal-functions--background-tasks)
- [File structure (outline)](#file-structure-outline)
- [Known issues / notes](#known-issues--notes)
- [Contributing](#contributing)

---

## Description
Cynthia is an "interaction" Discord bot offering a set of fun commands (hug, kiss, slap, marry, etc.), a few administration utilities (role management, ban/unban) and a scheduled background task that posts a daily "Song of the day" from a YouTube playlist into a configured channel.

It is implemented with `discord.py` (commands extension) and uses `yt_dlp` to parse YouTube playlist contents and `BeautifulSoup`/`requests` to fetch the video page title for nicer embeds.

---

## Features
- Fun user-to-user interactions with embeds and GIFs.
- Simple marriage flow using reactions (✅/❌) and 60s timeout.
- Admin role management: add/remove roles, ban/unban.
- Per-server configuration stored in a JSON file (`config.json`) for: playlist URL, target channel, and hour to post.
- Background `@tasks.loop` that checks every minute and posts one random video from the configured playlist at the configured hour.

---

## Prerequisites
- Python 3.10+ recommended
- A Discord bot token with message and member intents enabled
- A `.env` file containing at least `DISCORD_TOKEN` (and optionally `RIOT_API_KEY` if you plan to use Riot endpoints later)

Python dependencies (install with `pip`):
- discord.py (or `py-cord` / supported fork matching `discord` import)
- python-dotenv
- requests
- beautifulsoup4
- yt_dlp

---

## Configuration
- `CONFIG_FILE` — `config.json` (per-guild configuration): stores `playlist_url`, `channel_id`, `post_time`.
- Environment variables in `.env`: `DISCORD_TOKEN`
- Intents: `message_content`, `members`, `guilds`, `reactions` are enabled in the code and your bot application must enable any privileged intents used.

**Important**: `post_time` currently is expected to be an hour (0–23). See *Known issues* for a note about type handling.

---

## Usage
Start the bot with python. The bot automatically triggers `daily_song()` on ready and runs a minute loop (`@tasks.loop(minutes=1)`) that will post at each guild's configured hour.

Interactive commands use a prefix of `$` (configured when creating `Bot(command_prefix="$")`). Example: `$hug @member`.

---

## Commands & Functions

### Interaction commands (user-facing)
These commands are intended for normal users (no admin permission required unless specified):

- `$hello`
  - Sends a random greeting GIF and mentions another user if one is mentioned.

- `$hug @member`
  - Sends an embed with a hug GIF. Uses `createInteraction` helper to construct the embed.

- `$kiss @member`
  - Sends an embed with a kiss GIF.

- `$kill @member`
  - Sends a dramatic (joke) kill GIF embed.

- `$slap @member`
  - Sends a slap GIF embed.

- `$marry @member`
  - Sends a proposal embed, adds reactions ✅ and ❌, waits up to 60 seconds for target user's response. If ✅ → announces acceptance, if ❌ → announces rejection, on timeout informs the channel.


### Administration commands
Require elevated permissions as noted below.

- `$addrole <member> <role name>`
  - Required permission: `manage_roles` (bot also needs ability to manage roles).
  - Adds an existing role (by name) to the requested member.

- `$removerole <member> <role name>`
  - Required permission: `manage_roles`.
  - Removes the given role from the requested member.

- `$ban <member>`
  - Required permission: `administrator`.
  - Bans the supplied member. Note: this is a simple wrapper and does not accept reason or deletion days.

- `$unban <username>`
  - Required permission: `administrator`.
  - Unbans a user by username (exact match on `user.name`).


### Playlist configuration commands
- `$set_daily_playlist <playlist_url>`
  - Set the YouTube playlist URL to draw the daily song from.

- `$set_daily_playlist_channel <channel_name>`
  - Set which channel (by name) the bot will post the daily song into. The command searches `ctx.guild.channels` for a channel with the provided name and stores its `.id`.

- `$set_daily_playlist_post_time <hour>`
  - Set the hour (0–23) when the daily song should be posted. The command currently accepts a string and calls `save_config(..., post_time=hour)` — see Known Issues.


### Helper / internal functions & background tasks
These functions are defined in the source and used by the bot logic.

- `save_config(guild: discord.Guild, playlist_url=None, channel_id=None, post_time=None)`
  - Writes/updates `config.json` for the given guild. Creates the JSON file when missing.
  - Parameters are optional; only provided values update the stored config.

- `load_config(guild)`
  - Reads `config.json` and returns the stored configuration for the guild or defaults: `{ "playlist_url": None, "channel_id": None, "post_time": 12 }`.

- `on_guild_join(guild: discord.Guild)`
  - Ensures `config.json` has an entry for newly-joined guilds (called when the bot joins a server).

- `createInteraction(ctx: commands.Context, member: discord.Member, title: str, description: str, color: discord.Color, urls: list[str], footerText: str)`
  - Helper that builds a `discord.Embed` using a random image from `urls`, author's avatar as footer, and the target member's avatar as a thumbnail.

- `on_ready()`
  - Prints the bot user and starts `daily_song()` on ready.

- `daily_song()` — `@tasks.loop(minutes=1)`
  - Main background loop. Every minute it:
    1. Loads each guild's config and checks `post_time` against current hour.
    2. If it matches, uses `yt_dlp` with `extract_flat` to fetch playlist entries (no downloads) and chooses a random song.
    3. Builds an embed with the YouTube thumbnail and a title grabbed by `get_title(url)` (requests + BeautifulSoup).
    4. Sends embed to configured channel id.
  - Notes: If playlist or channel missing it logs/prints and continues.

- `get_title(url)` (inner helper used inside daily_song)
  - Uses `requests` + `BeautifulSoup` to fetch the HTML page and extract the `<title>` tag. If fetching fails, falls back to a default string `"Song of the day!"`.

---

## File structure (outline)
```
/ (repo root)
├─ bot.py (or main python file containing the code you provided)
├─ config.json (auto-generated)
├─ .env
├─ README.md
```

---

## Known issues / notes
- **post_time type**: `set_daily_playlist_post_time` calls `save_config(..., post_time=hour)` with `hour` as the incoming string. The `daily_song` task compares `post_time != current_hour` where `current_hour` is an `int`. If `post_time` is stored as a string that will never equal the integer hour. Recommend casting/normalizing the stored `post_time` to `int` (and validating range) inside `set_daily_playlist_post_time` and `save_config`/`load_config`.

- `unban` uses `user.name` exact match to identify a banned user. That may be ambiguous when multiple users share the same display name — consider using `name#discriminator` or user id.

- `on_ready()` calls `await daily_song()` and `daily_song` is also a `@tasks.loop`. Ideally call `daily_song.start()` from `on_ready()` instead of awaiting it directly.

- Playlist parsing uses `yt_dlp` `extract_flat`. For some playlist types this may not return `entries` or may require additional options.

---

## Contributing
Contributions are welcome — open an issue or create a PR. Please follow code style and include tests for non-trivial logic.

---



