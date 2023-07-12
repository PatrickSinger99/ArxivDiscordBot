import time
from functools import wraps


def info_print(func):
    @wraps(func)
    def info_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        print(f'{func.__name__}{args}{kwargs if len(kwargs) != 0 else ""} took {total_time:.4f} seconds')
        return result
    return info_wrapper
