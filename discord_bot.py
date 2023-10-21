import os
from datetime import datetime

import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv

from summ import gpt_summarize

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


async def process_gpt_responses(
    channel,
    n: int,
    before: datetime | None = None,
    after: datetime | None = None,
    individual: bool = True,
    send=None,
):
    if send is None:
        send = channel.send
    messages = await channel.history(limit=n, before=before, after=after).flatten()

    msglist = []
    for message in messages:
        if not message.author.bot:
            msglist.append(f"{message.author.name}:{message.content}")

    # History starts from most recent and moves back, reverse this to get the
    # messages in chronological order
    msglist.reverse()

    pre_summary = (
        f"**Here's a summary of the latest {len(msglist)} messages"
        + (f" (before {before})" if before else "")
        + (f" (after {after})" if after else "")
        + " (removed any sent by a bot):**\n"
    )
    await send(pre_summary + gpt_summarize(msglist, individual_summaries=individual))


@slash.slash(
    name="summarize",
    options=[
        create_option(
            name="howmany",
            description="How many messages to look through",
            option_type=4,  # int
            required=False,
        ),
        create_option(
            name="before",
            description="Only include messages sent before this time",
            option_type=3,  # str
            required=False,
        ),
        create_option(
            name="after",
            description="Only include messages sent after this time",
            option_type=3,  # str
            required=False,
        ),
        create_option(
            name="individual",
            description="Whether to summarize each message separately",
            option_type=5,  # bool
            required=False,
        )
    ],
    guild_ids=guild_ids,
)
async def _summarize(
    ctx: SlashContext,
    howmany: int = 10,
    before: str = "",
    after: str = "",
    individual: bool = True,
):
    if before:
        try:
            before_dt = datetime.fromisoformat(before)
        except ValueError:
            await ctx.send(f"Invalid 'before' datetime provided: {before}")
            return
    else:
        before_dt = None

    if after:
        try:
            after_dt = datetime.fromisoformat(after)
        except ValueError:
            await ctx.send(f"Invalid 'after' datetime provided: {after}")
            return
    else:
        after_dt = None

    await ctx.defer()
    await process_gpt_responses(
        ctx.channel,
        n=howmany,
        before=before_dt,
        after=after_dt,
        individual=individual,
        send=ctx.send,
    )


client.run(TOKEN)
