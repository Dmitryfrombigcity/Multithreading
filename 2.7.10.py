import queue
import threading
from typing import Generator, Callable, Any

tmp_queue: queue.Queue[Any] = queue.Queue()


def producer(
        source: Generator,
        tmp_queue: queue.Queue[Any]
) -> None:
    for item in source:
        tmp_queue.put(item)


def consumer(
        handler: Callable,
        tmp_queue: queue.Queue[Any]
) -> None:
    while True:
        try:
            handler(tmp_queue.get(timeout=0.21))
        except queue.Empty:
            logging_escape()
            break


def get_obj() -> Generator:
    yield from (1, 2, 3, 4)


def handler(item) -> None:
    print(f'{threading.current_thread()= }, {item= }')


def logging_escape() -> None:
    print('The END')


thread_1 = threading.Thread(
    target=producer,
    args=(get_obj(), tmp_queue),
    name="producer"
)
thread_1.start()

for index in (1, 2):
    threading.Thread(
        target=consumer,
        args=(handler, tmp_queue),
        name=f"consumer_{index}",
        daemon=True
    ).start()
