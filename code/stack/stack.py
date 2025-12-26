from typing import Any, List, Type, Union
from collections import deque
import argparse


class Empty(Exception):
    """Exception for access to an empty stack"""

    pass


class Full(Exception):
    """Exception for adding to a full storage"""
    
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


class MaxArrayStack:

    def __init__(self, data=[], max_len=None) -> None:
        """ variant -> Allows for initializing the underlying array 
        C-6.17 In the previous exercise, we assume that the underlying list is initially
        empty. Redo that exercise, this time preallocating an underlying list with
        length equal to the stack’s maximum capacity.
        """

        if max_len and len(data) > max_len:
            raise Full(f"Cannot initialize list with length ({len(data)}) max length: {max_len}")

        self._stack = data
        self._max_len = max_len

    def __len__(self) -> int:
        return len(self._stack)

    def is_empty(self) -> bool:
        return len(self) == 0

    def top(self) -> Any:

        if self.is_empty():
            raise Empty("Stack is Empty")
        return self._stack[-1]

    def push(self, val: Any) -> None:

        if self._max_len and len(self._stack) >= self._max_len:
            raise Full("Stack is full")
        
        self._stack.append(val)

    def pop(self) -> Any:

        if self.is_empty():
            raise Empty("Stack is Empty")

        return self._stack.pop()

    def __str__(self) -> str:

        return str(self._stack)

    def clear(self) -> None:

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

def testMatched():
    
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

def is_matched_html(raw: str) -> bool:
    """Return True if all HTML tags are properly match; False otherwise."""

    S = ArrayStack()
    j = raw.find("<")

    while j != -1:
        k = raw.find(">", j+1)
        if k == -1:
            return False
        
        tag = raw[j+1:k]
        if not tag.startswith("/"):
            S.push(tag)
        else:
            if S.is_empty():
                return False
            else:
                if tag[1:] != S.pop():
                    return False
        j = raw.find("<", k+1)
    return S.is_empty()

def is_matched_html_with_attr(raw: str) -> bool:
    """
    C-6.19 In Code Fragment 6.5 (is_matched_html) we assume that opening tags in HTML have form
    <name>, as with <li>. More generally, HTML allows optional attributes
    to be expressed as part of an opening tag. The general form used is
    <name attribute1="value1" attribute2="value2">; for example,
    a table can be given a border and additional padding by using an opening
    tag of <table border="3" cellpadding="5">. Modify Code Frag-
    ment 6.5 so that it can properly match tags, even when an opening tag
    may include one or more such attributes.
    """

    S = ArrayStack()
    j = raw.find("<")

    while j != -1:
        k = raw.find(">", j+1)
        if k == -1:
            return False
        
        tag_with_attr = raw[j+1:k]
        if not tag_with_attr.startswith("/"):
            tag = tag_with_attr.split(" ")[0]
            S.push(tag)
        else:
            tag = tag_with_attr[1:]
            if S.is_empty():
                return False
            else:
                if tag != S.pop():
                    return False
        j = raw.find("<", k+1)
    return S.is_empty()


def test_html_match(source: str) -> None:

    content = None
    matched = False

    with open(source, "r") as f:
        content = f.read()

    if content:
        matched = is_matched_html_with_attr(content)
    
    return matched

if __name__ == "__main__":
    m = test_html_match("./index.html")
    print(f"index is matched?: {m}")
    
        
