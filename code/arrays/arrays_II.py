from typing import List, Any, Optional
from arrays import DynamicArray3
from time import time
import sys
import ctypes

def test_size(n: int):

    data = DynamicArray3()
    for _ in range(n):
        length = len(data)
        # Size of the object itself
        obj_size = sys.getsizeof(data)
        # Size of the underlying ctypes array
        array_size = ctypes.sizeof(data._A)
        total_size = obj_size + array_size

        print(
            "Length: {0:3d}; Capacity: {1:3d}; Array bytes: {2:4d}; Total bytes: {3:5d}".format(
                length, data._capacity, array_size, total_size
            )
        )
        data.append(None)

    for _ in range(n):

        length = len(data)

        obj_size = sys.getsizeof(data)
        array_size = ctypes.sizeof(data._A)
    
        total_size = array_size + obj_size

        print(
            "Length: {0:3d}; Capacity: {1:3d}; Array bytes: {2:4d}; Total bytes: {3:5d}".format(
                length, data._capacity, array_size, total_size
            )
        )
        data.pop()


def concat(n: int) -> float:
    
    string = ''

    start = time()
    for _ in range(n):
        string += 'a'
    end = time()

    return (end - start) * 1000


def append(n: int) -> float:

    temp = []
    start = time()
    for _ in range(n):
        temp.append('a')
    end = time()
    
    # ''.join(temp)

    return (end - start) * 1000

def comprehension(n: int) -> float:

    start = time()
    string = ''.join(['a' for _ in range(n)])
    end = time()

    return (end - start) * 1000

def comprehension_generator(n: int) -> float:

    start = time()
    string = ''.join('a' for _ in range(n))
    end = time()

    return (end - start) * 1000


def extend(array1: List[Any], array2: List[Any]) -> float:

    """
    Concats array1 with array2 using the built-in extend list method. 
    Records the time elapsed for the operation
    params:
        array1: List[any] -> array to concat
        array2: List[any] -> array to concat with
    returns:
        duration; float -> time taken to concat.
    """

    start = time()
    array1.extend(array2)
    end = time()

    return (end - start) * 100


def appendArray(array1: List[Any], array2: List[Any]) -> float:
    """
    Concats array1 with array2 using a for loop and repeated calls to the built-in append method. 
    Records the time elapsed for the operation
    params:
        array1: List[any] -> array to concat
        array2: List[any] -> array to concat with
    returns:
        duration; float -> time taken to concat.
    """
    start = time()
    for item in array2:
        array1.append(item)
    end = time()

    return (end - start) * 1000


def experiment(description: str, funcs: list, runs: int=3, *args, **kwargs):
    """Wrapper function for array based sequences experiments"""
    
    print(description)

    duration = {f.__name__: 0 for f in funcs}

    for f in funcs:
        d = []
        for _ in range(runs):
            d.append(f(*args, **kwargs))

        duration[f.__name__] = sum(d)/len(d)

    print('\n'.join([f'{k}: {duration[k]}' for k in duration.keys()]))


def construct_array_loop(n: int) -> float:

    """
    Constructs a new list size n using a repeated call to `append`
    params:
        n: size of the final array
    returns:
        duration: time elapsed for loop
    """

    array = []
    start = time()
    for k in range(n):
        array.append(0)
    end = time()

    return (end - start) * 1000

def construct_array_multiply(n: int) -> float:

    """
    Constructs a new list size n using element mul
    params:
        n: size of the final array
    returns:
        duration: time elapsed for operation
    """

    start = time()
    final = [0] * n
    end = time()

    return (end - start) * 1000


def construct_array_comprehension(n: int) -> float:
    """
    Constructs a new list size n using list comprehension syntax
    params:
        n: size of the final array
    returns:
        duration: time elapsed for operation
    """

    start = time()
    final = [0 for _ in range(n)]
    end = time()

    return (end - start) * 1000


def do_experiments():

    d = """
    In Section 5.4.2, we described four different ways to compose a long
    string: (1) repeated concatenation, (2) appending to a temporary list and
    then joining, (3) using list comprehension with join, and (4) using genera-
    tor comprehension with join. Develop an experiment to test the efficiency
    of all four of these approaches and report your findings.\n
    """
    fs = [comprehension_generator, append, comprehension, concat]
    # experiment(d, fs, 10, n=1_000_000)

    print("\n")
    
    d = """
    C-5.22 Develop an experiment to compare the relative efficiency of the extend
    method of Python’s list class versus using repeated calls to append to
    accomplish the equivalent task.\n
    """
    fs = [extend, appendArray]
    # experiment(d, fs, 3, array1=[None], array2=[None] * 1_000_000)

    d = """
    Based on the discussion of page 207, develop an experiment to compare
    the efficiency of Python’s list comprehension syntax versus the construc-
    tion of a list by means of repeated calls to append.\n
    """

    fs = [construct_array_loop, construct_array_comprehension, construct_array_multiply]
    experiment(d, fs, 3, n=1_000_000)


def compute_average():

    size = 1_000_000
    run_set = ["10", "100", "1000", "10000", "100000"]
    data = [n for n in range(size)]
    
    # print("start of an array")
    # for runs in run_set:

    #     N = int(runs)

    #     d1 = data[:]

    #     start = time()
    #     for i in range(N):
    #         d1.remove(i)
    #     end = time()

    #     av = ((end - start) / N) * 1000
    #     print(f"{runs}: {av}")

    print("\nmiddle of an array\n")
    for runs in run_set:

        N = int(runs)
        d1 = data[:]
        k = size//2
        
        start = time()
        for i in range(N):
            d1.remove(k)
            k+=1
        end = time()

        av = ((end - start) / N) * 1000
        print(f"{runs}: {av}")

    print("\nend of an array\n")
    for runs in run_set:

        N = int(runs)
        d1 = data[:]
        k = size-1
        
        start = time()
        for i in range(N):
            d1.remove(k)
            k-=1
        end = time()

        av = ((end - start) / N) * 1000
        print(f"{runs}: {av}")

if __name__ == "__main__":
    compute_average()