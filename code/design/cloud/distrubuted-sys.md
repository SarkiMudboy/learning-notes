## What is a distrubuted system??

**Primer**

A set of networked computers co-operating together to complete tasks.

Examples:

- MapReduce
- P2P File sharing
- Large Storage systems

Reasons:

- High performance: Parallel resources (CPU, Memory)
- Fault tolerance
- Problems naturally spread out in space - Banking systems, cloud stuff
- Security - Split up and isolate untrusted code/software.

- Always try to solve your problems on a single computer before your distribute, its always easier.

Challenges:

- Concurrency
- Failure patterns - Partial failures (network, computers)
- Perfomance

- _Abstractions_: Ideally we want to build abstractions that hide the distrubuted nature of these applications (storage, computation, comms e.t.c). Implemetation may include i.e. Remote Procedure Calls, Threads, Concurrency control (locks, atomic operations e.t.c).

- _Perfomance_: We want to be able to get increase in perf when we add more resources i.e. More Computers = More perf (Horizontal scalability). It isn't infinite.

- _Fault tolerance_: Ability to mask or hide inevitable failures that occur when working with distributed systems. Examples include _availability_ (keep providing service when there is a failure), _recoverability_ (continue/recover without any loss of correctness after failure/fix). Tools might include non-volatile storage to persist state befor failure, replication and problems with out-of-sync replicas.

- _Consistency_: We also want our APIs to be clear and consistent with behaivour and results across the system. For example the system might expose stale data to clients due to inconsistent replicas. For these reason we want to define rules for our APIs. An example is in a distributed key-value store, consistency may be of two types:

Types of Consistency

- Strong consistency: State is consistent across board.
  - Expensive (i.e. Lots of network communication to ensure replicas are updated with latest state)
- Weak Consistency: State is not guraunteed to be consistent.
  - Cheaper.
