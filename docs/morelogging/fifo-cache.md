# morefunctools.experimental

## Annotations

```python
@overload
def fifo_cache(function: Callable) -> Callable:
    ...

@overload
def fifo_cache(maxsize: MaxSize = True) -> Callable[[Callable], Callable]:
    ...
```

## Parameters

`maxsize: MaxSize = True`
: If an integer, then `maxsize` is the maximum number of cache entries.
: If `True`, then the number of cache entries is unlimited.
: If `False`, then the number of cache entries is `1`.

## Return Value

*N/A*

## Raises

*N/A*

## Details

When applying `@fifo_cache()` to a function, you can use `fn.cache_clear()`, `fn.cache_info`, `fn.cache_entries`, with the following signatures:

```py
def cache_clear() -> None:
    ...

def cache_info() -> CacheInfo:  # has .hits, .misses, .maxsize, .currsize; is immutable
    ...

def cache_entries() -> tuple[*tuple[Any, Any]]:
    ...
```

## Example usage

```python
from morefunctools.cache import fifo_cache

@fifo_cache()
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)  # Uncached -> 3
add(1, 2)  # Cached   -> 3
add(1, 3)  # Uncached -> 4

add.cache_clear()
add(1, 2)  # Uncached -> 3

info = add.cache_info()
info.hits     # 1
info.misses   # 3
info.maxsize  # math.inf
info.currsize # 0
print(info)   # CacheInfo(hits=1, misses=3, maxsize=inf, currsize=0)

add(1, 2)
entries = add.cache_entries()
entries  # (('[ (1, 2) > () ]', 3),)
```
