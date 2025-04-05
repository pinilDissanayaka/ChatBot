# utils/helpers.py or similar
import asyncio
import concurrent.futures

def run_sync(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return loop.run_in_executor(pool, lambda: fn(*args, **kwargs))