# Авторский вариант.
# Есть вопросы.
import threading
from queue import Queue, PriorityQueue
from threading import Thread
from time import sleep
from typing import Generator

from _2_7_11 import CCD

main_queue = PriorityQueue(maxsize=30)
sup_queue = Queue()


def producer():
    for declaration in get_next_declaration():
        if declaration is None:
            break
        ccd = CCD(declaration)
        if not main_queue.full():
            main_queue.put(ccd)
        else:
            sup_queue.put(ccd)


def consumer():
    while True:
        try:
            ccd = main_queue.get()
            handler(ccd)
        finally:
            main_queue.task_done()


def get_next_declaration() -> Generator:
    yield from (d1, d2, d3, d4, d5, d6, d7, None)


d1 = {"cat": "0210", "union": True, "cargo": {"stew", 2}, "id": 1}
d2 = {"cat": "0208", "union": True, "cargo": {"liver", 1.78}, "id": 2}
d3 = {"cat": "0208", "union": True, "cargo": {"liver", 56}, "id": 3}
d4 = {"cat": "0208", "union": False, "cargo": {"pork fat", 100}, "id": 14}
d5 = {"cat": "87", "union": True, "cargo": {"bombardier", 1}, "id": 5}
d6 = {"cat": "0201", "union": False, "cargo": {"veal", 120}, "id": 7}
d7 = {"cat": "0201", "union": False, "cargo": {"veal", 79}, "id": 6}

d8 = {"cat": "0201", "union": False, "cargo": {"test", 79}, "id": 6}

def handler(item) -> bool:
    print(f'{threading.current_thread()= }, {item= }')
    return True


prod = Thread(target=producer)
prod.start()
prod.join()
Thread(target=consumer, name="inspector_1", daemon=True).start()
Thread(target=consumer, name="inspector_2", daemon=True).start()
Thread(target=consumer, name="inspector_3", daemon=True).start()

main_queue.join()

while not sup_queue.empty():
    print('FFF')
    main_queue.put(sup_queue.get())
    sleep(0)
print(threading.active_count())
