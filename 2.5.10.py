import threading
from typing import Any

import requests

sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]


class GetHeaders(threading.Thread):
    def __init__(
            self,
            url: str,
            url_headers: dict[str, Any] | None = None
    ) -> None:
        super().__init__()
        self.url = url
        self.url_headers = url_headers

    def run(self) -> None:
        self.url_headers = {self.url: get_request_header(self.url)}


def get_request_header(url: str) -> dict[str, Any]:
    return requests.get(url).headers


thrs = [GetHeaders(source) for source in sources]
results: dict[str, Any] = {}
for thr in thrs:
    thr.start()
for thr in thrs:
    thr.join(2.1)
    if thr.url_headers:
        results.update(thr.url_headers)
