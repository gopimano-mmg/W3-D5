import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}

try:
    response = requests.get(URL, headers=headers, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # BBC headlines normally appear inside h2 tags.
        headline_tags = soup.select('h2[data-testid="card-headline"]')

        # Fallback if BBC changes the data-testid attribute.
        if not headline_tags:
            headline_tags = soup.find_all("h2")

        headlines = []

        for tag in headline_tags:
            headline = tag.get_text(" ", strip=True)

            if headline and headline not in headlines:
                headlines.append(headline)

            if len(headlines) == 5:
                break

        print("\nTop 5 News Headlines\n")

        if headlines:
            for number, headline in enumerate(headlines, start=1):
                print(f"{number}. {headline}")

            if len(headlines) < 5:
                print(f"\nOnly {len(headlines)} headlines were available.")
        else:
            print("No headlines were found.")

    else:
        print(f"Failed to retrieve the webpage. HTTP status: {response.status_code}")

except requests.RequestException as error:
    print(f"An error occurred: {error}")