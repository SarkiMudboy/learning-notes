### Intro

A ***data structure*** is a systematic way of organizing and accessing data, and an ***algorithm*** is a step-by-step procedure for performing some task in a finite amount of time.

The primary analysis tool used involves characterizing the running times of algorithms and data structure operations, with space usage also being of interest. Running time is a natural measure of “goodness,” since time is a precious resource—computer solutions should run as fast as possible. In general, the running time of an algorithm or data structure operation increases with the input size, although it may also vary for different inputs of the same size. Also, the running time is affected by the hardware environment (e.g., the processor, clock rate, memory, disk) and software environment (e.g., the operating system, programming language) in which the algorithm is implemented and executed. All other factors being equal, the running time of the same algorithm on the same input data will be smaller if the computer has, say, a much faster processor or if the implementation is done in a program compiled into native machine code instead of an interpreted implementation.

Focusing on running time as a primary measure of goodness requires that we be able to use a few mathematical tools. In spite of the possible variations that come from different environmental factors, we would like to focus on the relationship between the running time of an algorithm and the size of its input.

**Experimental approach to measuring the goodness of an algo**:
In experimental studies: we can study its running time by executing it on various test inputs and recording the time spent during each execution.
*Challenges*:
While experimental studies of running times are valuable, especially when finetuning production-quality code, there are three major limitations to their use for algorithm analysis: 
- Experimental running times of two algorithms are difficult to directly compare unless the experiments are performed in the same hardware and software environments.
- Experiments can be done only on a limited set of test inputs; hence, they leave out the running times of inputs not included in the experiment (and these inputs may be important).
- An algorithm must be fully implemented in order to execute it to study its running time experimentally.

**Counting primitive ops**:
Formally, a primitive operation corresponds to a low-level instruction with an execution time that is constant. Ideally, this might be the type of basic operation that is executed by the hardware, although many of our primitive operations may be translated to a small number of instructions. Instead of trying to determine the specific execution time of each primitive operation, we will simply count how many primitive operations are executed, and use this number t as a measure of the running time of the algorithm. The implicit assumption in this approach is that the running times of different primitive operations will be fairly similar. Thus, the number, ***t***, of primitive operations an algorithm performs will be proportional to the actual running time of that algorithm.
*They include*:
- Assigning an identifier to an object.
- Determining the object associated with an identifier.
- Performing an arithmetic operation (for example, adding two numbers).
- Comparing two numbers.
- Accessing a single element of a Python list by index.
- Calling a function (excluding operations executed within the function).
- Returning from a function.

To capture the order of growth of an algorithm’s running time, we will associate, with each algorithm, a function f(n) that characterizes the number of primitive operations that are performed as a function of the input size n.

**Worst case > Average case**

Worst-case analysis is much easier than average-case analysis, as it requires only the ability to identify the worst-case input, which is often simple. Also, this approach typically leads to better algorithms. Making the standard of success for an algorithm to perform well in the worst case necessarily requires that it will do well on every input.

#### Seven deadly funcs

- ***Constant func***: 
$$
f(n) = c
$$
	For any size of n, f(n) will always be a constant c. As simple as it is, the constant function is useful in algorithm analysis, because it characterizes the number of steps needed to do a basic operation on a computer (primitive ops).

- ***Logarithmic Func***:  
$$
f(n) = logb n
$$
	if and only if 
$$
	b^x = n
$$
	for some constant b > 1 (base)
	
	The most common base for the logarithm function in computer science is 2, as computers store integers in binary, and because a common operation in many algorithms is to repeatedly divide an input in half. In fact, this base is so common that we will typically omit it from the notation when it is 2.

- ***Linear Func***:
$$
f(n) = n
$$

	That is, given an input value n, the linear function f assigns the value n itself.
	This function arises in algorithm analysis any time we have to do a single basic operation for each of n elements.

- **NlogN Func***:
$$
	f(n) = nlogn
$$
	This function grows a little more rapidly than the linear function and a lot less rapidly than the quadratic function; therefore, we would greatly prefer an algorithm with a running time that is proportional to *nlogn*, than one with quadratic running time. Example the fastest possible algorithms for sorting n arbitrary values require time proportional to *nlogn*.

- ***Quadratic Func***:
$$
f(n) = n^2
$$

	For any given value of n, f(n) assigns a product of itself i.e. n^2. This can be seen in nested loops where the inner loop performs a linear number of operations and the outer loop is performed a linear number of times.

- ***Cubic***: 
$$
f(n) = n^3
$$

- **Exponential Func***:
$$
f(n) = b^n
$$

	where b is a positive constant, called the base, and the argument n is the exponent. That is, function f(n) assigns to the input argument n the value obtained by multiplying the base b by itself n times. As was the case with the logarithm function, the most common base for the exponential function in algorithm analysis is b = 2. 
	For example, an integer word containing n bits can represent all the nonnegative integers less than 2^n. If we have a loop that starts by performing one operation and then doubles the number of operations performed with each iteration, then the number of operations performed in the nth iteration is 2^n.

**Ceiling/Floor functions**:

One additional comment concerning the functions above is in order. When discussing logarithms, we noted that the value is generally not an integer, yet the running time of an algorithm is usually expressed by means of an integer quantity, such as the number of operations performed. Thus, the analysis of an algorithm may sometimes involve the use of the floor function and ceiling function, which are defined respectively as follows:
- floor(x) = the largest integer less than or equal to x.
- ceil(x) = the smallest integer greater than or equal to x.


### CHAPTER 2: Recursion

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
for a seq in which the target value is at random'''

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
        
# test using python timeit module

# compute binary search time

def binary_time() -> None:
    SETUP_CODE = '''
from __main__ import binary_search
from random import randint'''
    TEST_CODE = '''
mylist = [x for x in range(10000)]
find = randint(0, len(mylist))
binary_search(mylist, find, len(mylist)-1, 0)'''

    # timeit.repeat statement
    times = timeit.timeit(setup=SETUP_CODE, stmt=TEST_CODE, number=10000)
    # printing minimum exec. time
    print('Binary search time: {}'.format(times))

# compute linear search time
def linear_time() -> None:
    SETUP_CODE = '''
from __main__ import linear_search
from random import randint'''

    TEST_CODE = '''
mylist = [x for x in range(10000)]
find = randint(0, len(mylist))
linear_search(mylist, find)'''

    # timeit.repeat statement
    times = timeit.timeit(setup=SETUP_CODE, stmt=TEST_CODE, number=10000)
    # printing minimum exec. time
    print('Linear search time: {}'.format(times))

if __name__ == '__main__':
    binary_time()
    linear_time()

'''
Results:
Binary search time: 2.175394000019878
Linear search time: 4.01497650006786
'''
```

^34e100
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

When c = 0 n = 0, when c = 1 n= 1 where n if num of lines drawn. More generally, the number of lines printed by draw interval(c) is one more than twice the number generated by a call to draw interval(c−1), as one center line is printed between two such recursive calls. By induction, we have that the number of lines is thus 
$$
1+2 ·((2^c−1) −1) = 1+((2^c) −2) = (2^c) −1. 
$$
So exponential time: ***O(2^n)***.

***Binary Search***: 
***The binary search algorithm runs in O(logn) time for a sorted sequence with n elements.***
For every recursive call n (number of candidates) reduces at least by half:
1st call to func -> n (n/(2^0))
2nd -> 1st recursive call:
$$
n/2 -> (n/(2^1))
$$
3rd -> 2nd recursive call:
$$
n/4 -> (n/(2^2))
$$
4th -> 3rd recursive call: 
$$
n/8 -> (n/(2^3)) ...
$$
nth -> (n-1)th recursive call:
$$
n/(2^j)
$$
which means max no of recursive calls is what j that produces a number of candidate < 1 i.e. Assuming that j = r

$$
n/(2^r) < 1 => 2^(-r) * n < 1 
$$
(remember n = 2^(logn) and from log rules 
$$
2^(x) * 2^(y) = 2^(x+y)
$$
which means 
$$
=> 2^(-r + logn) < 2^0 => (-r+logn) < 0 
$$
\[eliminating the base 2] 
$$
=> r > logn => r = logn + 1? 
$$
which implies ***O(logn)***

***File sys***:

- We begin by showing that there are precisely n recursive invocations of the function, in particular, one for each entry in the relevant portion of the file system. Intuitively, this is because a call to disk usage for a particular entry e of the file system is only made from within the for loop, when processing the entry for the unique directory that contains e, and that entry will only be explored once. 
- Having established that there is one recursive call for each entry of the file system, we return to the question of the overall computation time for the algorithm. It would be great if we could argue that we spend O(1) time in any single invocation of the function, but that is not the case. While there are a constant number of steps reflect in the call to os.path.getsize to compute the disk usage directly at that entry, when the entry is a directory, the body of the disk usage function includes a for loop that iterates over all entries that are contained within that directory. In the worst case, it is possible that one entry includes *n−1* others. This assumes a worst-case scenario.
- Based on this reasoning, we could conclude that there are ***O(n)*** recursive calls, each of which runs in ***O(n)*** time, leading to an overall running time that is:
$$
O(n^2)
$$
- While this upper bound is technically true, it is not a tight upper bound. Remarkably, we can prove the stronger bound that the recursive algorithm for disk usage completes in ***O(n)*** time! The weaker bound was pessimistic because it assumed a worst-case number of entries for each directory. While it is possible that some directories contain a number of entries proportional to n, they cannot all contain that many. To prove the stronger claim, we choose to consider the overall number of iterations of the for loop across all recursive calls. We claim there are precisely n − 1 such iteration of that loop overall. We base this claim on the fact that each iteration of that loop makes a recursive call to disk usage, and yet we have already concluded that there are a total of n calls to disk usage (including the original call). We therefore conclude that there are ***O(n)*** recursive calls, each of which uses ***O(1)*** time outside the loop, and that the overall number of operations due to the loop is **O(n)**. Summing all of these bounds, the overall number of operations is **O(n)**.
- The idea that we can sometimes get a tighter bound on a series of operations by considering the cumulative effect, rather than assuming that each achieves a worst case is a technique called **amortization**.

#### More Notes:

- To combat against infinite recursions, the designers of Python made an intentional decision to limit the overall number of function activations that can be simultaneously active. The precise value of this limit depends upon the Python distribution, but a typical default value is 1000. If this limit is reached, the Python interpreter raises a **RuntimeError** with a message, maximum recursion depth exceeded. Python’s artificial limit on the recursive depth could disrupt such otherwise legitimate computations.
- Python interpreter can be dynamically reconfigured to change the default recursive limit. This is done through use of a module named sys, which supports a ***getrecursionlimit*** function and a ***setrecursionlimit***.

```python
import sys old = sys.getrecursionlimit( ) # perhaps 1000 is typical 
sys.setrecursionlimit(1000000) # change to allow 1 million nested calls
```

- Types of recursion based on number of active recursion calls that may be started from within the body of a single activation.
	- If a recursive call starts at most one other, we call this a ***linear recursion***.
	- If a recursive call may start two others, we call this a ***binary recursion.***
	- If a recursive call may start three or more others, this is ***multiple recursion***.
- Examples of linear recursion: Ops on data sequences i.e. lists/arrays (like adding, reversing etc.) in **O(n)**, computing powers.

***Computing powers***:
- This involves raising a number x to an arbitrary nonnegative integer, n. For n > 0:
$$
x^n = x ·x^(n-1)
$$
- There are two ways to recursively implement this, each with diff perf.

	**First**:
	func power(x, n) => x^n
	base case: if n = 0, power(x, n) = 1
	for n > 0: power(x, n) = x * x ^ (n-1) => x * power(x, n-1)
	
	```python
	def power(base: int, exp: int) -> int:
	    if exp == 0:
	        return 1
	    else:
	        return base * power(base, exp-1)
	```

	A recursive call to this version of power(x,n) runs in *O(n)* time. Its recursion trace shows the parameter n decreasing by one with each call, and constant work performed at each of n+1 levels.

	**Second**:
	A much faster/efficient way is to consider that for n that is even. Consider k = n // 2 or k = floor(n/2). (highest <), therefore n //2 = n/2 implying:
$$
	(x^k)^2 = (x^(n/2))^2 = x^n 
$$
	for odd floor(n/2) = (n-1)/2 i.e. floor(13/2) = 12/2 = 6, therefore
$$
		(x^k)^2 = (x^(n-1/2))^2 = x ·x^(n-1) 
$$
	Base case: if n = 0, power(x, n) = 1
	n % 2 == 0 (even): (x^(n/2))^2 
	n % 2 == 1 (odd): x * (x^(n/2))^2 
	
	```python
	def f_power(base: int, expn: int) -> int:
	    if expn == 0:
	        return 1
	    else:
	        partial = f_power(base, expn//2)
	        result = partial * partial
	
	        if expn % 2 == 1:
	            return base * result
	        return result
```

The size of the problem n reduces by at most half with each recursive call. Each individual activation of the function uses O(1) operations (excluding the recursive calls), We see that the amount of recursive calls is same as the num of times we reduce our sample size before getting to 1 which implies the recursive depth of *O(logn)*. This also means the memory usage is also *O(logn)*. (*O(logn)* activation records to be stored in memory).

```shell
Loop approach time: 0.03884080005809665
Linear recursion approach time: 0.07637619995512068
Improved Linear recursion approach time: 0.008094700053334236
```
