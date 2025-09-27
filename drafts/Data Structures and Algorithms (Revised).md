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
  array. We will refer to each location within an array as a cell, and will use an
  integer index to describe its location within the array, with cells numbered starting
  with 0, 1, 2, and so on.

- Each cell of an array must use the same number of bytes. This requirement is
  what allows an arbitrary cell of the array to be accessed in constant time based on
  its index. In particular, if one knows the memory address at which an array starts,
  the number of bytes per element (e.g., 2 for a Unicode character), and a desired index
  within the array, the appropriate memory address can be computed using the calculation,
  _start + cellsize _ index.\*

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
  can be produced by using the **_deepcopy_** function from the copy module.

- Python allows you to query the actual number of bytes being used for the primary storage of any object. This is done using the _getsizeof_ function of the sys module.

- **Note** - _getsizeof_ for a list instance only includes the size for representing its primary structure;
  It does not account for memory used by the objects that are elements of the list. (Because a list is a referential structure)

- Strings are represented using an array of characters (not an array of references).
  We will refer to this more direct representation as a **_compact array_** because the array is
  storing the bits that represent the primary data (characters, in the case of strings).

- Compact arrays have several advantages over referential structures in terms
  of computing performance. Most significantly, the overall memory usage will be
  much lower for a compact structure because there is no overhead devoted to the
  explicit storage of the sequence of memory references (in addition to the primary
  data).

- Another important advantage to a compact structure for high-performance computing
  is that the primary data are stored consecutively in memory. Note well that
  this is not the case for a referential structure. That is, even though a list maintains
  careful ordering of the sequence of memory addresses, where those elements reside
  in memory is not determined by the list. Because of the workings of the cache and
  memory hierarchies of computers, it is often advantageous to have data stored in
  memory near other data that might be used in the same computations.

- Primary support for compact arrays is in a module named array. That module
  defines a class, also named array, providing compact storage for arrays of primitive
  data types. The public interface for the array class conforms mostly to that of a Python list.
  However, the constructor for the array class requires a type code as a first parameter,
  which is a character that designates the type of data that will be stored in the array.
  The type code allows the interpreter to determine precisely how many bits are
  needed per element of the array and are formally based upon the native data types used by the
  C programming language (the language in which the the most widely used distribution of Python is implemented).

**Dynamic Arrays**

- Because the system might dedicate neighboring memory locations to store other
  data, the capacity of an array cannot trivially be increased by expanding into sub-
  sequent cells. In the context of representing a Python tuple or str instance, this
  constraint is no problem. Instances of those classes are immutable, so the correct
  size for an underlying array can be fixed when the object is instantiated.
  Python’s list class presents a more interesting abstraction. Although a list has a
  particular length when constructed, the class allows us to add elements to the list,
  with no apparent limit on the overall capacity of the list. To provide this abstraction,

- Python relies on an algorithmic sleight of hand known as a dynamic array.
  The first key to providing the semantics of a dynamic array is that a list instance
  maintains an underlying array that often has greater capacity than the current length
  of the list. For example, while a user may have created a list with five elements,
  the system may have reserved an underlying array capable of storing eight object
  references (rather than only five). This extra capacity makes it easy to append a
  new element to the list by using the next available cell of the array.
  If a user continues to append elements to a list, any reserved capacity will
  eventually be exhausted. In that case, the class requests a new, larger array from the
  system, and initializes the new array so that its prefix matches that of the existing
  smaller array. At that point in time, the old array is no longer needed, so it is
  reclaimed by the system. Intuitively, this strategy is much like that of the hermit
  crab, which moves into a larger shell when it outgrows its previous one.

- The strategy of replacing an array with a new, larger array might at first seem
  slow, because a single append operation may require Ω(n) time to perform, where
  n is the current number of elements in the array. However, notice that by doubling
  the capacity during an array replacement, our new array allows us to add n new
  elements before the array must be replaced again. In this way, there are many
  simple append operations for each expensive one. This fact allows
  us to show that performing a series of operations on an initially empty dynamic
  array is efficient in terms of its total running time.

**_ctypes.py_object_** -> Represents the C [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject "PyObject") type:

- From [docs](https://docs.python.org/3/c-api/structures.html#c.PyObject)
  "All object types are extensions of this type. This is a type which contains the information Python needs to treat a pointer to an object as an object. In a normal “release” build, it contains only the object’s reference count and a pointer to the corresponding type object. Nothing is actually declared to be a [`PyObject`](https://docs.python.org/3/c-api/structures.html#c.PyObject "PyObject"), but every pointer to a Python object can be cast to a [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject "PyObject")\*. Access to the members must be done by using the macros [`Py_REFCNT`](https://docs.python.org/3/c-api/refcounting.html#c.Py_REFCNT "Py_REFCNT") and [`Py_TYPE`](https://docs.python.org/3/c-api/structures.html#c.Py_TYPE "Py_TYPE")."

- The idea that we can sometimes get a tighter bound on a series of operations by considering the cumulative effect, rather than assuming that each achieves a worst case is a technique called **_amortization_**.

**P1** - Let S be a sequence implemented by means of a dynamic array with initial capacity one, using the strategy of doubling the array size when full. The total time to perform a series of n append operations in S , starting from S being empty, is **O(n)**.

**Geometric Increase in Capacity**

- Although the proof of Proposition 1 relies on the array being doubled each time
  we expand, the O(1) amortized bound per operation can be proven for any geometrically
  increasing progression of array sizes. When choosing the geometric base, there exists a tradeoff between run-time efficiency and memory usage. With a base of 2 (i.e., doubling the array), if the last insertion causes a resize event, the array essentially ends up twice as large as it needs to be. If we instead increase the array by only 25% of its current size (i.e., a geometric base of 1.25), we do not risk wasting as much memory in the end, but there will be more intermediate resize events along the way. The key to the performance is that the amount of additional space is proportional to the current size of the array.

**Arithmetic Increase**

- To avoid reserving too much space at once, it might be tempting to implement a
  dynamic array with a strategy in which a constant number of additional cells are reserved each time an array is resized. Unfortunately, the overall performance of such a strategy is significantly worse. At an extreme, an increase of only one cell causes each append operation to resize the array, leading to a familiar 1 + 2 + 3 + · · · + n summation and **_Ω(n^2_**) overall cost.

- **P2** - Performing a series of n append operations on an initially empty dynamic array using a fixed increment with each resize takes **_Ω(n^2)_** time.

- A lesson to be learned from Propositions 1 and 2 is that a subtle difference in an algorithm design can produce drastic differences in the asymptotic performance, and that a careful analysis can provide important insights into the design of a data structure.

**Memory Usage and Shrinking an Array**

### Cycle Detection (In an array)

Several algorithms are known for finding cycles quickly and with little memory. Robert W. Floyd's tortoise and hare algorithm moves two pointers at different speeds through the sequence of values until they both point to equal values.
Alternatively,Brent's algorithm is based on the idea of exponential search. Both Floyd's and Brent's algorithms use only a constant number of
memory cells, and take a number of function evaluations that is proportional to the distance from the start of the sequence to the first repetition. Several other algorithms trade off larger amounts of memory for fewer function evaluations.
