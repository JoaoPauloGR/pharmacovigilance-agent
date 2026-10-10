import asyncio
import llm


async def main():
    async for chunk in llm.stream(
        system="You are a helpful assistant.",
        user="Say hello in five words.",
        max_tokens=50,
    ):
        print(chunk.message.content, end="", flush=True)
        if chunk.done:
            print(f"\n\nin={chunk.prompt_eval_count} out={chunk.eval_count}")


asyncio.run(main())