import queue
import threading
from typing import Generator, Callable, Any

my_queue: queue.Queue[Any] = queue.Queue()


def producer(
        source: Generator,
        queue: queue.Queue[Any]
) -> None:
    for item in source:
        queue.put(item)


def consumer(
        handler: Callable,
        queue: queue.Queue[Any]
) -> None:
    while not queue.empty():
        handler(queue.get())


def get_obj() -> Generator:
    yield from (1, 2, 3, 4)


def handler(item) -> None:
    print(f'{threading.current_thread()= }, {item= }')


thread_1 = threading.Thread(
    target=producer,
    args=(get_obj(), my_queue),
    name="producer"
)
thread_1.start()
thread_1.join()
for index in (1, 2):
    threading.Thread(
        target=consumer,
        args=(handler, my_queue),
        name=f"consumer_{index}"
    ).start()
