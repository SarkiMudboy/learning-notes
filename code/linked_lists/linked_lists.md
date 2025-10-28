## Linked Lists

There are disadvantages in using array-based python lists class in implementing the ADT of a classic stack, queue and deque:

1. The length of a dynamic array might be longer than the actual number of elements that it stores.
2. Amortized bounds for operations may be unacceptable in real-time systems.
3. Insertions and deletions at interior positions of an array are expensive.

- linked list, in contrast, relies on a more distributed representation in which a lightweight object, known as a node, is allocated for each element. Each node maintains a reference to its element and one or more references to neighboring nodes in order to collectively represent the linear order of the sequence

- Linked lists also has its setbacks however linked lists avoid the three disadvantages noted above for array-based sequences.

**Singly Linked List**

A singly linked list, in its simplest form, is a collection of nodes that collectively form a linear sequence. Each node stores a reference to an object that is an element of the sequence, as well as a reference to the next node of the list.

- The first and last node of a linked list are known as the head and tail of the list, respectively. By starting at the head, and moving from one node to another by following each node’s next reference, we can reach the tail of the list.

- We can identify the tail as the node having None as its next reference. This process is commonly known as traversing the linked list. Because the next reference of a node can be viewed as a link or pointer to another node, the process of traversing a list is also known as link hopping or pointer hopping.
