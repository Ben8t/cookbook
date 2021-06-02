from cookbook.src.scraping import Scraper


if __name__ == "__main__":
    BASE_URL = "https://cuisine.journaldesfemmes.fr/"
    scraper = Scraper(BASE_URL)
    print(scraper)