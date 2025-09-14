from typing import Any, List
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

    parser = argparse.ArgumentParser(description="A CLI app for peeking at text files")
    parser.add_argument("-f", "--file", help="File to peek", default="results.txt")
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

        print(Down.top())


if __name__ == "__main__":
    main()
    # reverse_file("oop.py", "results.txt")


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
