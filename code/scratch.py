import functools
import math
import time


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        # begin measuring delay
        start = time.perf_counter()
        values = func(*args, **kwargs)
        stop = time.perf_counter()
        delay = stop - start
        print(f"Ran {func.__name__}() in {delay} secs")

        return values

    return wrapper_timer


@timer
def waste(n: int):
    for i in range(n):
        sum([number**2 for number in range(10_000)])


# waste(99)


def debug(func):
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        arg_sig = [repr(arg) for arg in args]
        kwargs_sig = [f"{k}: {repr(v)}" for k, v in kwargs.items()]
        signature = ", ".join(arg_sig + kwargs_sig)
        print(f"Calling {func.__name__}({signature})")
        values = func(*args, **kwargs)
        print(f"{func.__name__}() returned {repr(values)}")
        return values

    return wrapper_debug


fac = debug(math.factorial)


def approx_e(terms=19):
    return sum([(1 / fac(n)) for n in range(terms)])


class Square:

    def __init__(self, length: int):
        self.length = length

    @debug
    def area(self, unit: str):
        return str(self.length**2) + " " + unit


if __name__ == "__main__":
    s = Square(5)
    print(s.area("m^2"))


@debug
def find_log(n: int):
    """Find the log to base 2 of a given number n"""

    if n <= 1.0:
        return 0
    else:
        return 1 + find_log(n // 2)


# n = find_log(256)
# print(approx_e())


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        """Get value of radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set radius, raise error if negative"""
        print("setter called")
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("radius must be non-negative")

    @property
    def area(self):
        """Calculate area inside circle"""
        return self.pi() * self.radius**2

    def cylinder_volume(self, height):
        """Calculate volume of cylinder with circle as base"""
        return self.area * height

    @classmethod
    def unit_circle(cls):
        """Factory method creating a circle with radius 1"""
        return cls(1)

    @staticmethod
    def pi():
        """Value of π, could use math.pi instead though"""
        return 3.1415926535


@timer
class TimeWaster:
    # @debug
    def __init__(self, duration: int) -> None:
        self.duration = duration

    # @timer
    def waste_time(self):
        for i in range(self.duration):
            sum([number**2 for number in range(10_000)])


def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        # print("dt getting called")
        func(*args, **kwargs)
        value = func(*args, **kwargs)
        return value

    return wrapper_do_twice


def repeat(_func=None, *, num_times=2):
    """Puts num_times in namespace or closure for use later"""

    def decorate_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result

        return wrapper_repeat

    if _func is None:
        print("return func")
        return decorate_repeat
    else:
        print("return decorated func")
        return decorate_repeat(_func)
    return decorate_repeat


def call_count(func):
    @functools.wraps(func)
    def wrapper_call_count(*args, **kwargs):
        wrapper_call_count.num_calls += 1
        print(f"Call {wrapper_call_count.num_calls} of {func.__name__}")
        result = func(*args, **kwargs)
        return result

    wrapper_call_count.num_calls = 0
    return wrapper_call_count


# @debug
@repeat
@call_count
def say_hello(name):
    print(f"Hey {name}")
