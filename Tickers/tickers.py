import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Queue
from time import mktime, strptime
from typing import Sequence

import requests
from requests.cookies import RequestsCookieJar


class TickersInfo:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64)"
        }
        self.cookie: RequestsCookieJar | None = None
        self.crumb: str | None = None
        self.event: threading.Event = threading.Event()
        self.queue: queue.Queue[tuple[str, str] | None] = Queue()
        self.start_date: str | None = None
        self.end_date: str | None = None
        self.interval: str | None = None

    def executor(
            self,
            tickers: Sequence[str],
            *,
            start_date: str,
            end_date: str,
            interval: str = '1wk'
    ) -> None:
        if not isinstance(start_date, str) \
                or not isinstance(end_date, str) \
                or not isinstance(interval, str):
            raise Exception('Check arguments type')

        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        _writer = threading.Thread(target=self._write_to_file)
        _writer.start()
        with ThreadPoolExecutor(max_workers=len(tickers) + 1) as pool:
            pool.submit(self._get_crumb)
            for ticker in tickers:
                pool.submit(self._get_ticker_info, ticker=ticker)
        self.queue.put(None)
        _writer.join()

    def _get_crumb(self) -> None:
        """'Crumb' is not needed in this example;
        however, not all Yahoo Finance endpoints work without it.
        I left this just in case.

        Ref. https://cryptocointracker.com/yahoo-finance/yahoo-finance-api

        """
        self.cookie = requests.get(
            "https://fc.yahoo.com", headers=self.headers
        ).cookies
        get_crumb = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=self.headers,
            cookies=self.cookie
        )
        if get_crumb.ok:
            self.crumb = get_crumb.text
            self.event.set()
        else:
            raise Exception('Failed to receive a crumb')

    def _get_ticker_info(self, ticker: str) -> None:
        self.event.wait()
        params = {
            'crumb': self.crumb,
            'period1': self._convert_to_unix(self.start_date),
            'period2': self._convert_to_unix(self.end_date),
            'interval': self.interval
        }
        ticker_info = requests.get(
            f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}",
            headers=self.headers,
            cookies=self.cookie,
            params=params

        )
        if not ticker_info.ok:
            print(f'#Warning#  {ticker} {ticker_info.text.split(":")[-1]}')
        else:
            self.queue.put((ticker, ticker_info.text))

    def _write_to_file(self) -> None:
        if not Path('CSV').exists():
            Path('CSV').mkdir()
        while True:
            if (item := self.queue.get()) is None:
                break
            title, data = item
            with open(f'CSV/{title}.csv', 'w', newline='') as csvfile:
                csvfile.write(data)

    @staticmethod
    def _convert_to_unix(date: str) -> str:
        """Converts date to unix timestamp
            date - in format (dd-mm-yyyy)
            returns string of unix timestamp
        """
        return str(
            int(
                mktime(
                    strptime(date, '%d-%m-%Y')
                )
            )
        )


if __name__ == '__main__':
    tickers = 'AAPL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'GOOGL', 'META', 'BRK-B', 'UNH', 'JPM'
    t = TickersInfo()
    t.executor(tickers, start_date='01-01-2020', end_date='20-05-2024')
