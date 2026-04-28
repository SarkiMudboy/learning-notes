from typing import Callable, Type, Any, Union

class Empty(Exception):
    """Exception for access to an empty storage"""

    pass

class Full(Exception):
    """Exception for adding to a full storage"""
    pass


class BaseLinkedList:

    class _Node:
        def __init__(self, element:Any, next) -> None:
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def is_empty(self) -> bool:
        return True

    def __str__(self) -> str:

        if self.is_empty():
            return '[]'
        
        array = [self._head._element]
        
        next = self._head
        while next._next:
            next = next._next
            array.append(next._element)
        
        return str(array)


class LinkedStack(BaseLinkedList):

    def __init__(self):
    
        super().__init__()

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

def test_match():
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

class LinkedQueue(BaseLinkedList):

    def __init__(self):
        super().__init__()
        self._tail = None
    
    def __len__(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def first(self) -> Any:
        
        if self.is_empty():
            raise Empty("Queue is empty")
        
        return self._head._element
    
    def dequeue(self) -> Any:

        if self.is_empty():
            raise Empty("Queue is empty")

        val = self._head._element
        self._head = self._head._next
        self._size -= 1

        if self.is_empty():
            self._tail = None
        
        return val
    
    def enqueue(self, val: Any) -> None:

        n = self._Node(val, None)
        if self.is_empty():
            self._head = n
        else:
            self._tail._next = n
        self._tail = n
        self._size += 1


def test_queue():
    q = LinkedQueue()
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

def find_max_integer_from_random_stack():
    
    stack = LinkedStack()
    for n in [11, 2, 5]:
        stack.push(n)

    x = stack.pop()
    print(f'top -> {stack.top()}, pop -> {x}')
    x = stack.pop() if x < stack.top() else x
    print(x)
    # pop has a probability of 1/3, pop x 2 has a prob 2/3
    # store the first pop in x and compare the second pop with the first and store the largest

    # Another approach from claude:
    """
        x = pop()
        if pop() > x:
            x = pop()
    """


class CircularQueue(BaseLinkedList):

    def __init__(self):
        super().__init__()
        self._tail = None
    
    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def first(self) -> Any:

        if self.is_empty():
            raise Empty("Queue is empty")

        head = self._tail._next
        return head._element

    def dequeue(self) -> Any: 
        if self.is_empty():
            raise Empty("Queue is empty")

        old_head = self._tail._next
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = old_head._next
        self._size -= 1
        return old_head.element

    def enqueue(self, element: Any) -> None:
        new_node = self._Node(element, None)
        if self.is_empty():
            new_node._next = new_node
        else:
            new_node._next = self._tail._next
            self._tail._next = new_node
        self._tail = new_node

        self._size += 1
        return

    def rotate(self):
        if self._size > 0:
            self._tail = self._tail._next

    def __str__(self) -> str:

        if self.is_empty():
            return '[]'
        
        array = [self._tail._element]
        
        next = self._tail
        while next._next:
            next = next._next
            array.append(next._element)
        
        return str(array)
   
class RoundRobinScheduler:

    def __init__(self, services: list, operation: Callable):
        self.queue = CircularQueue()
        self.services = services or []
        self._op = operation
        self.__load_services()

    def __load_services(self):
        try:
            for service in self.services:
                self.queue.enqueue(service)
        except Exception as ex:
            print(f"error occured: {ex}")

        return

    def service(self):
        service = self.queue.first()
        result = None
        if service:
            result = self._op(service)

        self.queue.rotate()

        return result


def pay_five_k(name):
    return f"Paid {name} 5k ..."

def test_rr():
    s = ["woks", "roland", "antony", "victor"]
    r = RoundRobinScheduler(s, pay_five_k)

    for _ in range(12):
        print(r.service())

test_rr()


