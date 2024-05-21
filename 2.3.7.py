import threading
from _thread import _ExceptHookArgs


def intercept(args: _ExceptHookArgs) -> None:
    message: str = f'{args.thread.name}, {args.exc_type.__name__}, {args.exc_value}'
    if args.exc_type in (ValueError, TypeError):
        print(message)
    else:
        with open('custom_errors.txt', 'a') as file:
            print(message, file=file)


threading.excepthook = intercept
