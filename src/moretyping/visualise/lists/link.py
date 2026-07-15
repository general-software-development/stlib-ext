from ..shared import VisualiseMeta
from typing import Any
from functools import cached_property
from collections.abc import Iterable

class VisLink(metaclass=VisualiseMeta):
    def __init__(self, data: list[Any]) -> None:
        self.data = tuple(data)

    @cached_property
    def strdata(self) -> Iterable[str]:
        return map(lambda x: str(x), self.data)

    @cached_property
    def string(self) -> str:
        return f"[ {" > ".join(self.strdata)} ]"
