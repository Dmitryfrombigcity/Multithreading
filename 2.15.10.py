from concurrent.futures import ThreadPoolExecutor, wait
from time import perf_counter
from typing import Any

import requests

sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]

headers_stor: dict[str, Any] = dict.fromkeys(sources, 'no_response')


def get_request_header(url: str) -> dict[str, Any]:
    return requests.get(url).headers


def run(url) -> tuple[str, dict[str, Any]]:
    return url, get_request_header(url)


start = perf_counter()

with ThreadPoolExecutor(max_workers=5) as pool:
    futures = [pool.submit(run, url) for url in sources]
    for future in wait(futures, timeout=1.5).done:
        url, headers = future.result()
        headers_stor[url] = headers

print(perf_counter() - start)
