## Recursion

Recursion is a technique by which a function makes one or more calls to itself during execution, or by which a data structure relies upon smaller instances of the very same type of structure in its representation.

Most modern programming languages support functional recursion using the identical mechanism that is used to support traditional forms of function calls. When one invocation of the function make a recursive call, that invocation is suspended until the recursive call completes.

An example of a recursive function is the Factorial(!):
1. It contains at least one (1) **base case**: 
	n! -> 1 if n = 0
2. It contains at least 1 **recursive case**: 
	 n! -> n!(n-1)! if n>=1

```python
 # Achieving factorial with recursion 
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Achieving factorial with loops 
def fac_iter(n):
    total = 1
    for i in range(1, n+1):
        total *= i
    return total

  

print('recursive-> ', factorial(14))

print('iterative-> ', fac_iter(14))
```

^2a56d4

A ***recursion trace*** is an illustration of the program's execution of a recursive function. In Python, each time a function (recursive or otherwise) is called, a structure known as an **activation record** or **frame** [Maybe?](https://courses.grainger.illinois.edu/cs225/sp2024/resources/stack-heap/#:~:text=stack%20%3A%20stores%20local%20variables,stores%20the%20code%20being%20executed) & [[Computer Architecture Notes#^5b8bc9]] is created to store information about the progress of that invocation of the function. This activation record includes a namespace for storing the function call’s parameters and local variables and information about which command in the body of the function is currently executing. 
- When the execution of a function leads to a nested function call, the execution of the former call is suspended and its activation record stores the place in the source code at which the flow of control should continue upon return of the nested call. This process is used both in the standard case of one function calling a different function, or in the recursive case in which a function invokes itself. The key point is that there is a different activation record for each active call.
#### **Binary Search**

This is an important ***recursive*** algo in computing that is used to locate a target value in a sorted sequence of ***n*** elements. It shows the importance of storing data in a sorted manner.
- When the sequence is unsorted, the standard approach to search for a target value is to use a loop to examine every element, until either finding the target or exhausting the data set. This is known as the ***sequential search algorithm***. This algorithm runs in O(n) time (i.e., linear time) since every element is inspected in the worst case.

Take a sorted and indexable list:
- S = 2, 3, 4, 5, 7, 9, 10, 15, 18, 24, 28, 30, 32, 34, 36, 38, 40, 42, 45, 46, 50, 55, 60

**To find an element x?:** at any loc S\[j] we know that all element at interval S\[j] >= (S\[0]-> S\[j-1] )
and S\[j] < (S\[j+1] -> S\[n-1]). We can ***zero in*** by recursively checking the S\[high, low] at diff indices. We call an element of the sequence a candidate if, at the current stage of the search, we cannot rule out that this item matches the target. The algorithm maintains two parameters, low and high, such that all the candidate entries have index at least low and at most high. Initially, low = 0 and high = n− 1. We then compare the target value to the median candidate, that is, the item data\[mid] with index. 
- mid = floor((low +high)/2) -> (Largest num >= mid).
We consider three cases: 
-  If the target equals data\[mid], then we have found the item we are looking for, and the search terminates successfully.
- If target < data\[mid], then we recur on the first half of the sequence, that is, on the interval of indices from low to mid−1.
- If target > data\[mid], then we recur on the second half of the sequence, that is, on the interval of indices from mid+1 to high. An unsuccessful search occurs if low > high, as the interval \[low, high] is empty.

- This Binary search runs in ***O(logn)*** time.

```python
'''In this test, we evaluate the running times of
a sequesntial search vs binary search vs unsorted data
for a seq in which the target value is at the end'''

from typing import Sequence

# Sequential search
def seq_search(data: Sequence[int], target: int) -> None:
    for index, elem in enumerate(data):
        if elem == target:
            print(f'Found! at {index}')
            break  

# Binary Search

def binary_search(data: Sequence[int], target: int, high: int, low: int) -> None:
    if low > high:
        print('Error! Found')
        return
        
    mid = (high + low) // 2
    if data[mid] == target:
        print(f'Found! at {mid}')
        return

    if target < data[mid]:
        return binary_search(data, target, mid - 1,  low)
    else:
        return binary_search(data, target, high, mid + 1)
        
data = (12, 11, 3, 2, 16, 13, 10, 5, 15, 4, 7, 8, 1, 9, 6, 14) # unsorted list

sorted_data = tuple(sorted(data)) # sorted list

seq_search(sorted_data, 14)
'''
-> time python recursive.py (on wsl)
Found! at 13

real    0m0.046s
user    0m0.014s
sys     0m0.014s
'''

binary_search(sorted_data, 14, 15, 1)
'''
-> time python recursive.py (on wsl)
Found! at 13

real    0m0.051s
user    0m0.001s
sys     0m0.027s
'''
```


## File systems

The computer file system structure is recursive in nature: Where files and folders are nested arbitrary deep within a topmost folder/directory as deep as the computer memory allows. The OS operations on the file system also include recursive algos. One of such is a function that computes the disk space usage of each folder/file in a given file sys path. It includes the immediate space used by the Dir += the cumulative space used by all nested entries. An implementation is seen below:

```python
import os
import sys

def DiskUsage(path: str) -> int:
    '''Disk Usage for a directory/file in python'''
    total = os.path.getsize(path)

    if os.path.isdir(path):
        for obj in os.listdir(path):
            child = os.path.join(path, obj)
            total += DiskUsage(child) # recursive call
    print(f'total du for {path}:', '{0:<7}'.format(total))
    return total

if __name__ == '__main__':
    path = sys.argv[1]
    if not path:
        raise ValueError('Please Enter a filepath')
    du = DiskUsage(path)
    print(f'ToTal->{du/1000}kb')
```


#### **Running time for each algo**

***Factorial***: Each activation of the factorial function accounts for n-1 iterations if O(1) ops. To compute factorial(n), we see that there are a total of n+1 activations, as the parameter decreases from n in the first call, to n−1 in the second call, and so on, until reaching the base case with parameter 0.
```python
return n * factorial(n-1)
```
Total ops sits at n+1 ops (Looking at the recursive trace). So it can be concluded that the running time for the algo is **O(n)**. It is also clear, given an examination of the function body in ***Code Fragment*** [[Data Structures and Algo#^2a56d4]], that each individual activation of factorial executes a constant number of operations. Therefore, we conclude that the overall number of operations for computing factorial(n) is ***O(n)***, as there are ***n+1*** activations, each of which accounts for ***O(1)*** operations.

***Ruler***: The initial call to `draw_interval` serves as the basis for analyzing the efficiency of the algo as we want to measure how many calls to the `draw_line` function was made. Each call to the `draw_interval` func makes at least 1 call to `draw_line` and 2 calls to `draw_interval`. 
```python
def draw_interval(c): # c -> center_length
	if c > 0:
		draw_interval(c-1) # top
		draw_line(c) # mid
		draw_interval(c-1) # bottom
```

**We use induction to prove a conclusion**: ***For every c>= 0, the `draw_line` func is called (2^c) -1 times***.

When c = 0 n = 0, when c = 1 n= 1 where n if num of lines drawn. More generally, the number of lines printed by draw interval(c) is one more than twice the number generated by a call to draw interval(c−1), as one center line is printed between two such recursive calls. By induction, we have that the number of lines is thus 1+2 ·((2^c−1) −1) = 1+((2^c) −2) = (2^c) −1. So exponential time: ***O(2^n)***.

***Binary Search***: 

