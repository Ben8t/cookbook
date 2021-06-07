from cookbook.src.scraping import Scraper
from cookbook.src.io import write_file, write_folder
from time import sleep
from jinja2 import Template

def read_template(template_file: str) -> Template:
    with open(template_file, "r") as template_open:
        return Template(template_open.read())


def build_receipe(scraper, receipe, cat_foldername):
    receipe_filename = receipe.get('caption').lower().replace(" ", "-").replace("/", "")
    markdown_content = ""
    markdown_content = markdown_content + f"# {receipe.get('caption')}"
    receipe_content = scraper.parse_receipe(receipe)
    if receipe_content:
        template  = read_template("cookbook/template/receipe_template.md")
        data = template.render(receipe_content)
        write_file(receipe_filename, data, path=f"docs/{cat_foldername}")


if __name__ == "__main__":
    BASE_URL = "https://cuisine.journaldesfemmes.fr/toutes-les-recettes/"
    LOCAL = True
    scraper = Scraper(BASE_URL)
    categories = scraper.get_recipes_categories(BASE_URL)
    if LOCAL:
        categories = [i for i in categories][0:5]
    for cat in categories:
        receipes = scraper.get_recipes_categories(cat.get("url"))
        cat_foldername = cat.get('caption').lower().replace(" ", "-")
        write_folder(cat_foldername)
        print(cat_foldername)
        for receipe in receipes:
            try:
                url = receipe.get("url")
                if url.startswith("https://cuisine.journaldesfemmes.fr/recette/"):
                    build_receipe(scraper, receipe, cat_foldername)
            except Exception as e:
                print(e)
                print("Sleep 2 seconds")
                sleep(2)
                try:
                    build_receipe(scraper, receipe, cat_foldername)
                except Exception as e:
                    print(f"Fail to parse {receipe.get('url')}, {e}")
