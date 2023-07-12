import time
from functools import wraps


def info_print(text):
    def decorate(func):
        @wraps(func)
        def info_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            print(f"{text}...", end="")
            result = func(*args, **kwargs)
            total_time = time.perf_counter() - start_time
            print(f'done ({total_time:.2f} sec).')
            return result
        return info_wrapper
    return decorate
