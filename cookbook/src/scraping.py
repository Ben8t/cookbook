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
        tree = self.get_tree(url)
        img = tree.xpath('//img[@class="bu_cuisine_img_noborder photo"]/@src')[0]
        recipe_resume_tree = tree.xpath('//div[@class="app_recipe_resume"]')
        recipe_resume = [i for i in self.parse_recipe_resume(recipe_resume_tree)]

        return {
            "url": url,
            "name": tree.xpath('//*[@id="jStickySize"]/header/h1/text()')[0],
            "img": img,
            "recipe_resume": recipe_resume
        }

    def parse_recipe_resume(self, recipe_resume_tree):
        for resume in recipe_resume_tree[0].xpath('.//div'):
            flat = "".join(resume.xpath('.//span/text()')).replace("\n", "").strip()
            strong = resume.xpath('.//span/strong/text()')
            if flat and strong:
                yield {
                    "flat": flat,
                    "strong": strong[0]
                }