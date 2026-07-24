from typing import Any
import warnings

def importDefaults(module: Any) -> dict[str, Any]:
    if not hasattr(module, "__defaults__"):
        return {}
    vals = {}
    for obj in module.__defaults__:
        if obj.__name__ in globals().keys():
            warnings.warn(f"Warning: importDefaults may overwrite globals()[{repr(obj.__name__)}]")
        vals[obj.__name__] = obj
    return vals

from . import cache
from . import pyexperimental as exp

globals().update(importDefaults(exp))

from .notimplemented import notimplemented, NotImplemented
