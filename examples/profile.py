from scrapingisnotacrime import ScrapingIsNotACrime

# Reads SCRAPINGISNOTACRIME_API_KEY from the environment.
with ScrapingIsNotACrime() as client:
    profile = client.instagram.profile("nasa")
    print(profile["username"], profile["followers"])
