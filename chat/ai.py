from openai import OpenAI
from db.MySqlConn import config

OPENAI_CHAT_COMPLETION_OPTIONS = {
    "temperature": 1,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stream": True,
    "stop": None,
    "model": config["AI"]["MODEL"]
}


async def ChatCompletionsAI(logged_in_user, messages):
    level = logged_in_user.get("level")

    answer = ""

    client = OpenAI(api_key=config["AI"]["TOKEN"])
    with client.chat.completions.with_streaming_response.create(
            messages=messages,
            max_tokens=1500,
            **OPENAI_CHAT_COMPLETION_OPTIONS) as response:
        for r in response.parse():
            if r.choices:
                delta = r.choices[0].delta
                if delta.content:
                    answer += delta.content
                yield answer, r.choices[0].finish_reason
