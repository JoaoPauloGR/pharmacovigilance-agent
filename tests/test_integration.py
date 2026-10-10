from app import llm

import pytest

@pytest.mark.integration
@pytest.mark.asyncio
async def test_stream_against_real_ollama():
    chunks = [
        c async for c in llm.stream(
            system="You are a helpful assistant.",
            user="Say hello in five words.",
            max_tokens=500,
        )
    ]

    assert chunks[-1].done is True # check if the last chunk was actually the final one
    assert chunks[-1].eval_count > 0 # check if the model produced output tokens
    assert "".join(c.message.content or "" for c in chunks).strip() != "" # check if there is visible text