from collections.abc import AsyncIterator
from ollama import AsyncClient, ChatResponse
from dotenv import load_dotenv

import os

load_dotenv()

MODEL = os.environ.get("OLLAMA_MODEL")

client = AsyncClient(host=os.environ.get("OLLAMA_URL")) # non-blocking version of the Ollama client

async def stream(system: str, user:str, max_tokens: int) -> AsyncIterator[ChatResponse]:
    response = await client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        options={"num_predict": max_tokens},
        stream=True
    )
    async for chunk in response:
        yield chunk