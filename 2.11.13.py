import threading
from typing import Callable

barrier = threading.Barrier(4, action=finalizer)


def target_func(
        barrier: threading.Barrier,
        task_stage1: Callable,
        task_stage2: Callable
) -> None:
    task_stage1()
    barrier.wait()
    task_stage2()


for thread in range(1, 5):
    threading.Thread(
        target=target_func,
        name=f'Thread #{thread}',
        args=(barrier, task_stage1, task_stage2)
    ).start()
