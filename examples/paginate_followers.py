from scrapingisnotacrime import ScrapingIsNotACrime

with ScrapingIsNotACrime() as client:
    for count, user in enumerate(client.github.followers("torvalds", limit=100), start=1):
        print(user["username"])
        if count >= 250:
            break  # stop early; no further pages are fetched
