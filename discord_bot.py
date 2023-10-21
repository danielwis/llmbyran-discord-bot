import os

import discord
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv

from summarize import gpt_summarize

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]
GUILD = int(os.environ["DISCORD_GUILD"])

intents = discord.Intents.all()

client = discord.Client(intents=intents)
slash = SlashCommand(
    client, sync_commands=True
)  # Declares slash commands through the client.
guild_ids = [799601314765340693]  # Guild ID in this array.


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == GUILD:
            break
    else:
        print("No guild detected, exiting")
        exit(1)

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})\n"
    )

    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


async def process_gpt_responses(channel, n: int, send=None):
    if send is None:
        send = channel.send
    messages = await channel.history(limit=n).flatten()
    msglist = []
    for message in messages:
        msglist.append(f"{message.author.name}:{message.content}")

    await send(gpt_summarize(msglist))


@slash.slash(name="summarize", guild_ids=guild_ids)
async def _summarize(ctx: SlashContext, howmany: int = 10):
    await ctx.defer()
    await process_gpt_responses(ctx.channel, n=howmany, send=ctx.send)


client.run(TOKEN)
