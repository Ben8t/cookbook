from cookbook.src.scraping import Scraper
from cookbook.src.io import write_file, write_folder
from time import sleep


def build_receipe(scraper, receipe, cat_foldername):
    receipe_filename = receipe.get('caption').lower().replace(" ", "-").replace("/", "")
    markdown_content = ""
    markdown_content = markdown_content + f"# {receipe.get('caption')}"
    receipe_content = scraper.parse_receipe(receipe)
    if receipe_content:
        markdown_content = markdown_content + f"\n![]({receipe_content.get('img')})"
        write_file(receipe_filename, markdown_content, path=f"docs/{cat_foldername}")

if __name__ == "__main__":
    BASE_URL = "https://cuisine.journaldesfemmes.fr/toutes-les-recettes/"
    LOCAL = False
    scraper = Scraper(BASE_URL)
    categories = scraper.get_recipes_categories(BASE_URL)
    if LOCAL:
        categories = [i for i in categories][0:2]
    for cat in categories:
        receipes = scraper.get_recipes_categories(cat.get("url"))
        cat_foldername = cat.get('caption').lower().replace(" ", "-")
        write_folder(cat_foldername)
        print(cat_foldername)
        for receipe in receipes:
            try:
                build_receipe(scraper, receipe, cat_foldername)
            except Exception as e:
                print(e)
                print("Sleep 2 seconds")
                sleep(2)
                try:
                    build_receipe(scraper, receipe, cat_foldername)
                except Exception as e:
                    print(f"Fail to parse {receipe.get('url')}, {e}")
