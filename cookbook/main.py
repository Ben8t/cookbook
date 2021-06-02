from cookbook.src.scraping import Scraper
from cookbook.src.io import write_file, write_folder


if __name__ == "__main__":
    BASE_URL = "https://cuisine.journaldesfemmes.fr/toutes-les-recettes/"
    scraper = Scraper(BASE_URL)
    categories = scraper.get_recipes_categories(BASE_URL)
    for cat in categories:
        receipes = scraper.get_recipes_categories(cat.get("url"))
        cat_foldername = cat.get('caption').lower().replace(" ", "-")
        write_folder(cat_foldername)
        print(cat_foldername)
        for receipe in receipes:
            receipe_filename = receipe.get('caption').lower().replace(" ", "-").replace("/", "")
            write_file(receipe_filename, f"# {receipe.get('caption')}", path=f"docs/{cat_foldername}")