# This contains code to different concepts I'm studying on Array Based Sequences
import sys
from array import array
import ctypes
from typing import Any, List, Dict, Optional


def test_size_of_list(n: int) -> None:
    """Experiment to provide empirical evidence that Python’s list class is
    based upon such a strategy of dynamic arrays
    args: n -> Length of array"""

    data = []
    for _ in range(n):
        length = len(data)
        s = sys.getsizeof(data)
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, s))
        data.append(None)


if __name__ == "__main__":
    test_size_of_list(20)


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

    init_list = [None] * n

    for _ in range(n + 1):
        length = len(init_list)
        size = sys.getsizeof(init_list)
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, size))
        if length > 0:
            init_list.pop()


# if __name__ == "__main__":

# test_size_of_list(20)
# test_size_limits(20)
# test_list_shrinkage(30)


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


class DynamicArray:
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


# if __name__ == "__main__":
#
# d = DynamicArray()
# for i in range(10):
#     d.append(i)
# arr = d.get_array()
#
# start = 55
# print(d.stats())
# print(d)
# # print("\n")
#
# for x in range(20):
#     d.insert(2, start)
#     start += 1
#
# print(d.stats())
# print(d)


def test_size_of_d_array(n: int) -> None:
    """Similar experiment for the custom dynamic array"""
    # args: n -> Length of array

    data = DynamicArray()
    for _ in range(n):
        length = len(data)
        s = sys.getsizeof(data.get_array())
        print("Length: {0:3d}; Size in bytes: {1:4d}".format(length, s))
        data.append(0)


# test_size_of_d_array(20)


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
        encoder = [None] * 26
        decoder = [None] * 26

        for c in range(26):
            encoder[c] = chr(((c + shift) % 26) + ord("A"))
            decoder[c] = chr(((c - shift) % 26) + ord("A"))

        self._forwards = "".join(encoder)
        self._backwards = "".join(decoder)

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


# if __name__ == "__main__":
#
#     cipher = CaesarCipher(3)
#     message = "THIS IS THE PASSWORD: PASSWORD"
#     coded = cipher.encrypt(message)
#     print("Secret:", coded)
#     answer = cipher.decrypt(coded)
#     print("Message:", answer)
