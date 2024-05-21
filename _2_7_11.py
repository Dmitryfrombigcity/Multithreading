from dataclasses import dataclass, field
from typing import Iterable, Any


@dataclass()
class _Special:
    item: str | int | bool

    def __post_init__(self) -> None:
        self._set = set(f'0{num}' for num in range(201, 210))

    def __lt__(self, other: object) -> bool:
        if isinstance(other, _Special):
            match self.item, other.item:
                case (bool(elem), bool(elem_2)) if elem is True \
                                                   and elem != elem_2:
                    return True
                case bool(), bool():
                    return False

                case (str(elem), str(elem_2)) if elem in self._set \
                                                 and elem_2 not in self._set:
                    return True
                case (str(), str()):
                    return False

                case int(elem), int(elem_2):
                    return int.__lt__(elem, elem_2)
                case _:
                    raise Exception('Comparison error')
        else:
            raise Exception('Comparison error')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _Special):
            match self.item, other.item:
                case (bool(elem), bool(elem_2)) if elem == elem_2:
                    return True
                case (str(elem), str(elem_2)) \
                    if self._set.issuperset((elem, elem_2)) \
                       or self._set.isdisjoint((elem, elem_2)):
                    return True
                case _:
                    return False
        else:
            raise Exception('Comparison error')


@dataclass(slots=True, order=True)
class CCD:
    union: bool = field(init=False, compare=False)
    cat: str = field(init=False, compare=False)
    id: int = field(init=False, compare=False)
    cargo: Iterable[Any] = field(init=False, compare=False)

    _union: _Special = field(init=False, repr=False)
    _cat: _Special = field(init=False, repr=False)
    _id: _Special = field(init=False, repr=False)
    _cargo: _Special = field(init=False, repr=False)

    _kwargs: dict[str, Any] = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        for key, value in self._kwargs.items():
            setattr(self, key, value)
            setattr(self, f'_{key}', _Special(value))


d1 = {"cat": "0210", "union": True, "cargo": {"stew", 2}, "id": 1}
d2 = {"cat": "0208", "union": True, "cargo": {"liver", 1.78}, "id": 2}
d3 = {"cat": "0208", "union": True, "cargo": {"liver", 56}, "id": 3}
d4 = {"cat": "0208", "union": False, "cargo": {"pork fat", 100}, "id": 14}
d5 = {"cat": "87", "union": True, "cargo": {"bombardier", 1}, "id": 5}
d6 = {"cat": "0201", "union": False, "cargo": {"veal", 120}, "id": 7}
d7 = {"cat": "0201", "union": False, "cargo": {"veal", 79}, "id": 6}

if __name__ == '__main__':
    dataset = (CCD(d) for d in (d1, d2, d3, d4, d5, d6, d7))
    print(*(ccd for ccd in sorted(dataset)), sep='\n')

    # 2 3 1 4 6 7 5
