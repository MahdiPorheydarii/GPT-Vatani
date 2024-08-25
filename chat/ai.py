from openai import OpenAI
from db.MySqlConn import config

OPENAI_CHAT_COMPLETION_OPTIONS = {
    "temperature": 1,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stream": True,
    "stop": None,
}


async def ChatCompletionsAI(logged_in_user, messages):
    sub = logged_in_user.get("sub")
    OPENAI_CHAT_COMPLETION_OPTIONS['model'] = ['gpt-4o-mini', 'gpt-4o'][max(0, sub-1)]
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
