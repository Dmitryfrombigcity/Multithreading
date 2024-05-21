import threading
from dataclasses import dataclass
from typing import Callable


@dataclass
class HubHendler:
    n: int
    task: Callable
    n_threads: int

    def __post_init__(self):
        self._sem: threading.Semaphore = threading.Semaphore(self.n)

    def _get_func(self):
        with self._sem:
            self.task()

    def start_hub(self):
        for _ in range(self.n_threads):
            threading.Thread(target=self._get_func).start()
