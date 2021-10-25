# Informed (heuristic) search


## Search with partial information
- POMDP
- agent doesn't know the current state (no sensors, unreliable sensors)
- **no sensors**
	- agent works with **belief state**
	- set of real states, possibly weighted
	- represents an estimate of the actual state
- **non-deterministic actions**
	- *contingency problems*
- **unknown actions**
	- effects discovered by exploration-exploitation


## Heuristic
- **notation**
	- $h(n)$ - heuristic
	- $g(n)$ - cost of current node
	- $f(n)$ - function guiding the search
		- always expanding the node with the lowest $f(n)$
- information, that can help the search algorithm
- **ideally** - distance to some goal state
- **in practice** - we can only estimate it

### Greedy best-first search
- $f(n) = h(n)$
- always expand the node with the lowest $h(n)$
- doesn't guarantee finding the shortest path
- may end up cycling

### A*
- also takes into account the $g(n)$
- $f(n) = g(n) + h(n)$
- most popular heuristic search algorithm
- doesn't extend already long paths

#### A* properties
- first some definitions...
- **admissible heuristic $h(n)$**
	- $h(n) \leq$ cost of the cheapest path from $n$ to goal
- **monotonous (consistent) heuristic $h(n)$**
	- $h(n) \leq c(n, a, n^`) + h(n^`)$
		- form of triangle inequality

- **Monotonous heuristic is admissible**
	- induction from start to goal
	- excercise: find admisible, which is not monotonous
- **For a monotonous heuristic, $f(n)$ is non-decreasing**
	- proof - trivial (TODO)
- **if $h(n)$ is an admissible, then A* in TREE-SEARCH is optimal**
	- tree-search - can visit node multiple times
	- optimal - first expanded goal is optimal
	- **proof** - contradition
		- let $G_2$ be sub-optimal goal from the fringe and $C^\star$ be the optimal cost
		- $f(G_2) = g(G_2) + h(G_2) = g(G_2) > C\star$, because $h(G_2) = 0$
		- but $C^\star \lt f(G_2) \leq f(n) \leq C^\star$
		- where $n$ is node in the frontier, which is on some shortest path to the goal
- in **GRAPH-SEARCH** also **optimal**
	- possible problem: reaching the same state for the second time using a better path
		- classical GRAPH-SEARCH would ignore this node, because it's already explored
	- we need to prove, that when we're closing a node $n$, it's for sure on a shortest path
	- ![[Pasted image 20211025095217.png]]
- for $h(n) = 0$ we obtain Dijkstra
- A* is **optimally efficient**
	- we don't do more work than Dijkstra
	- we can only do better
- **Time complexity**
	- still exponential
- **Space complexity**
	- has to keep all nodes in memory (keeping track of explored nodes)

### IDA (iterative deepening A*)
- **TODO**

### Recursive best-first search
- tree-search
- update the $f(n)$ estimates

### Simplified memory-bounded A*
- what if we run-out of memory in A*?
- IDA* and RBFS doesn't exploit all available memory!
- SMBA finds the optimal path that fits in memory
- idea - drop the node with the worst $f(n)$

### Weighted A (satisficing search)*
- **TODO**

## Looking for heuristics
### 8-puzzle
- 22 steps to goal in average, branching factor ~3
- state-space - $3^22 \approx 3.1 \times 10^{10}$
- $h_1(n)$ - number of misplaced tiles
- $h_2(n)$ - sum of tile's manhattan distances to the goal configuration
- which is better?
	- $h_2(n)$, because $h_2(n) \geq $h_1(n)$, while still being admissible

- $h_2(n)$ dominates $h_1(n)$, if $\forall n$, $h_2(n) \geq h_1(n)$
- if we have multiple admissible heuristics, we can take the $max(h_1(n), h_2(n), ... h_k(n))$ and get better heuristic
- we find heuristics by **problem relaxation**