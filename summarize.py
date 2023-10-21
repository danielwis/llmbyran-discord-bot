import os
from typing import Generator

import openai
import tiktoken

SYSTEM_MESSAGE = [
    {
        "role": "system",
        "content": "summarize the following messages, disregard uninportant messages",
    }
]
GPT_3_MAX_TOKENS = 4096
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
MODEL = "gpt-3.5-turbo"


def gpt_summarize(messages: list):
    # This should really not be fetched here but i cba to look up all documentation atm :)
    openai.api_key = os.environ["OPENAI_API_KEY"]
    concatMessage = ""
    for message in messages:
        concatMessage += message + "\n"

    tokens = len(enc.encode(concatMessage))
    if tokens > GPT_3_MAX_TOKENS:
        return gpt_summarize(messages[0 : len(messages) // 2]) + gpt_summarize(
            messages[len(messages) // 2 :]
        )
    responses = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "summarize the following messages into a list, delimited with two colons ('::'). Disregard uninportant messages.",
            },
            {"role": "user", "content": concatMessage},
        ],
    )

    if isinstance(responses, Generator):
        responses = list(responses)
    elif isinstance(responses, dict):
        responses = [responses]
    elif isinstance(responses, list):
        pass
    else:
        raise ValueError("Unexpected response type")

    response = responses[0]
    summary_items = response.choices[0].message.content.split("::")
    for item in summary_items:
        item = f"- {item}"
    summary = "\n".join(summary_items)

    return summary
