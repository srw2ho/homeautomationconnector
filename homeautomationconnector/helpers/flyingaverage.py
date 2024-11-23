from threading import RLock
import numpy as np


class FlyingAverage(object):
    def __init__(self, stack_size: int):

        self._lock = RLock()
        self._stack_size = stack_size
        self.reset()

    def add(self, value: float):
        self._lock.acquire()
        self._stack[self._ptr] = value
        self._ptr += 1
        if self._ptr == len(self._stack):
            self._full_cycle = True
            self._ptr = 0
        self._lock.release()

    @property
    def stack_size(self):
        self._lock.acquire()
        size =  self._stack_size
        self._lock.release()
        return size

    @property
    @stack_size.setter
    def stack_size(self, value):
        self._lock.acquire()
        self._stack_size = value
        self.reset()
        self._lock.release()

    def reset(self):
        self._lock.acquire()
        self._stack = [0 for _ in range(self._stack_size)]
        self._ptr = 0
        self._full_cycle = False
        self._lock.release()

    # Mittelung der letzen stack_size Values
    def get_avg(self) -> float:
        ret = 0.0
        
        self._lock.acquire()
        
        if self._full_cycle:
            ret =  float(np.mean(a=self._stack, dtype=np.float64))
        else:
            ret = float(np.mean(a=self._stack[: self._ptr], dtype=np.float64))
        
        self._lock.release()
        return ret

    def get_values(self) -> list[float]:
        self._lock.acquire()
        
        ret = self._stack
        
        self._lock.release()
        return ret
