from functools import lru_cache
from settings import FIBONACCI_CACHE_SIZE

@lru_cache(maxsize=FIBONACCI_CACHE_SIZE)
def calculate_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)