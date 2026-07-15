from __future__ import annotations
from typing import Any

class VisualiseMeta(type):
    def __new__(mcls: type[VisualiseMeta], name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> "VisualiseMeta":
        def __repr__(self: Any) -> str:
            return f"<{type(self).__name__} object> {self.__str__()}"
        
        def __str__(self: Any) -> str:
            return str(self.string)

        namespace["__repr__"] = namespace.get("__repr__") or __repr__
        namespace["__str__"] = namespace.get("__str__") or __str__
        cls = super().__new__(mcls, name, bases, namespace)
        return cls
    