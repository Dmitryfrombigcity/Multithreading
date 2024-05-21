import queue
import threading
from typing import Generator, Callable

from _2_7_11 import CCD

main_queue: queue.PriorityQueue[CCD] = queue.PriorityQueue(maxsize=30)
sup_queue: queue.PriorityQueue[CCD] = queue.PriorityQueue()


def producer(
        source: Generator,
        main_queue: queue.PriorityQueue[CCD],
        sup_queue: queue.PriorityQueue[CCD]
) -> None:
    for item in source:
        if item is None:
            break
        elif not main_queue.full():
            main_queue.put(CCD(item))
        else:
            sup_queue.put(CCD(item))


def consumer(
        handler: Callable,
        main_queue: queue.PriorityQueue[CCD]
) -> None:
    while True:
        if main_queue.empty():
            break
        elif handler(main_queue.get()):
            main_queue.task_done()
        else:
            ...


def get_next_declaration() -> Generator:
    yield from (d1, d2, d3, d4, d5, d6, d7, None)


d1 = {"cat": "0210", "union": True, "cargo": {"stew", 2}, "id": 1}
d2 = {"cat": "0208", "union": True, "cargo": {"liver", 1.78}, "id": 2}
d3 = {"cat": "0208", "union": True, "cargo": {"liver", 56}, "id": 3}
d4 = {"cat": "0208", "union": False, "cargo": {"pork fat", 100}, "id": 14}
d5 = {"cat": "87", "union": True, "cargo": {"bombardier", 1}, "id": 5}
d6 = {"cat": "0201", "union": False, "cargo": {"veal", 120}, "id": 7}
d7 = {"cat": "0201", "union": False, "cargo": {"veal", 79}, "id": 6}


def handler(item: CCD) -> bool:
    print(f'{threading.current_thread()= }, {item= }')
    return True

if __name__ == '__main__':

    thread_1 = threading.Thread(
        target=producer,
        args=(get_next_declaration(), main_queue, sup_queue),
        name="producer"
    )
    thread_1.start()
    thread_1.join()

    thrs = [
        threading.Thread(
            target=consumer,
            args=(handler, main_queue),
            name=f"inspector_{index}",
            daemon=True
        ) for index in (1, 2, 3)]
    for thr in thrs:
        thr.start()

    main_queue.join()
    for thr in thrs:
        thr.join()

    while sup_queue.qsize():
        main_queue.put(sup_queue.get())

    print(threading.active_count())
