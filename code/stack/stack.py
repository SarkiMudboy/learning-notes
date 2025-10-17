from typing import Any, List, Type
from collections import deque
import argparse


class Empty(Exception):
    """Exception for access to an empty stack"""

    pass


class ArrayStack:

    def __init__(self, init: int = 0) -> None:

        self._stack = [] if not init else [i for i in range(init)]

    def __len__(self) -> int:
        return len(self._stack)

    def is_empty(self) -> bool:
        return len(self) == 0

    def top(self) -> Any:

        if self.is_empty():
            raise Empty("Stack is Empty")
        return self._stack[-1]

    def push(self, val: Any) -> None:

        self._stack.append(val)

    def pop(self) -> Any:

        if self.is_empty():
            raise Empty("Stack is Empty")

        return self._stack.pop()

    def __str__(self) -> str:

        return str(self._stack)

    def clear(self) -> None:
        """
        R-6.4 Give a recursive method for removing all the elements from a stack.
        """

        if len(self) == 0:
            return

        self.pop()
        return self.clear()


def reverse_file(file: str, out: str) -> None:

    S = ArrayStack()

    f = open(file, "r")
    for line in f:
        S.push(line.rstrip("\n"))

    o = open(out, "w")
    while not S.is_empty():
        o.write(S.pop() + "\n")
    o.close()


def main():

    parser = argparse.ArgumentParser(
        description="A CLI app for peeking at text files"
    )
    parser.add_argument(
        "-f", "--file", help="File to peek", default="results.txt"
    )
    args = parser.parse_args()

    file = open(args.file, "r")
    Down = ArrayStack()
    Up = ArrayStack()

    line = file.readline().rstrip("\n")
    Down.push(line)
    print(Down.top())

    while line:

        nav = input("enter (u) to go up or (d) to go down:")

        if nav.lower() == "u":
            line = Up.pop()
            Down.push(line)
        elif nav.lower() == "d":
            Up.push(Down.pop())
            line = file.readline()
            Down.push(line)
        else:
            print("Invalid input")
            quit(0)

        print(Down.top())



def test_stack():

    S = ArrayStack()  # contents: []
    print(S)

    S.push(5)  # contents: [5]
    print(S)

    S.push(3)  # contents: [5, 3]
    print(len(S))  # contents: [5, 3]; outputs 2

    print(S.pop())  # contents: [5]; outputs 3
    print(S.is_empty())  # contents: [5]; outputs False
    print(S.pop())  # contents: [ ]; outputs 5
    print(S.is_empty())  # contents: [ ]; outputs True

    S.push(7)  # contents: [7]
    S.push(9)  # contents: [7, 9]

    print(S)
    print(S.top())  # contents: [7, 9]; outputs 9
    S.push(4)  # contents: [7, 9, 4]
    print(len(S))  # contents: [7, 9, 4]; outputs 3
    print(S.pop())  # contents: [7, 9]; outputs 4
    S.push(6)  # contents: [7, 9, 6]
    print(S)


def transfer(S: ArrayStack, T: ArrayStack) -> None:
    """
    Implement a function with signature transfer(S, T) that transfers all ele-
    ments from stack S onto stack T, so that the element that starts at the top
    of S is the first to be inserted onto T, and the element at the bottom of S
    ends up at the top of T.

    Args:
        S: ArrayStack -> The source Stack for transfer
        T: ArrayStack The destination stack for transfer
    Returns:
        None

    """
    print(S.top())
    for _ in range(len(S)):

        T.push(S.pop())

    print(T)


def reverse_list(data: list) -> list:
    """
    Implement a function that reverses a list of elements by pushing them onto
    a stack in one order, and writing them back to the list in reversed order.

    Args:
        data: list -> initial array

    Returns:
        list: reversed list
    """

    s = ArrayStack()
    for item in data:
        s.push(item)

    reversed = []
    for i in range(len(s)):
        reversed.append(s.pop())

    return reversed


class ArrayQueue:

    DEFAULT_CAPACITY = 10
    EMPTY_ERROR_MSG = "Queue is empty"

    def __init__(self, cap: int=0):

        if cap <= 0:
            cap = ArrayQueue.DEFAULT_CAPACITY

        self._data = [None] * cap
        self._size = 0
        self._front = 0

    def first(self) -> Any:

        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)

        return self._data[self._front]

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def dequeue(self) -> Any:

        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)

        obj = self._data[self._front]
        self._data[self._front] = None # helps with GC
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        return obj

    def enqueue(self, obj: Any) -> None:

        if self._size == len(self._data):
            # resize
            self._resize(2 * len(self._data))

        available = (self._front + self._size) % len(self._data)
        self._data[available] = obj
        self._size += 1

    def _resize(self, capacity: int) -> None:

        old = self._data
        self._data = [None] * capacity
        walk = self._front

        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (walk + 1) % len(old)

        self._front = 0

    def __str__(self) -> str:
         
        data = [None] * self._size

        walk = self._front

        for k in range(self._size):
            data[k] = self._data[walk]
            walk = (walk + 1) % len(self._data)

        return str(data)


def test():
    q = ArrayQueue()
    q.enqueue(5)
    print(q)  # [5]
    q.enqueue(3)
    print(q)  # [5, 3]
    print(q.dequeue())  # 5
    q.enqueue(2)
    print(q)  # [3, 2]
    q.enqueue(8)
    print(q)  # [3, 2, 8]
    print(q.dequeue())  # 3
    print(q.dequeue())  # 2
    q.enqueue(9)
    print(q)  # [8, 9]

def test_operations(q):
    """
    R-6.8 Suppose an initially empty queue Q has executed a total of 32 enqueue
    operations, 10 first operations, and 15 dequeue operations, 5 of which
    raised Empty errors that were caught and ignored. What is the current
    size of Q?
    ----
    R-6.9 Had the queue of the previous problem been an instance of ArrayQueue
    that used an initial array of capacity 30, and had its size never been greater
    than 30, what would be the final value of the front instance variable?

    """

    for i in range(10):
        q.enqueue(i)
    
    for _ in range(15):
        try:
            print(q.dequeue())
        except Empty:
            print("empty")
            continue
    

    for i in range(22):
        q.enqueue(i)

    print(q.first())
    print(q)

def test_ops2(q):

    # another approach to R-6.9

    for _ in range(5):
        try:
            print(q.dequeue())
        except Empty:
            print("empty")
            continue
    
    for i in range(30):
        q.enqueue(i)
    
    for _ in range(10):
        print(q.dequeue())

    for i in range(2):
        q.enqueue(i)

    print(q.first())
    print(q)



class CollectionsQueue:
    """
    R-6.11 Give a simple adapter that implements our queue ADT while using a
    collections.deque instance for storage.
    """
    EMPTY_ERROR_MSG = "Queue is empty"

    def __init__(self):

        self._data = deque([])
    
    def first(self) -> Any:

        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)
        
        return self._data[0]

    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:

        return len(self._data) == 0
    
    def dequeue(self) -> Any:

        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)
        
        return self._data.popleft()
    
    def enqueue(self, obj: Any) -> None:

        self._data.append(obj)
    
    def __str__(self) -> str:

        return str(self._data)
    
class ArrayDeque:

    DEFAULT_CAPACITY = 10
    EMPTY_ERROR_MSG = "Queue is empty"

    def __init__(self):

        self._data = [None] * ArrayDeque.DEFAULT_CAPACITY
        self._front = 0
        self._size = 0

    def __len__(self) -> int:
        """Return the number of elements in deque D;"""
        return self._size
    
    def is_empty(self) -> bool:
        """Return True if deque D does not contain any elements."""
        return self._size == 0
    
    def add_first(self, e: Any):
        """Add element e to the front of deque D."""

        if self._size == len(self._data):
            self._resize(len(self._data) * 2)

        front = (self._front - 1) % len(self._data)
        self._data[front] = e
        self._front = front

        self._size += 1

        return
        
    def add_last(self, e: Any):
        """Add element e to the back of deque D"""

        if self._size == len(self._data):
            self._resize(self._cap * 2)
        
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

        return
        

    def delete_first(self) -> any:
        """Remove and return the first element from deque D;
            an error occurs if the deque is empty."""
        
        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)

        obj = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)

        self._size -= 1

        return obj

    def delete_last(self) -> Any:
        """Remove and return the last element from deque D;
            an error occurs if the deque is empty."""
        
        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)
        
        last = (self._front + self._size - 1) % len(self._data)
        obj = self._data[last]
        self._data[last] = None
        self._size -= 1

        return obj

    def first(self) -> Any:
        """
        Return (but do not remove) the first element of deque D;
        an error occurs if the deque is empty.
        """

        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)
        
        return self._data[self._front]

    def last(self) -> Any:
        """
        Return (but do not remove) the last element of deque D;
        an error occurs if the deque is empty.
        """

        if self.is_empty():
            raise Empty(self.EMPTY_ERROR_MSG)
        
        last = (self._front + self._size - 1) % len(self._data)
        return self._data[last]


    def _resize(self, cap: int) -> None:
        """Resizes the underlying array to the new capacity specified by cap"""

        old = self._data
        walk = self._front
        self._data = [None] * cap

        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (self._front + 1) % len(old)
        
        self._front = 0

        return
    
    def __str__(self) -> str:
        """Returns the string representation of the deque"""
         
        data = [None] * self._size

        walk = self._front

        for k in range(self._size):
            data[k] = self._data[walk]
            walk = (walk + 1) % len(self._data)

        return str(data)
    
def swap_indices(D: Type[ArrayDeque], Q: Type[ArrayQueue], index_1: int, index_2: int) -> Type[ArrayDeque]:
    
    """
    R-6.13 Suppose you have a deque D containing the numbers (1, 2, 3, 4, 5, 6, 7, 8),
    in this order. Suppose further that you have an initially empty queue Q.
    Give a code fragment that uses only D and Q and
    results in D storing the elements in the order (1, 2, 3, 5, 4, 6, 7, 8).
    """
    size = len(D)
    prefix_count = 0
    index = 0

    while index < index_1:
        # ideally the loop mutates deque to [4, 5, 6, 7, 8, 1, 2, 3]

        D.add_last(D.delete_first())
        prefix_count += 1
        index += 1

    Q.enqueue(D.delete_first()) # index_1 -> queue
    Q.enqueue(D.delete_first()) # index_2 -> queue [4, 5]

    for k in range(prefix_count):
        Q.enqueue(D.delete_last()) # queue = [4, 5, 3, 2, 1]
    
    for _ in range(len(D)):
        Q.enqueue(D.delete_first()) # queue = [4, 5, 3, 2, 1, 6, 7, 8] / deque -> []

    for k in range(size):
        
        if k > (prefix_count + 1):
            D.add_last(Q.dequeue()) # deque = [..., 6, 7, 8]
        else:
            D.add_first(Q.dequeue()) # deque = [1, 2, 3, 5, 4]

    return D

def swap_indices_v2(D: Type[ArrayDeque], Q: Type[ArrayQueue], index_1: int, index_2: int) -> Type[ArrayDeque]:
    
    """
    R-6.13 Suppose you have a deque D containing the numbers (1, 2, 3, 4, 5, 6, 7, 8),
    in this order. Suppose further that you have an initially empty queue Q.
    Give a code fragment that uses only D and Q (and no other variables) and
    results in D storing the elements in the order (1, 2, 3, 5, 4, 6, 7, 8).
    """
    size = len(D)

    while True:
        # ideally the loop mutates deque to [4, 5, 6, 7, 8, 1, 2, 3]

        D.add_last(D.delete_first())
        if D.last() == 3:
            break

    Q.enqueue(D.delete_first()) # index_1 -> queue
    Q.enqueue(D.delete_first()) # index_2 -> queue [4, 5]

    while True:
        Q.enqueue(D.delete_last())
        if len(Q) == 5:  # queue = [4, 5, 3, 2, 1]
            break
    
    for _ in range(len(D)):
        Q.enqueue(D.delete_first()) # queue = [4, 5, 3, 2, 1, 6, 7, 8] / deque -> []

    for k in range(size):
        
        if len(Q) < 4:
            D.add_last(Q.dequeue()) # deque = [..., 6, 7, 8]
        else:
            D.add_first(Q.dequeue()) # deque = [1, 2, 3, 5, 4]

    return D

def swap_indices_stack(D: Type[ArrayDeque], S: Type[ArrayStack], index_1: int, index_2: int) -> Type[ArrayDeque]:
    """
    R-6.14 Repeat the previous problem using the deque D and an initially empty stack S.
    """

    while True:

        S.push(D.delete_last())
        if D.last() == 5:
            break

    for _ in range(3):

        S.push(D.delete_first())

    S.push(D.delete_last())
    S.push(D.delete_last())

    D.add_last(S.pop())
    D.add_first(S.pop())

    for _ in range(3):
        D.add_first(S.pop())

    for _ in range(len(S)):
        D.add_last(S.pop())

    return D

    



if __name__ == "__main__":

    source_array = [1, 2, 3, 4, 5, 6, 7, 8]
    D = ArrayDeque()
    Q = ArrayQueue()
    S = ArrayStack()

    for i in source_array:
        D.add_last(i)
    print(D)

    swapped_D = swap_indices_stack(D, S, 3, 4)
    print(swapped_D)


def test_deque():

    D = ArrayDeque()

    D.add_last(5) 
    D.add_first(3) # – [3, 5]
    D.add_first(7) # – [7, 3, 5]
    print(D.first()) #  7 [7, 3, 5]
    print(D.delete_last()) # 5 [7, 3]
    print(len(D)) # 2 [7, 3]
    print(D.delete_last()) # 3 [7]
    print(D.delete_last()) # 7 [ ]
    D.add_first(6) # – [6]
    print(D.last()) # 6 [6]
    D.add_first(8) # – [8, 6]
    print(D.is_empty()) # False [8, 6]
    print(D.last()) # 6