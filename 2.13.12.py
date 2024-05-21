import threading
from typing import Callable

stor_local = threading.local()


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


def permission() -> bool:
    if getattr(stor_local, 'sentinel', None):
        return True
    if getattr(stor_local, 'permission', None):
        setattr(stor_local, 'sentinel', True)
    return False


for _ in '12345':
    TestWorker(task, permission).start()
