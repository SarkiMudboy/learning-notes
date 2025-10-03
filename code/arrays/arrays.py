# This contains code to different concepts I'm studying on Array Based Sequences
import sys
from array import array
import ctypes
from typing import Any, List, Dict, Optional
from time import time
import random
import math


def test_size_of_list(n: int) -> None:
    """
    Prints the list length and its memory size while repeatedly appending elements to demonstrate Python list growth behavior.
    
    Runs for `n` iterations starting from a small list; on each iteration it prints the current length and the result of `sys.getsizeof` for the list.
    """

    data = [None, None, None, None, None, None, None]
    for _ in range(n):
        length = len(data)
        s = sys.getsizeof(data)
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, s))
        data.append(None)


"""
empty array = []
Length:   0; Size in bytes:   56
Length:   1; Size in bytes:   88
Length:   2; Size in bytes:   88
Length:   3; Size in bytes:   88
Length:   4; Size in bytes:   88
Length:   5; Size in bytes:  120
Length:   6; Size in bytes:  120
Length:   7; Size in bytes:  120
Length:   8; Size in bytes:  120
Length:   9; Size in bytes:  184
------------------------------------
3-item array 

Length:   3; Size in bytes:   88
Length:   4; Size in bytes:   88
Length:   5; Size in bytes:  120
Length:   6; Size in bytes:  120
Length:   7; Size in bytes:  120
Length:   8; Size in bytes:  120
Length:   9; Size in bytes:  184
Length:  10; Size in bytes:  184
Length:  11; Size in bytes:  184
Length:  12; Size in bytes:  184
----------------------------------

104 - 

5-item array 
Length:   0; Size in bytes:  56
Length:   1; Size in bytes:  104
Length:   2; Size in bytes:  104
Length:   3; Size in bytes:  104
Length:   4; Size in bytes:  104


Length:   5; Size in bytes:  104
Length:   6; Size in bytes:  104
Length:   7; Size in bytes:  152
Length:   8; Size in bytes:  152
Length:   9; Size in bytes:  152
Length:  10; Size in bytes:  152
Length:  11; Size in bytes:  152
Length:  12; Size in bytes:  152
Length:  13; Size in bytes:  216
Length:  14; Size in bytes:  216
Length:  15; Size in bytes:  216
Length:  16; Size in bytes:  216
Length:  17; Size in bytes:  216
Length:  18; Size in bytes:  216
Length:  19; Size in bytes:  216
Length:  20; Size in bytes:  216
Length:  21; Size in bytes:  280
Length:  22; Size in bytes:  280
Length:  23; Size in bytes:  280
Length:  24; Size in bytes:  280
Length:  25; Size in bytes:  280
Length:  26; Size in bytes:  280

"""


# if __name__ == "__main__":
#
#     test_size_of_list(27)


def test_size_limits(n: int) -> None:
    data = []
    init_size = sys.getsizeof(data)
    prev_size = init_size
    idx = 0
    index = 0
    for _ in range(n):
        length = len(data)
        s = sys.getsizeof(data)
        if s != prev_size:
            idx = (s - init_size) / 8
        if index == idx:
            print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, s))
        data.append(None)
        index += 1


def test_list_shrinkage(n: int) -> None:
    """
    Modify the experiment from Code Fragment 5.1 in order to demonstrate
    that Python’s list class occasionally shrinks the size of its underlying array
    when elements are popped from a list.
    """
    init_list = [None] * n

    for _ in range(n + 1):
        length = len(init_list)
        size = sys.getsizeof(init_list)
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, size))
        if length > 0:
            init_list.pop()


def test_size_of_array(n: int) -> None:
    """Similar experiment for low-level arrays"""
    # args: n -> Length of array

    data = array("i", [])
    for _ in range(n):
        length = len(data)
        s = sys.getsizeof(data)
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, s))
        data.append(0)


# test_size_of_array(20)


class DynamicArray1:
    """An implementation of dynamic array similar to the python list"""

    def __init__(self) -> None:
        self._n = 0
        self._capacity = 1
        self._A = self._make_array(self._capacity)

    def __len__(self) -> int:
        return self._n

    def __getitem__(self, k: int) -> Any:  # change this type to generic?
        index = k
        if k < 0:
            index = self._n - abs(k)
        if not 0 <= index < self._n:
            raise IndexError("Array index out if range")

        return self._A[index]

    def append(self, obj: Any) -> None:
        """
        If there is no space for the new obj:
        1. Allocate a new array B with larger capacity.
        2. Set B[i] = A[i], for i = 0, . . . , n − 1, where n denotes current number of items.
        3. Set A = B, that is, we henceforth use B as the array supporting the list.
        4. Insert the new element in the new array.
        """

        if self._n == self._capacity:
            self._resize(2 * self._capacity)

        self._A[self._n] = obj
        self._n += 1

    def insert(self, k: int, val: int) -> None:
        """Insert a value at index k. k is of the range 0 <= k <= n"""
        if self._n == self._capacity:
            self._resize(self._capacity * 2, k)
        else:
            for j in range(self._n, k, -1):
                self._A[j] = self._A[j - 1]

        self._A[k] = val
        self._n += 1

    def _resize(self, capacity: int, shift_loc: Optional[int] = None) -> None:
        B = self._make_array(capacity)

        for j in range(self._n):
            if shift_loc and j >= shift_loc:
                B[j + 1] = self._A[j]
            else:
                B[j] = self._A[j]
        self._A = B
        self._capacity = capacity

    def _make_array(self, capacity: int) -> ctypes.py_object:
        return (ctypes.py_object * capacity)()

    def get_array(self):
        return self._A

    def stats(self) -> Dict[str, Any]:
        return {
            "length": self._n,
            "cap": self._capacity,
        }

    def __str__(self) -> str:
        "string representation of the underlying array"
        array = [None] * self._n
        try:
            for i in range(self._n):
                array[i] = str(self._A[i])
        except ValueError:
            pass

        return ", ".join(array)


def safe_loop(d: ctypes.py_object) -> None:
    try:
        for i in d:
            print(i)
    except ValueError:
        pass


def log_array():
    d = DynamicArray1()
    for _ in range(50):
        d.append(None)
    safe_loop(d)
    print(sys.getsizeof(d.get_array()))


def test_size_of_d_array(n: int) -> None:
    """Similar experiment for the custom dynamic array"""
    # args: n -> Length of array

    data = DynamicArray1()
    for _ in range(n):
        length = len(data)
        s = sys.getsizeof(data.get_array())
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, s))
        data.append(0)


def InsertionSort(A: list) -> list:
    """Sort list of comparable elements into increasing order"""
    for k in range(1, len(A)):
        curr = A[k]
        j = k
        while j > 0 and A[j - 1] > curr:
            A[j] = A[j - 1]
            j -= 1
        A[j] = curr
    return A


# print(InsertionSort([4, 6, 8, 1, 9, 0, 1, 5]))


class CaesarCipher:
    """Implementation for the oldest crypto scheme - Caesar cipher"""

    def __init__(self, shift: int) -> None:

        self._forwards = "".join(
            [chr(((c + shift) % 26) + ord("A")) for c in range(26)]
        )
        self._backwards = "".join(
            [chr(((c - shift) % 26) + ord("A")) for c in range(26)]
        )

        print("Characters (encoding): ", self._forwards)
        print("Characters (decoding): ", self._backwards)

    def encrypt(self, message: str) -> str:
        return self._transform(message, self._forwards)

    def decrypt(self, secret: str) -> str:
        return self._transform(secret, self._backwards)

    def _transform(self, text: str, code: str) -> str:
        msg = list(text)
        for k in range(len(msg)):
            if msg[k].isupper():
                j = ord(msg[k]) - ord("A")
                msg[k] = code[j]

        return "".join(msg)


class CaesarCipherUTF:
    """Implementation for the oldest crypto scheme - Caesar cipher for any charcter set in the UTF-8 charset"""

    def __init__(self, shift: int, first_letter: str, size: int) -> None:
        encoder = [None] * size
        decoder = [None] * size

        for c in range(size):
            encoder[c] = chr(((c + shift) % size) + ord(first_letter))
            decoder[c] = chr(((c - shift) % size) + ord(first_letter))

        self._forwards = "".join(encoder)
        self._backwards = "".join(decoder)
        print("Characters (encoding): ", self._forwards)
        print("Characters (decoding): ", self._backwards)

    def encrypt(self, message: str) -> str:
        return self._transform(message, self._forwards)

    def decrypt(self, secret: str) -> str:
        return self._transform(secret, self._backwards)

    def _transform(self, text: str, code: str) -> str:
        msg = list(text)
        for k in range(len(msg)):
            j = ord(msg[k]) - ord("α")
            msg[k] = code[j]

        return "".join(msg)


# if __name__ == "__main__":
#     cipherEnglish = CaesarCipher(3)
#     plaintext = "THE EAGLE IS IN PLAY; MEET AT JOE S."
#     ciphertext = cipherEnglish.encrypt(plaintext)
#     print(f"Text: {plaintext}\nsecret: {ciphertext}")
#     d = cipherEnglish.decrypt(ciphertext)
#
#     print(f"decrypted: {d}")
#
# cipherUTF = CaesarCipherUTF(3, "α", 25)
# plaintext = "ρθε"
# ciphertext = cipherUTF.encrypt(plaintext)
#
# print(f"Text: {plaintext}\nsecret: {ciphertext}")


#  the first letter of the lang
# how many characters are in the chrset
# shift as usual


def find_duplicate(S: List[int]) -> Optional[int]:
    count = 0
    for n in range(0, len(S)):
        for i in range(n + 1, len(S)):
            count += 1
            if S[n] == S[i]:
                print(count)
                return S[n]
    print(count)
    return None


def find_cycle(A: List):
    """
    Cycle Detection (Floyd’s Tortoise and Hare) Algorithm:
    A fast algorithm for finding the integer in A that is repeated in an
    array of size n ≥ 2 containing  integers from 1 to n − 1, inclusive.
    Time complexity = O(n) single scan
    Space complexity = O(1) only storing pointers
    see https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
    """
    # create two pointers
    slow = A[0]
    fast = A[0]

    # phase 1: Detect cycle (like in linked list)
    while True:
        slow = A[slow]
        fast = A[A[fast]]
        print(slow, fast)

        if slow == fast:
            break

    # phase 2: find entrance into the cycle (i.e repeated number)
    slow = A[0]
    while slow != fast:
        slow = A[slow]
        fast = A[fast]
        print(slow, fast)

    lam = 1
    fast = A[slow]
    while slow != fast:
        fast = A[fast]
        lam += 1

    print(lam)
    return slow


def compute_average():

    sizes = [10, 100, 1000, 10_000]

    for size in sizes:

        indices = [0, size // 2, size - 1]

        array = [None] * size

        for k in indices:

            loop_array = array[:]

            start = time()

            for i in range(size):

                try:

                    loop_array.pop(k)

                except IndexError:

                    break

            end = time()

            av = (end - start) / size

            print(
                f"Array length = {size}, index popped = {k}, Average time per pop op = {av * 1000}"
            )


def array_sum2(data: list):
    """
    built-in sum function can be combined with Python’s
    comprehension syntax to compute the sum of all numbers in an n × n data
    set, represented as a list of lists.
    """
    if isinstance(data, list):
        return sum([array_sum2(data[i]) for i in range(len(data))])
    else:
        return data


def arraySum(data: list):

    total = (
        sum([arraySum(data[i]) for i in range(2)])
        if isinstance(data, list)
        else sum([i for i in data])
    )
    return total


def array_sum(data: list) -> int:
    """
    Using standard control structures to compute the sum of all numbers in an
    n × n data set, represented as a list of lists.
    """
    total = 0

    for i in range(len(data)):
        if isinstance(data[i], int):
            total += data[i]
        elif isinstance(data[i], list):
            total += array_sum2(data[i])
        else:
            raise ValueError("invalid input")

    return total


def shuffle(data: List[Any]) -> List[Any]:
    """Custom shuffle function that rearranges a list so that every possible ordering is equally likely."""
    index = 0
    shuffled_data = [None for _ in range(len(data))]

    while index < len(shuffled_data):

        i = random.randrange(0, len(data))

        if data[i] not in shuffled_data:
            shuffled_data[index] = data[i]
            index += 1

    return shuffled_data


class DynamicArray2:
    """

    Consider an implementation of a dynamic array, but instead of copying
    the elements into an array of double the size (that is, from N to 2N) when
    its capacity is reached, we copy the elements into an array with N/4
    additional cells, going from capacity N to capacity N + N/4

    """

    def __init__(self):

        """
        Initialize an empty dynamic array with zero elements and an initial capacity of 1.
        """
        self._n = 0  # count
        self._capacity = 1  # cap
        self._A = self._make_array(self._capacity)

    def __len__(self) -> int:
        return self._n

    def append(self, obj: Any) -> None:

        """
        Append an element to the end of the dynamic array.
        
        Inserts the given object at the next available index and increments the element count. If the backing storage is full, the array's capacity is increased (by roughly 25%) before insertion.
        """
        if self._n == self._capacity:
            self._resize(self._capacity + math.ceil(self._capacity / 4))
        self._A[self._n] = obj
        self._n += 1

    def __getitem__(self, k: int) -> Any:

        if not 0 <= k < self._n:
            raise IndexError("Index out of range")

        return self._A[k]

    def _resize(self, c: int) -> None:

        """
        Resize the internal backing array to the specified capacity while preserving existing elements.
        
        Parameters:
            c (int): New capacity for the backing array; must be at least the current number of elements.
        
        Detailed behavior:
            Allocates a new underlying array of size `c`, copies all current elements from the old array into the new one, and updates the internal reference and capacity.
        """
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    def get_array(self):
        """
        Return the underlying ctypes-backed array used as the backing storage.
        
        Returns:
            The internal ctypes array object (the backing storage for this dynamic array).
        """
        return self._A

    def _make_array(self, capacity: int) -> ctypes.py_object:
        """
        Create a new low-level ctypes array for storing Python objects with the given capacity.
        
        Parameters:
            capacity (int): Number of slots to allocate in the array.
        
        Returns:
            ctypes.py_object: A newly allocated ctypes array of length `capacity` suitable for storing Python objects.
        """
        return (ctypes.py_object * capacity)()


def test_size_of_d2_array(n: int) -> None:

    """
    Measure and print memory usage of a DynamicArray2 instance while appending items.
    
    Runs n iterations; before each append it prints the current length, capacity,
    size in bytes of the underlying ctypes array, and the total estimated size
    (object plus array).
    
    Parameters:
        n (int): Number of iterations / append operations to perform.
    """
    data = DynamicArray2()
    for _ in range(n):
        length = len(data)
        # Size of the object itself
        obj_size = sys.getsizeof(data)
        # Size of the underlying ctypes array
        array_size = sys.getsizeof(ctypes.py_object) * data._capacity
        total_size = obj_size + array_size

        print(
            "Length: {0:3d}; Capacity: {1:3d}; Array bytes: {2:4d}; Total bytes: {3:5d}".format(
                length, data._capacity, array_size, total_size
            )
        )
        data.append(None)


class DynamicArray3:

    def __init__(self):

        """
        Initialize an empty dynamic array with an initial capacity of 1.
        
        Sets the element count to 0, the internal capacity to 1, and allocates the backing ctypes array via `_make_array`.
        """
        self._n = 0
        self._capacity = 1
        self._A = self._make_array(self._capacity)

    def __len__(self) -> int:
        """
        Get the number of elements currently stored in the dynamic array.
        
        Returns:
            int: Number of elements in the array.
        """
        return self._n

    def __getitem__(self, k) -> any:

        """
        Return the element at position k from the dynamic array.
        
        Parameters:
            k (int): Zero-based index of the element to retrieve.
        
        Returns:
            any: The element stored at index k.
        
        Raises:
            IndexError: If k is not between 0 and self._n - 1.
        """
        if not 0 <= k < self._n:
            raise IndexError("Index out of range")

        return self._A[k]

    def append(self, obj: any):

        """
        Append an element to the end of the dynamic array, resizing the backing store if necessary.
        
        Parameters:
            obj (any): Element to append.
        """
        if self._n == self._capacity:
            self._resize(2 * self._capacity)

        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c: int) -> None:

        """
        Resize the instance's backing array to the given capacity.
        
        Parameters:
            c (int): New capacity (number of element slots). Must be greater than or equal to the current number of elements.
        
        Description:
            Allocates a new underlying array with capacity `c`, copies existing elements into it, and updates the instance's backing array and capacity.
        """
        B = self._make_array(c)

        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    def _make_array(self, capacity: int) -> ctypes.py_object:
        """
        Create a new low-level ctypes array for storing Python objects with the given capacity.
        
        Parameters:
            capacity (int): Number of slots to allocate in the array.
        
        Returns:
            ctypes.py_object: A newly allocated ctypes array of length `capacity` suitable for storing Python objects.
        """
        return (ctypes.py_object * capacity)()

    def pop(self) -> any:
        """
        Remove and return the last element, shrinking internal capacity when sparsely populated.
        
        If the number of stored elements falls below one quarter of the current capacity, the capacity is reduced by half before removing the last element.
        
        Returns:
            The element that was removed from the end of the array.
        
        Raises:
            IndexError: If the array is empty.
        """

        if self._n < self._capacity // 4:
            self._resize(self._capacity // 2)

        obj = self._A.pop()
        self._n -= 1
        return obj


if __name__ == "__main__":

    test_size_of_d2_array(20)
