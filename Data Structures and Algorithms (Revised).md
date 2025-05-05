
## Array Based Sequences

**Notes**

- A computer system will have a huge number of bytes of memory, and to keep
track of what information is stored in what byte, the computer uses an abstraction
known as a memory address. In effect, each byte of memory is associated with a
unique number that serves as its address (more formally, the binary representation
of the number serves as the address). In this way, the computer system can refer
to the data in “byte #2150” versus the data in “byte #2157,” for example. Memory
addresses are typically coordinated with the physical layout of the memory system,
and so we often portray the numbers in sequential fashion. 

- Despite the sequential nature of the numbering system, computer hardware is
designed, in theory, so that any byte of the main memory can be efficiently accessed
based upon its memory address. In this sense, we say that a computer’s main memory 
performs as **random access memory (RAM)**. That is, it is just as easy to retrieve
byte #8675309 as it is to retrieve byte #309. (In practice, there are complicating
factors including the use of caches and external memory.
Using the notation for asymptotic analysis, we say that any individual byte of memory 
can be stored or retrieved in O(1) time.

- A group of related variables can be stored one after another in a contiguous
portion of the computer’s memory. We will denote such a representation as an
array.  We will refer to each location within an array as a cell, and will use an
integer index to describe its location within the array, with cells numbered starting
with 0, 1, 2, and so on.

- Each cell of an array must use the same number of bytes. This requirement is
what allows an arbitrary cell of the array to be accessed in constant time based on
its index. In particular, if one knows the memory address at which an array starts, 
the number of bytes per element (e.g., 2 for a Unicode character), and a desired index 
within the array, the appropriate memory address can be computed using the calculation, 
*start + cellsize * index.* 

- Python represents a list or tuple instance using an internal storage mechanism 
of an array of object references. At the lowest level, what is stored is a consecutive 
sequence of memory addresses at which the elements of the sequence reside. 
Although the relative size of the individual elements may vary, the number of
bits used to store the memory address of each element is fixed (e.g., 64-bits per
address). In this way, Python can support constant-time access to a list or tuple
element based on its index. Note as well that a reference to the None object can 
be used as an element of the list to represent an empty value.

- A single list instance may include multiple references to the same object as elements 
-of the list, and it is possible for a single object to be an element of two or more lists, as 
those lists simply store references back to that object. When the elements of the list are immutable objects, (as with the integer instances), the fact that the two lists share elements is 
not that significant, as neither of the lists can cause a change to the shared object.

- The same semantics is demonstrated when making a new list as a copy of an
existing one, with a syntax such as backup = list(primes). This produces a new
list that is a **shallow copy**, in that it references the same elements
as in the first list. With immutable elements, this point is moot. If the contents of
the list were of a mutable type, a deep copy, meaning a new list with new elements,
can be produced by using the ***deepcopy*** function from the copy module.

- **Note** - *getsizeof* for a list instance only includes the size for representing its primary structure; 
	It does not account for memory used by the objects that are elements of the list. (Because a list is a referential structure)
