from ..shared import VisualiseMeta
from functools import cached_property
from typing import Any, Optional
import json

class ViewJSON(metaclass=VisualiseMeta):
    def __init__(self, data: Optional[Any] = {}) -> None:
        self.data = data

    @cached_property
    def string(self) -> str:
        return json.dumps(self.data, indent = 4)
