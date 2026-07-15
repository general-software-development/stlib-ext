import math
from functools import lru_cache
from functools import wraps
from typing import Optional, Any
from collections.abc import Callable
from moretyping.visualise import VisLink
from .pyexperimental import experimental

type MaxSize = int | bool

class CacheInfo:
    def __init__(self, hits: int, misses: int, maxsize: MaxSize, currsize: int) -> None:
        self.hits = hits
        self.misses = misses
        self.maxsize = maxsize
        self.currsize = currsize
        self.locked = False

    def lock(self) -> None:
        self.locked = True

    def __setattr__(self, name, value):
        if self.locked == False:
            self.__dict__[name] = value
        else:
            raise RuntimeError("Attempted to modify immutable object: CacheInfo")

# TODO: Implement cache_clear()
# TODO: Implement cache_info()
# TODO: Implement cache_entries()
@experimental
def fifo_cache(maxsize: Optional[MaxSize]) -> Callable[[Callable], Callable]:
    if isinstance(maxsize, bool):
        maxsize = math.inf if maxsize else 0

    def decorator(function: Callable):
        cache = {}
        cacheList = []  # TODO: Switch to deque

        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            key = VisLink((tuple(args), tuple(kwargs.items()))).string
            if key in set(cache.keys()):  # TODO: Remove set()
                return cache.get(key)
            
            value = function(*args, **kwargs)
            cacheList.append(key)
            cache[key] = value

            if len(cacheList) > maxsize:
                removalKey = cacheList.pop(0)
                cache.pop(removalKey)
                print(f"Removing key: {removalKey}")  # TODO: Remove debug print statements

            return value

        return wrapper
    
    return decorator
