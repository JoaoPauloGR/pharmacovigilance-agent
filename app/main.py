from app import llm
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    max_tokens: int = Field(default=512, le=2_048)

PROMPT_TEMPLATE = """You are an assistant that answers questions about FAERS, the FDA Adverse Event Reporting System.
Answer in short, plain sentences.
If you do not know the answer, say "I don't know".
Do not give medical advice."""

app = FastAPI(
    title="FAERS AI",
    version="0.0.1"
)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/v1/chat/stream")
async def chat_stream(req: ChatIn):
    async def tokens():
        async for chunk in llm.stream(
            system=PROMPT_TEMPLATE, user=req.message,
            max_tokens=req.max_tokens
        ):
            yield f"data: {chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(tokens(),
                             media_type="text/event-stream")