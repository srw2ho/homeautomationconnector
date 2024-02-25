
import numpy as np


class FlyingAverage(object):
    def __init__(self, stack_size: int):
        self._stack_size = stack_size
        self.reset()

    def add(self, value: float):
        self._stack[self._ptr] = value
        self._ptr += 1
        if self._ptr == len(self._stack):
            self._full_cycle = True
            self._ptr = 0


    @property
    def stack_size(self):
        return self._stack_size

    @property
    @stack_size.setter
    def stack_size(self, value):
        self._stack_size = value
        self.reset()

    def reset(self):
        self._stack = [0 for _ in range(self._stack_size)]
        self._ptr = 0
        self._full_cycle = False

    # Mittelung der letzen stack_size Values
    def get_avg(self):
        if self._full_cycle:
            return np.mean(a=self._stack, dtype=np.float64)
        else:
            return np.mean(a=self._stack[: self._ptr], dtype=np.float64)

    def get_values(self) -> list[float]:
        return self._stack
