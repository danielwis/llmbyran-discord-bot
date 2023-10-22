# GPT-Summarize

A Discord bot that summarises messages in a channel for your (and others') convenience using GPT-3.5 turbo.

## Quick start

1. Clone the repository: `git clone git@github.com:danielwis/llmbyran-discord-bot.git`
2. Rename (or copy) the `.env.example` file to just `.env` and replace the placeholder values with your real ones.
3. Install the requirements: `pip install -r requirements.txt`
4. Run the application: `python main.py`
5. Run the slash command `/summarize` in any channel the bot is allowed to access. Optionally, you can set a few parameters to limit the number of messages read:
   1. `howmany` controls the number of messages to read. Bot messages are discarded, but it's not possible to filter this beforehand and thus only `howmany - <number of bot messages within the last howmany>` messages will actually be considered. For example, passing `howmany:20` with 5 of the latest 20 being bot messages, will result in only 15 messages being considered.
   2. `before` restricts the message being read to those sent _before_ a certain time. Takes a string formatted like a date(time) - anything parseable by the Python `datetime.datetime.fromisoformat` function is fair game.
   3. `after` restricts the message being read to those sent _after_ a certain time. Takes a string formatted like a date(time) - anything parseable by the Python `datetime.datetime.fromisoformat` function is fair game.
   4. `individual` controls whether GPT should attempt to summarise the messages individually (e.g. "take each message and summarise it") or all together (e.g. "give me a summary of what people have said in the latest `howmany` messages").
