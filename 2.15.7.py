from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any

sources = [1, 2, 3]


def worker(source: Any):
    ...


def post_worker(future: Future):
    try:
        print(f'{future.result()} saved')
    except Exception:
        print(future.exception())


with ThreadPoolExecutor() as pool:
    for source in sources:
        future = pool.submit(worker, source)
        future.add_done_callback(post_worker)
