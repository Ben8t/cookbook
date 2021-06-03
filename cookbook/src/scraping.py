from lxml import html
import requests


class Scraper:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_tree(self, url: str):
        response = requests.get(url)
        return html.fromstring(response.content)

    def get_recipes_categories(self, url) -> dict:
        tree = self.get_tree(url)
        elements = tree.xpath('//a[contains(@class, "bu_cuisine_recette_img")]')
        for e in elements:
            img = e.xpath('.//span/@style')[0].replace("background-image: url(", "").replace(")", "")
            caption = e.xpath('.//figcaption/text()')[0].replace("\n", "").strip()
            href = e.xpath('.//@href')[0]
            if href.startswith("https://"):
                yield {"img": img, "caption": caption, "url": href}
    
    def parse_receipe(self, receipe: dict) -> dict:
        url = receipe.get("url")
        if url.startswith("https://cuisine.journaldesfemmes.fr/recette/"):
            tree = self.get_tree(url)
            img = tree.xpath('//img[@class="bu_cuisine_img_noborder photo"]/@src')[0]
            return {
                "url": url,
                "name": tree.xpath('//*[@id="jStickySize"]/header/h1/text()'),
                "img": img
            }
        else:
            print(f"Probably not a good receipe url, {url}")