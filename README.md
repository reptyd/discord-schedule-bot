# Discord Schedule Bot

This project provides a Discord bot for scheduling events with automatic reminders and clean-up of old entries. Users invoke a command to create an event (date, time and description), the bot stores the information in an SQLite database and periodically checks for due events. When the scheduled time arrives, the bot posts a reminder in the originating channel and removes the event from the database.

## Purpose

*Help communities, teams and study groups stay organised.* Instead of remembering meeting times manually, users create events with a simple `!schedule` command. The bot handles reminders and keeps the list tidy by deleting past events, reducing clutter in the channel.

## Technology Stack

* **Python 3** – base language.
* **discord.py** – library for interacting with the Discord API.
* **discord.ext.tasks** – built-in task helper for periodic checks. The `tasks.loop` decorator allows a background loop to run at a specified interval without manual asyncio management.
* **aiosqlite** – asynchronous wrapper around SQLite for safe concurrent access.

## Installation

1. [Create a Discord bot token](https://discord.com/developers/applications) and add the bot to your server.
2. Clone this repository and create a virtual environment:

   ```bash
   git clone https://github.com/your-username/discord-schedule-bot.git
   cd discord-schedule-bot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3
. Set the `DISCORD_TOKEN` environment variable to the bot token and start the bot:

   ```bash
   export DISCORD_TOKEN="<your token>"
   python main.py
   ```

4. (Optional) Edit the `TZ` variable in `main.py` to your preferred time zone (defaults to UTC).

## Usage

* **Schedule an event**:

  ``
  !schedule YYYY-MM-DD HH:MM Description of the event
  ``

  Example:

  ``
  !schedule 2025-08-01 15:30 Team sync-up meeting
  ``

  The bot replies with a confirmation and adds a 📍 reaction. At the scheduled time it will post a reminder in the same channel and delete the event from its database.

* **Listing events**: this minimal implementation does not include a list command, but adding one is straightforward (see the suggestions below).


## Quick note on background tasks

The bot uses the `discord.ext.tasks` helper. This extension simplifies running background jobs and abstracts away common pitfalls such as reconnection logic and handling `asyncio.CancelledError`. The documentation notes that the `tasks.loop` decorator allows a background loop to run at a specified interval without manual scheduling, and the tasks extension is designed to abstract these worries away.
