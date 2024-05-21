import threading
from concurrent.futures import ThreadPoolExecutor


def task(num: int):
    print(f'Поток {threading.current_thread().name} выполняет задачу с аргументом {num}, '
          f'всего {threading.active_count()} активных потока')


with ThreadPoolExecutor(
        max_workers=3,
        thread_name_prefix='task_pool',
        initializer=lambda: print(f'Поток {threading.current_thread().name} выполняет инициализацию')
) as pool:
    pool.map(task, range(1, 11))
