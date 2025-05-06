import math
import re
from typing import List

import requests
from bs4 import BeautifulSoup, element

from project.scraper.models import AssetProperty


class Rcm1MarketplaceScraper:
    def __init__(self, token: str, per_page: int = 100):
        self.token = token
        self.url = "https://my.rcm1.com/api/AjaxEngine/GetListingsHtml"

        self.total = 0
        self.per_page = per_page
        self.stdout = None

    def set_stdout(self, stdout):
        self.stdout = stdout

    def handle(self):
        response = self.page(1)

        total = response["total"]

        number_of_pages = math.ceil(total / self.per_page)
        for page in range(0, number_of_pages):
            if page == 0:
                continue  # already fetched first

            start = (page * self.per_page) + 1
            self.page(start)

    def page(self, start: int = 1) -> dict:
        self.stdout.write(f"Fetching item {start} and further...")
        url = f"{self.url}?pv={self.token}"

        response = requests.post(
            url,
            {
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
            },
        )

        self.store(response.json()["html"])
        return response.json()

    def sanitize(self, html: str) -> str:
        return html.replace(r"\"", '"').replace("\r", "").replace("\n", "").replace("\t", "")

    def store(self, html):

        finder = Finder(self.sanitize(html))
        for property in finder.properties():
            self.stdout.write(f"Found: {property.name}")
            AssetProperty.objects.create(
                name=property.name,
                cover_image_url=property.cover_image_url,
                price=property.price,
                city=property.city,
                kind=property.kind,
                size=property.size,
                status=property.status,
                contact_name=property.contact_name,
                company=property.company,
                summary=property.summary,
                source="https://www.rcm1.com/marketplace/",
            )


class PropertyFinder:
    def __init__(self, property: element.Tag):
        self.property: element.Tag = property

        self.__image_card__ = self.property.select("div.rcm_img_section")[0]
        self.__caption_card__ = self.property.select("div.rcm_card_caption")[0]

    def first_if_exists(self, selector):
        if len(selector) == 0:
            return None
        return selector[0]

    @property
    def name(self) -> str:
        headline_selector = self.__caption_card__.select("div.headline")
        result = self.first_if_exists(headline_selector)
        if result:
            return result.text
        return None

    @property
    def cover_image_url(self) -> str:
        image_selector = self.__image_card__.select("img")
        result = self.first_if_exists(image_selector)
        if result:
            return result.get("src")
        return None

    def _parse_currency_(self, value):
        raw = re.sub(r"[^\d.,-]", "", value)

        # Heuristic: if comma is used as decimal, it's likely EU format
        if raw.count(",") == 1 and raw.count(".") > 1:
            # Example: 1.234.567,89 → 1234567.89
            raw = raw.replace(".", "").replace(",", ".")
        elif raw.count(",") > 1 and raw.count(".") == 0:
            # Example: 1,234,567 → US-style commas, remove them
            raw = raw.replace(",", "")
        elif raw.count(",") == 1 and raw.count(".") == 0:
            # Could be 1,50 (EU format for 1.50)
            raw = raw.replace(",", ".")

        try:
            return float(raw)
        except ValueError:
            return None  # or raise Exception("Invalid currency format")

    @property
    def price(self) -> float:
        price_selector = self.__image_card__.select("div.price")
        result = self.first_if_exists(price_selector)
        if not result:
            return

        return self._parse_currency_(result.text)

    @property
    def city(self) -> str:
        city_selector = self.__caption_card__.select("div.city")
        result = self.first_if_exists(city_selector)
        if not result:
            return
        return result.text

    @property
    def kind(self) -> str:
        selector = self.__caption_card__.select(
            ".features > .feature-label > .feature-value.asset-type"
        )
        result = self.first_if_exists(selector)
        if result:
            return result.text
        return None

    @property
    def size(self) -> str:
        selector = self.__caption_card__.select(
            ".features > .feature-label > .feature-value.asset-units"
        )
        result = self.first_if_exists(selector)
        if result:
            return result.text

        selector = self.__caption_card__.select(
            ".features > .feature-label > .feature-value.asset-sqft"
        )
        result = self.first_if_exists(selector)
        if result:
            return result.text

        return None

    @property
    def status(self) -> str:
        selector = self.__caption_card__.select(
            ".features > .feature-label > .feature-value.asset-status"
        )
        result = self.first_if_exists(selector)
        if result:
            return result.text
        return None

    @property
    def summary(self) -> str:
        summary_selector = self.__caption_card__.select("div.more-details > .summary")
        summary = self.first_if_exists(summary_selector)
        if not summary:
            return None

        return summary.text

    @property
    def contact_name(self) -> str:
        selector = self.__caption_card__.select("div.more-details .contact > .name")
        result = self.first_if_exists(selector)
        if not result:
            return None
        return result.text

    @property
    def company(self) -> str:
        selector = self.__caption_card__.select("div.more-details .contact > .company")
        result = self.first_if_exists(selector)
        if not result:
            return None
        return result.text


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
