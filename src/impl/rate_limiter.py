import time
import sys

if sys.platform == 'win32':
    ms_time = time.clock
else:
    ms_time = time.time


class RateLimiter(object):
    def __init__(self, calls_per_second):
        self._interval = 1.0 / calls_per_second
        self._last_call = 0

    def wait(self):
        time_since_last_call = ms_time() - self._last_call
        sleep_time = self._interval - time_since_last_call
        if sleep_time > 0.0:
            time.sleep(sleep_time)
        self._last_call = ms_time()
