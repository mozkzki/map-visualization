import logging

import requests
from bs4 import BeautifulSoup


class Geocoder:
    url = "http://www.geocoding.jp/api/"

    def get(self, address: str) -> tuple:
        payload = {"q": address}
        response = requests.get(self.url, params=payload)

        soup = BeautifulSoup(response.content, "lxml")
        lat = ""
        lng = ""
        if soup.find("error"):
            logging.error(f"invalid address submitted. {address}")
            # raise ValueError(f"invalid address submitted. {address}")
        else:
            lat = soup.find("lat").string
            lng = soup.find("lng").string

        return (lat, lng)
