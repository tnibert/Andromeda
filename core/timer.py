from events import EVT_TIMEOUT
from core.observe import Observable
import time


class Timer(Observable):
    """
    todo: use monotonic clock
    """
    def __init__(self, owner=None):
        """

        :param owner: An optional Observable to send the timeout event from
        """
        Observable.__init__(self)

        # for general tick
        # this must be initialized on the first tick
        # otherwise, the first tick diff will be the time between init and scene attachment
        self.prevtime = None

        # for stopwatch timing
        self.start = None
        self.threshold = None
        if owner is not None:
            self.owner = owner
        else:
            self.owner = self

    def startwatch(self, seconds):
        self.start = time.time()
        self.threshold = seconds

    def stopwatch(self):
        self.start = None
        self.threshold = None
        # todo: return diff

    def is_timing(self):
        """
        Check if timer is currently running
        :return: boolean, True if startwatch() has been called and timeout has not yet been reached
        """
        return self.start is not None and self.threshold is not None

    def tick(self):
        # if this is the first tick, initialize the last tick
        if self.prevtime is None:
            self.prevtime = time.time()

        curtime = time.time()

        diff = curtime - self.prevtime
        self.prevtime = curtime

        # if stop watch is running
        if self.start:
            if (curtime - self.start) > self.threshold:
                # allows the callback to start another timer
                self.stopwatch()
                self.owner.notify(EVT_TIMEOUT)

        self.notify("tick", diff=diff)
        return diff
