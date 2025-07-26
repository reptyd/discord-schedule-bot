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

3. Set the `DISCORD_TOKEN` environment variable to the bot token and start the bot:

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

## Demonstration idea (≤2 min)

1. Start recording a Loom video and introduce the bot in a test Discord server.
2. Use the `!schedule` command to create an event a minute into the future.
3. Show the bot’s acknowledgement message with the 📍 reaction.
4. Wait until the reminder fires; highlight that the bot automatically cleans up old events.
5. Optionally schedule a second event and cancel it manually by deleting the row in the database or adding a cancel command to illustrate extendability.

## What can be improved for a client

* **Time zone handling** – accept time in the user’s local time zone and convert to UTC.
* **Recurring events** – allow daily/weekly repeats or custom recurrence rules.
* **List and delete commands** – add commands like `!events` to list upcoming events and `!cancel <id>` to remove a scheduled entry.
* **Role mention** – ping a specific role when posting reminders to alert all relevant members.
* **Web dashboard** – provide a simple front-end to view and manage scheduled events outside of Discord.

## Quick note on background tasks

The bot uses the `discord.ext.tasks` helper. This extension simplifies running background jobs and abstracts away common pitfalls such as reconnection logic and handling `asyncio.CancelledError`. The documentation notes that running a loop in the background at a specified interval is a common pattern, and the tasks extension is designed to abstract these worries away.
