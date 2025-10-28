from typing import Any, List, Type, Union
from collections import deque
import argparse


class Empty(Exception):
    """Exception for access to an empty stack"""

    pass


class ArrayStack:

    def __init__(self) -> None:

        self._stack = []

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


def isMatched(expr: Union[str, list]) -> bool:

    lefty = "({["
    righty = ")}]"
    S = ArrayStack()

    for symbol in expr:
        if symbol in lefty:
            S.push(symbol)
        elif symbol in righty:
            if S.is_empty():
                return False
            elif righty.index(symbol) != lefty.index(S.pop()):
                return False
        
    return S.is_empty()

if __name__ == "__main__":
    
    expressions = [
        '()(()){([()])}', 
        '((()(()){([()])}))', 
        ')(()){([()])}',
        '({[])}',
        '('
    ]

    results = []

    for e in expressions:
        results.append(isMatched(e))
    
    print(results)