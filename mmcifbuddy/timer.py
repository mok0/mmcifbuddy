import time

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self, verbose=True):
        self._start_time = None
        self.elapsed_time = 0
        self.lap_time = 0
        self.verbose = verbose


    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()
        self.lap_time = time.perf_counter()
        self.elapsed_time = 0

    def lap(self):
        """Take a lap time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        #.
        self.lap_time = time.perf_counter() - self.lap_time
        print(f"Elapsed time: {self.lap_time:0.4f} seconds")
        self.lap_time = time.perf_counter()


    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        #.
        ##elapsed_time = time.perf_counter() - self._start_time
        self.elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        if self.verbose:
            print(f"Elapsed time: {self.elapsed_time:0.4f} seconds")
