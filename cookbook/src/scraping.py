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
    

#/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/section[1]/div/ul/li[1]/figure/a