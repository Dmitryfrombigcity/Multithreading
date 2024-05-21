import threading
from itertools import count
from typing import Callable

storage = threading.local()


class TestWorker(threading.Thread):
    def __init__(
            self,
            task: Callable,
            permission: Callable
    ) -> None:
        super().__init__()
        self.permission = permission
        self.task = task
        self.condition = threading.Condition()

    def make_work(self) -> None:
        with self.condition:
            tmp = self.condition.wait_for(
                predicate=self.permission,
                timeout=1
            )
            if tmp:
                self.task()
            else:
                print(
                    f"{threading.current_thread().name} завершается по таймеру"
                )

    def run(self) -> None:
        self.make_work()


def task() -> None:
    print(
        f"{threading.current_thread().name} ВЫЗЫВАЕТ ЗАДАЧУ task!"
    )


_count = count(1)


def permission() -> bool:
    n = next(_count)
    thread_name = threading.current_thread().name
    print(f"{thread_name} проверяет предикат, permission вызывается {n}-й раз")
    if getattr(storage, 'sentinel', None):
        return True
    if n == 2:
        storage.sentinel = True
    return False


for _ in '123':
    TestWorker(task, permission).start()
