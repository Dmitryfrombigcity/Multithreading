import threading
from typing import Callable


def get_permission(
        permission: Callable,
        event: threading.Event
) -> None:
    while True:
        if permission():
            event.set()
            break


def get_task(
        initializer: Callable,
        task: Callable,
        event: threading.Event
) -> None:
    initializer()
    event.wait()
    task()


def delayed_launch(
        initializer: Callable,
        task: Callable,
        permission: Callable
) -> None:
    event = threading.Event()
    threading.Thread(target=get_permission, args=(permission, event)).start()
    threading.Thread(target=get_task, args=(initializer, task, event)).start()

