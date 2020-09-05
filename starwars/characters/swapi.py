import requests


class Client:
    def __init__(self, api_url):
        self.api_url = api_url
        self.session = requests.Session()

    def get_single(self, url):
        return self.session.get(url)

    def get_paginated_results(self, path):
        url = f"{self.api_url}{path}"
        while url:
            resp = self.get_single(url)
            decoded = resp.json()
            yield from decoded["results"]
            url = decoded["next"]

    def characters(self):
        yield from self.get_paginated_results("people/")

    def planets(self):
        yield from self.get_paginated_results("planets/")
