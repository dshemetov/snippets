# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "duckdb",
#     "feedparser",
#     "python-dotenv",
#     "requests",
# ]
# ///
"""RSS feed reader.

Maintains a simple DB of RSS posts and posts new entries to Discord.

Setup as a cron job to run every Friday at 9am PST. Doesn't send more
than 10 entries per feed and only sends entries that are less than 4 weeks old.
"""

import os
from datetime import datetime, timedelta
from time import mktime
from typing import cast

import duckdb
import feedparser
import requests
from dotenv import load_dotenv

load_dotenv()

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
con = duckdb.connect("rss.db")
# RSS feeds to monitor, with their URLs
# The names will be used in the message, so keep them short and clean
feeds = {
    "Factorio": "https://www.factorio.com/blog/rss",
}
# You'll need to set up a Discord webhook to post messages
# https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
discord_hook_url = os.getenv("DISCORD_WEBHOOK")
if not discord_hook_url:
    raise ValueError("DISCORD_WEBHOOK environment variable not set.")
# Entries are considered stale after
stale_after = timedelta(weeks=4)
# Max number of entries to send
max_entries = 10


def main():
    """Bot main script."""
    for feed_name, feed_link in feeds.items():
        feed = cast(feedparser.FeedParserDict, feedparser.parse(feed_link))
        con.sql(f"CREATE TABLE IF NOT EXISTS {feed_name} (id STRING PRIMARY KEY, title STRING, updated TIMESTAMPTZ)")

        sent_entries = con.sql(f"SELECT * FROM {feed_name}").df()
        for i, entry in enumerate(feed.entries):
            # If the entry is already in the DB, skip it
            if entry.id in sent_entries.id.values:
                continue
            updated = datetime.fromtimestamp(mktime(entry.updated_parsed))
            con.execute(
                f"INSERT OR IGNORE INTO {feed_name} VALUES (?, ?, ?)",
                (entry.id, entry.title, updated),
            )
            # Cap max sent entries and only send recent ones
            if i < max_entries and updated > today - stale_after:
                discord_hook(feed_name, entry.title, entry.link)


def discord_hook(feed_name, title, link):
    """Post message to Discord."""
    data = {"content": f"New {feed_name} blog post: [{title}]({link})"}
    requests.post(discord_hook_url, json=data, timeout=5)


if __name__ == "__main__":
    main()
