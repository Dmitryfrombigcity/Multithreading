import threading
from _thread import _ExceptHookArgs


class NoTargetException(Exception):
    ...


def custom_hook(args: _ExceptHookArgs) -> None:
    print(f'{args.thread.name} '
          f'(id={args.thread.ident}) failed')


threading.excepthook = custom_hook


class MyThread(threading.Thread):
    def __init__(
            self,
            target=None,
            result=None
    ) -> None:
        super().__init__()
        self.target = target
        self.result = result

    def run(self) -> None:
        if not self.target:
            raise NoTargetException(threading.current_thread().name)
        self.result = self.target()
