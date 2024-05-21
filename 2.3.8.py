import threading
import traceback
from _thread import _ExceptHookArgs


def intercept(args: _ExceptHookArgs) -> None:
    with open(f'{args.thread.name}.txt', 'a') as file:
        names = [item.name for item in traceback.extract_tb(args.exc_traceback)][2:]
        chain = ' -> '.join(names)
        print(f"""Traceback:
{chain}
Exception:
{args.exc_type.__name__}: {args.exc_value}
""", file=file)


threading.excepthook = intercept


def inner():
    raise TypeError("message_error")


def test_inner():
    inner()


def my_test():
    test_inner()


my_thread = threading.Thread(target=my_test, name="my_thread")
my_thread.start()
