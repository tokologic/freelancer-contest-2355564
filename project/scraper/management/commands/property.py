import requests

from django.core.management.base import BaseCommand

from project.scraper.services.property.rcm1 import Rcm1MarketplaceScraper


class Command(BaseCommand):
    help = "Scrape info from property websites."

    # def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        scraper = Rcm1MarketplaceScraper(token="SFh_vpTV6FE6kPQ3K5oDjDISfZcVJLJtiFcKcbENqhk")
        scraper.handle()
        # from bs4 import BeautifulSoup

        # token = "SFh_vpTV6FE6kPQ3K5oDjDISfZcVJLJtiFcKcbENqhk"

        # url = f"https://my.rcm1.com/api/AjaxEngine/GetListingsHtml?pv={token}"

        # response = requests.post(url, {
        #     "FilterProjectName": None,
        #     "FilterProjectAssetSubType": None,
        #     "FilterProjectState": None,
        #     "FilterProjectCountry": None,
        #     "FilterProjectUnits": "All",
        #     "FilterProjectValue": "All",
        #     "FilterProjectUserAttr": 0,
        #     "PageSize": 100,
        #     "Start": 1,
        #     "FilterProjectMsa": None,
        #     "FilterProjectBroker": None,
        # })

        # # todo: when response not success

        # html = response.json()['html']

        # html = (
        #     html.replace(f'\"', '"')
        #     .replace("\r", "")
        #     .replace("\n", "")
        #     .replace("\t", "")
        # )

        # soup = BeautifulSoup(html, "html.parser")
        # parent = soup.find("div", class_="property_area")
        # properties = parent.find_all(recursive=False)

        # i = 1
        # for property in properties:
        #     print(i)
        #     # try:
        #     image_card = property.select("div.rcm_img_section")[0]
        #     image = image_card.select("img")[0]
        #     image_link = image.get("src")
        #     image_alt = image.get("alt")

        #     price_string = ""
        #     price = image_card.select("div.price")
        #     if len(price) > 0:
        #         price_string = price[0].text
            

        #     caption_card = property.select("div.rcm_card_caption")[0]
        #     title = caption_card.select("div.headline")[0].text
        #     city = caption_card.select("div.city")[0].text

        #     features = caption_card.select("div.features")[0]
        #     feature_items = features.select("div.feature-label")
        #     type_string = ""
        #     size_string = ""
        #     status_string = ""
        #     for feature in feature_items:
        #         label = feature.find(text=True, recursive=False).strip()
        #         value = feature.select('.feature-value')[0].text
        #         if label.lower() == "type":
        #             type_string = value
        #         elif label.lower() == "size":
        #             size_string = value
        #         elif label.lower() == "status":
        #             status_string = value

        #     details = caption_card.select("div.more-details")[0]

        #     summary_string = ""
        #     summary = details.select("div.summary")
        #     if len(summary) > 0:
        #         summary_string = summary[0].text

        #     contact_name = details.select(".contact > .name")[0].text
        #     contact_company = details.select(".contact > .company")[0].text


        #     print({
        #         "title": title,
        #         "image_link": image_link,
        #         "image_alt": image_alt,
        #         "price": price_string,
        #         "city": city,
        #         "type": type_string,
        #         "size": size_string,
        #         "status": status_string,
        #         "summary": summary_string,
        #         "contact_name": contact_name,
        #         "contact_company": contact_company,
        #     })
        #     # except IndexError:
        #     #     print(property)

        #     i += 1


