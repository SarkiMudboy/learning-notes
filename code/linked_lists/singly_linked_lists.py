from typing import Type, Any, Union

class Empty(Exception):
    """Exception for access to an empty stack"""

    pass


class LinkedStack:

    class _Node:

        def __init__(self, element: Any, next):
            self._element = element
            self._next = next

    def __init__(self):

        self._head = None
        self._size = 0

    def __len__(self) -> int:

        return self._size
    
    def is_empty(self) -> bool:

        return self._size == 0
    
    def top(self) -> Any:

        if self.is_empty():
            raise Empty('Stack is empty')
        
        return self._head._element
    
    def push(self, e: Any) -> None:

        self._head = self._Node(e, self._head)
        self._size += 1

    def pop(self) -> Any:

        if self.is_empty():
            raise Empty('Stack is empty')

        element = self._head._element
        self._head = self._head._next

        self._size -= 1

        return element
    
    def __str__(self) -> str:

        if self.is_empty():
            return ''
        
        array = [self._head._element]
        
        next = self._head
        while next._next:
            next = next._next
            array.append(next._element)
        
        return str(array)

def test_stack():

    S = LinkedStack()  # contents: []
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

    print(S) # outputs: [7, 9]
    print(S.top())  # contents: [7, 9]; outputs 9
    S.push(4)  # contents: [7, 9, 4]
    print(len(S))  # contents: [7, 9, 4]; outputs 3
    print(S.pop())  # contents: [7, 9]; outputs 4
    S.push(6)  # contents: [7, 9, 6]
    print(S)

def isMatched(expr: Union[str, list]) -> bool:

    lefty = "({["
    righty = ")}]"
    S = LinkedStack()

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
    
    # test_stack()
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