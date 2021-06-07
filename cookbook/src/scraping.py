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
        recipe_ingredients = [i for i in self.parse_ingredients(tree)]
        recipe_preparation_tree = tree.xpath('//li[@class="bu_cuisine_recette_prepa "]')
        recipe_preparations = [i for i in self.parse_preparation(recipe_preparation_tree)]

        return {
            "url": url,
            "name": tree.xpath('//*[@id="jStickySize"]/header/h1/text()')[0],
            "img": img,
            "recipe_resume": recipe_resume,
            "recipe_ingredients": recipe_ingredients,
            "recipe_preparations": recipe_preparations
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

    def parse_ingredients(self, tree):
        recipe_ingredients_tree = tree.xpath('//ul[@class="app_recipe_list app_recipe_list--2"]')
        for ingredient in recipe_ingredients_tree[0].xpath('.//div'):
            name = "".join(ingredient.xpath('.//div/h3/a/text()')).replace("\n", "").strip()
            img = ingredient.xpath('.//div/img/@src')
            quantity = "".join(ingredient.xpath('.//div/h3/span/@data-quantity')).replace("\n", "").strip()
            quantity_title = "".join(ingredient.xpath('.//div/h3/span/@data-mesure-singular')).replace("\n", "").strip()
            if "".join(ingredient.xpath('.//div/h3/span/text()')).replace("\n", "").strip() in [f"{i}" for i in range(0,20)]:
                quantity = float("".join(ingredient.xpath('.//div/h3/span/text()')).replace("\n", "").strip())
                quantity_title = "NONE"
            try:
                base_person_quantity = float(tree.xpath('//span[@id="numberPerson"]/text()')[0])
                if base_person_quantity:
                    quantity2, quantity4, quantity6 = self.get_quantity_coef(quantity, base_person_quantity, quantity_title)
                    if name and img:
                        yield {
                            "name": name,
                            "img": img[0],
                            "quantity2": quantity2,
                            "quantity4": quantity4,
                            "quantity6": quantity6,
                            "quantity_title": quantity_title if quantity_title != "NONE" else ""
                        }
            except:
                if name and img:
                    yield {
                        "name": name,
                        "img": img[0],
                        "quantity2": "".join(ingredient.xpath('.//div/h3/span/text()')).replace("\n", "").strip(),
                        "quantity4": "".join(ingredient.xpath('.//div/h3/span/text()')).replace("\n", "").strip(),
                        "quantity6": "".join(ingredient.xpath('.//div/h3/span/text()')).replace("\n", "").strip(),
                        "quantity_title": ""
                    }
            
    def get_quantity_coef(self, quantity, base_person_quantity: int, quantity_title):
        if quantity == "1/2":
            quantity = 0.5
        if quantity == "1/4":
            quantity = 0.25

        if quantity_title in ["g", "cl", "ml", "gousse", "c à s", "NONE", "pot", "pincée", "sachet", "tranche", "branche", "jus", "filet", "c à c"]:
                return float(quantity)*2/base_person_quantity, float(quantity)*4/base_person_quantity, float(quantity)*6/base_person_quantity
        
        return quantity, quantity, quantity

    def parse_preparation(self, recipe_preparation_tree):
        for preparation in recipe_preparation_tree:
            etape = "".join(preparation.xpath('.//span[@class="bu_cuisine_recette_prepa_etape"]/text()')).replace("\n", "").strip()
            text = "".join(preparation.xpath('.//text()')).replace("\n", "").strip()[3:]
            yield {
                "etape": etape if etape else "Pour finir",
                "text": text if etape else text[8:]
            }