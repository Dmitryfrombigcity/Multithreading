import threading
import traceback
from _thread import _ExceptHookArgs
from typing import reveal_type


def task() -> None:
    raise TypeError("ops, TypeError")


def custom_hook(args: _ExceptHookArgs) -> None:
    # print(args.__dir__())
    print(_ExceptHookArgs.__mro__)
    reveal_type(args)
    print(f"Тип исключения: {args.exc_type.__name__}")
    print(f"Сообщение исключения: {args.exc_value}")
    print(f"Номер потока: {args.thread.__dict__}")
    print(f"Имя потока: {args.thread.name}")
    print(f"Путь исключения:")
    traceback.print_tb(args.exc_traceback)


threading.excepthook = custom_hook

thread = threading.Thread(target=task)
thread.start()
