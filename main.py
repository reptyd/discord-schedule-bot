"""
Discord Schedule Bot
--------------------

This bot allows users to schedule events via a simple text command.  Events are
stored in an SQLite database and a background task periodically checks for
upcoming events, sending reminders at the exact time.  After a reminder is sent,
the event is automatically removed.  The implementation uses the
`discord.ext.tasks` extension to manage the periodic check.

Commands:

* `!schedule YYYY-MM-DD HH:MM Description` – create a new event.

Feel free to extend the bot with commands such as `!events` to list events or
`!cancel` to remove one.  See README.md for installation instructions.
"""

import asyncio
import os
from datetime import datetime, timezone
from typing import Optional

import aiosqlite
import discord
from discord.ext import commands, tasks

# Database file
DB_FILE = "events.db"

# Command prefix
COMMAND_PREFIX = "!"

# Optionally adjust the time zone (UTC by default)
TZ = timezone.utc

# Prepare the bot
intents = discord.Intents.default()
# We need message content intent to read commands
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


async def init_db() -> None:
    """Create the events table if it does not already exist."""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                event_time TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
        )
        await db.commit()


@bot.event
async def on_ready() -> None:
    """Called when the bot has connected to Discord."""
    await init_db()
    check_events.start()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.command(name="schedule")
async def schedule_event(ctx: commands.Context, date: str, time: str, *, description: str) -> None:
    """Schedule a new event.

    Usage: !schedule YYYY-MM-DD HH:MM Description of the event
    """
    # Combine date and time and parse into a datetime object (assume UTC)
    try:
        dt_str = f"{date} {time}"
        dt = datetime.fromisoformat(dt_str)
        # Attach timezone info; assume naive times are given in the configured TZ
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ)
    except ValueError:
        await ctx.send("❌ Invalid date or time format. Use YYYY-MM-DD HH:MM")
        return

    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT INTO events (guild_id, channel_id, event_time, description) VALUES (?, ?, ?, ?)",
            (ctx.guild.id, ctx.channel.id, dt.isoformat(), description),
        )
        await db.commit()

    msg = await ctx.send(f"✅ Scheduled '{description}' for {dt.isoformat()}.")
    # Add a calendar emoji reaction to indicate success
    try:
        await msg.add_reaction("📅")
    except discord.HTTPException:
        pass


@tasks.loop(seconds=60)
async def check_events() -> None:
    """Background task that checks for due events every minute."""
    now = datetime.now(tz=TZ)
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT id, guild_id, channel_id, event_time, description FROM events") as cursor:
            rows = await cursor.fetchall()
        for event_id, guild_id, channel_id, event_time, description in rows:
            try:
                event_dt = datetime.fromisoformat(event_time)
                if event_dt.tzinfo is None:
                    event_dt = event_dt.replace(tzinfo=TZ)
            except ValueError:
                # Malformed date; skip
                continue
            # If the event time has passed or is now, send a reminder
            if now >= event_dt:
                channel = bot.get_channel(channel_id)
                if channel is not None:
                    try:
                        await channel.send(f"🔔 Reminder: '{description}' is happening now!")
                    except discord.HTTPException:
                        pass
                # Delete the event from the database
                await db.execute("DELETE FROM events WHERE id = ?", (event_id,))
                await db.commit()


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable is required")
    bot.run(token)
