from unittest.mock import AsyncMock

import pytest
from app import llm

async def fake_response():
    # imitates what Ollama returns when stream=True
    for text in ["Hel", "lo,", "wor", "ld"]:
        yield text

@pytest.mark.asyncio
async def test_stream_yields_chunks_and_passes_args(monkeypatch):
    fake_chat = AsyncMock(return_value=fake_response())
    monkeypatch.setattr(llm.client, "chat", fake_chat)

    chunks = [c async for c in llm.stream(system="sys", user="hi", max_tokens=10)]

    assert chunks == ["Hel", "lo,", "wor", "ld"]
    kwargs = fake_chat.call_args.kwargs
    assert kwargs["stream"] is True
    assert kwargs["options"] == {"num_predict": 10}
    assert kwargs["messages"][0] == {"role": "system", "content": "sys"}
    assert kwargs["messages"][1] == {"role": "user", "content": "hi"}