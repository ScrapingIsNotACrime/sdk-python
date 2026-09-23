import asyncio

from scrapingisnotacrime import AsyncScrapingIsNotACrime, NotFoundError


async def main() -> None:
    async with AsyncScrapingIsNotACrime() as client:
        try:
            page = await client.bluesky.posts("bsky.app", limit=25)
        except NotFoundError:
            print("No such profile.")
            return
        count = 0
        async for post in page:
            print(post)
            count += 1
            if count >= 100:
                break  # stop early; no further pages are fetched


asyncio.run(main())
