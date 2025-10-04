**Notes**

**Upstream and Downstream dependencies**

- Imagine that we have three services: A, B, and C, as shown in the following figure:

	![[upstream-downstream-dependencies.png]]

- In this scenario, Service A makes requests to (and therefore depends on) Service B,
	which in turn depends on Service C.
- Because Service B depends on Service C, we can say that Service C is a downstream
	dependency of Service B. By extension, because Service A depends on Service B which
	depends on Service C, Service C is also a transitive downstream dependency of Service A.
- Inversely, because Service C is depended upon by Service B, we can say that Service B
	is an upstream dependency of Service C, and that Service A is a transitive upstream
	dependency of Service A.


**Cloud Native applications: What is cloud native**:
- Cloud native technologies empower organizations to build and run scalable applications in modern, dynamic environments such as public, private, and hybrid clouds.
- These techniques enable loosely coupled systems that are resilient, manageable, and
observable. Combined with robust automation, they allow engineers to make high-
impact changes frequently and predictably with minimal toil.

**Scalability**

- **Scalability** can be defined as the ability of a system to continue to behave as expected in the face of significant upward or downward changes in demand. 
- There are two different ways that a service can be scaled, each with its own associated
pros and cons:
- **Vertical scaling**: A system can be vertically scaled (or scaled up) by upsizing (or downsizing) the
hardware resources that are already allocated to it. 
- **Horizontal scaling**: A system can be horizontally scaled (or scaled out) by adding (or removing) service instances. 
- So what’s the difference between a service that’s horizontally scalable and one that’s
not? It all boils down to one thing: state. A service that doesn’t maintain any application state—or which has been very carefully designed to distribute its state between service replicas—will be relatively straightforward to scale out. For any other application, it will be hard. It’s that simple.

**Loose Coupling**

- Loose coupling is a system property and design strategy in which a system’s components
have minimal knowledge of any other components. Two systems can be said to be loosely coupled when changes to one component generally don’t require changes to the other.
- It could be said that “loose coupling” is just a restatement of the whole point of
microservice architectures: to partition components so that changes in one don’t necessarily 
affect another.

**Resilience**

- Resilience (roughly synonymous with fault tolerance) is a measure of how well a system withstands and recovers from errors and faults. 
- A system can be considered resilient if it can continue operating correctly—possibly at a reduced level—rather than failing completely when some part of the system fails.
- There are many ways of designing a system for resiliency. Deploying redundant com‐
ponents is perhaps the most common approach, but that also assumes that a fault
won’t affect all components of the same type. **Circuit breakers** and retry logic can be
included to prevent failures from propagating between components. Faulty components 
can even be reaped—or can intentionally fail—to benefit the larger system.

-  The resilience of a system is the degree to which it can continue to operate correctly 
in the face of errors and faults. Resilience, along with the other four cloud native properties, is just one factor that contributes to reliability.
- The reliability of a system is its ability to behave as expected for a given time interval.
Reliability, in conjunction with attributes like availability and maintainability, contributes to a system’s overall dependability.

**Manageability**

- A system’s manageability is the ease (or lack thereof) with which its behavior can be
modified to keep it secure, running smoothly, and compliant with changing requirements. 
A system can be considered manageable if it’s possible to sufficiently alter its behavior without having to alter its code.

