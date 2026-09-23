import asyncio

from scrapingisnotacrime import AsyncScrapingIsNotACrime, NotFoundError


async def main() -> None:
    async with AsyncScrapingIsNotACrime() as client:
        try:
            page = await client.bluesky.posts("bsky.app", limit=25)
        except NotFoundError:
            print("No such profile.")
            return
        async for post in page:
            print(post)


asyncio.run(main())
