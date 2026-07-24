import math
from functools import lru_cache
from functools import wraps
from typing import Any, overload
from collections.abc import Callable
from moretyping.meta import Unknown
from .pyexperimental import experimental
from collections import deque
import warnings

type MaxSize = int | bool | float

class CacheInfo:
    def __init__(self, *, hits: int, misses: int, maxsize: MaxSize, currsize: int) -> None:
        self.__dict__["locked"] = False
        self.hits = hits
        self.misses = misses
        self.maxsize = maxsize
        self.currsize = currsize

    def lock(self) -> None:
        self.locked = True

    def __setattr__(self, name: str, value: Unknown) -> None:
        if self.locked == False:
            self.__dict__[name] = value
        else:
            raise RuntimeError("Attempted to modify immutable object: CacheInfo")
        
    def __str__(self) -> str:
        return f"CacheInfo(hits={self.hits}, misses={self.misses}, maxsize={self.maxsize}, currsize={self.currsize})"

@overload
def fifo_cache(function: Callable) -> Callable:
    ...

@overload
def fifo_cache(maxsize: MaxSize = True) -> Callable[[Callable], Callable]:
    ...

@experimental
def fifo_cache(maxsize: MaxSize | Callable = True) -> Callable[[Callable], Callable]:
    if isinstance(maxsize, bool):
        maxsize = math.inf if maxsize else 1

    realmaxsize: int | float
    if maxsize == True:
        realmaxsize = math.inf
    elif callable(maxsize):
        realmaxsize = math.inf
    else:
        realmaxsize = int(maxsize)
    if isinstance(maxsize, int) and maxsize <= 0:
        warnings.warn(f"Invalid fifo_cache maxsize: {maxsize}")
    

    def decorator(function: Callable) -> Callable:
        cache: dict[str, Any] = {}
        cacheList: deque = deque()

        hits, misses = 0, 0

        def cache_clear() -> None:
            nonlocal cache, cacheList
            cache = {}
            cacheList = deque()

        def cache_info() -> CacheInfo:
            info = CacheInfo(hits = hits, misses = misses, maxsize = realmaxsize, currsize = len(cache.keys()))
            info.lock()
            return info
        
        def cache_entries() -> tuple[tuple[Any, Any], ...]:
            return tuple(cache.items())

        @wraps(function)
        def wrapper(*args: Unknown, **kwargs: Unknown) -> Any:
            nonlocal hits, misses
            key = str((args, tuple(kwargs.items())))
            if key in cache.keys():
                hits += 1
                return cache.get(key)
            
            misses += 1
            
            value = function(*args, **kwargs)
            cacheList.append(key)
            cache[key] = value

            # Remove cache items to reduce size usage
            if len(cacheList) > realmaxsize:
                removalKey = cacheList.popleft()
                cache.pop(removalKey)

            return value
        
        setattr(wrapper, "cache_clear", cache_clear)
        setattr(wrapper, "cache_info", cache_info)
        setattr(wrapper, "cache_entries", cache_entries)

        return wrapper
    
    if callable(maxsize):
        return decorator(maxsize)  # in case of @fifo_cache instead of @fifo_cache()
    
    return decorator
