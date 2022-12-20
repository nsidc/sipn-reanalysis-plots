from dataclasses import dataclass
from typing import TypedDict


class Variable(TypedDict):
    # short_name: str
    long_name: str
    levels: tuple[str] | tuple[str, str, str] | tuple[str, str, str, str]


@dataclass
class YearMonth:
    year: int
    month: int

    def __str__(self):
        return f'{self.year}{self.month:02}'
