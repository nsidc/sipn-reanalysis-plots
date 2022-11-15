from typing import TypedDict


class Variable(TypedDict):
    # short_name: str
    long_name: str
    levels: tuple[str] | tuple[str, str, str] | tuple[str, str, str, str]
