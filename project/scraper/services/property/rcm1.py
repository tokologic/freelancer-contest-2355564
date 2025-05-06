from typing import List
import requests
import math

from bs4 import BeautifulSoup, element
from project.scraper.models import AssetProperty


class Rcm1MarketplaceScraper:

    def __init__(self, token: str, per_page: int = 100):
        self.token = token
        self.url = "https://my.rcm1.com/api/AjaxEngine/GetListingsHtml"

        self.total = 0
        self.per_page = per_page
    
    def handle(self):
        response = self.page(1)

        total = response['total']

        number_of_pages = math.ceil(total/self.per_page)
        for page in range(0, number_of_pages):
            if page == 0:
                continue  # already fetched first

            start = (page * self.per_page) + 1
            self.page(start)



    def page(self, start: int = 1) -> dict:
        url = f"{self.url}?pv={self.token}"

        response = requests.post(url, {
            "FilterProjectName": None,
            "FilterProjectAssetSubType": None,
            "FilterProjectState": None,
            "FilterProjectCountry": None,
            "FilterProjectUnits": "All",
            "FilterProjectValue": "All",
            "FilterProjectUserAttr": 0,
            "PageSize": self.per_page,
            "Start": start,
            "FilterProjectMsa": None,
            "FilterProjectBroker": None,
        })

        self.store(response.json()['html'])
        return response.json()

    def sanitize(self, html: str) -> str:
        return (
            html.replace(f'\"', '"')
            .replace("\r", "")
            .replace("\n", "")
            .replace("\t", "")
        )
    

    def store(self, html):

        finder = Finder(self.sanitize(html))
        for property in finder.properties():
            AssetProperty.objects.create(
                name=property.name,
                cover_image_url=property.cover_image_url,
                price=property.price,
                city=property.city,
                kind=property.kind,
                contact_name=property.contact_name,
                company=property.company,
                summary=property.summary,
            )

class PropertyFinder:
    def __init__(self, property: element.Tag):
        self.property: element.Tag = property

        self.__image_card__ = self.property.select("div.rcm_img_section")[0]
        self.__caption_card__ = self.property.select("div.rcm_card_caption")[0]

    @property
    def name(self) -> str:
        return self.__caption_card__.select("div.headline")[0].text
    
    @property
    def cover_image_url(self) -> str:
        image = self.__image_card__.select("img")[0]
        return image.get("src")
    
    @property
    def price(self) -> float:
        price_selector = self.__image_card__.select("div.price")
        if len(price_selector) == 0:
            return None
        
        price = price_selector[0].text
        return price
    
    @property
    def city(self) -> str:
        return self.__caption_card__.select("div.city")[0].text
    
    @property
    def kind(self) -> str:
        return ""
    
    @property
    def size(self) -> str:
        return ""

    @property
    def status(self) -> str:
        return ""
    
    @property
    def summary(self) -> str:
        detail = self.__caption_card__.select("div.more-details")[0]
        summary_selector = detail.select("div.summary")
        if len(summary_selector) == 0:
            return None
        
        summary = summary_selector[0].text
        return summary
    
    @property
    def contact_name(self) -> str:
        detail = self.__caption_card__.select("div.more-details")[0]
        return detail.select(".contact > .name")[0].text
    
    @property
    def company(self) -> str:
        detail = self.__caption_card__.select("div.more-details")[0]
        return detail.select(".contact > .company")[0].text



        
class Finder:
    def __init__(self, html: str):
        self.html: str = html
        self.soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

        self._properties_ = []

    def properties(self) -> List[PropertyFinder]:
        parent = self.soup.find("div", class_="property_area")
        properties = parent.find_all(recursive=False)
        for property in properties:
            self._properties_.append(PropertyFinder(property))

        return self._properties_