## Problem formulation
- initial state
- goal test
    - have we solved the problem?
- path cost
    - sum of costs alongside the actions taken

## Abstractionn
- **valid** - can be expanded to the real world
- **useful** - makes the problem solving easier


### Toy-problem 8-queens
- incrementatal formulation - adding queens
- moving queens

### Route-finding problems
- graph-search

### Touring problems
- TSP

### Product assembly problem
- state = $\text{arm location} \times \text{components}$
- goal - assembled product
- successor - movement of "hinges"
- cost - total assembly time
- similar problem - protein folding

## State space search
- start in **initial state** (root node)
- 

```python
def tree_search(node, problem, strategy):
    if node.children() is empty:
        return False
    elif goal in node.children():
        return goal
    elif expand cheapest child from node.children() with respect to strategy.
```

- **fringe** (frontier)
    - set of nodes not expanded yet
- algorithm on top of the **fringe**

## Measuring the performance
- **completeness**
     - will solution be found given there is one
- **optimality**
    - will optimal solution be found
- **time/space complexity**
    - **branching factor b**
        - maximum number of successors for any given node
    - **depth d**
        - path length for the root to the shallowest goal node
    - **path length m**
        - maximum length of any path in the search space

## Uniformed (blind) search
- no additional information about states beyond problem formulation
    - only generate successors and distinguish goal state from non-goal state

## BFS
- shallowest unexpanded node selected for expansion
    - **FIFO** for the frontier
- BFS is **complete** (given the branching factor is finite)
- BFS is **not optimal**
- **time/space complexity** - $O(b^{d+1})$

## Uniform-cost search
- modifying BFS to find an optimal solution
- expand the node $n$ with the **lowest path cost $g(n)$**
    - zero-cost steps can cause cycling
- **completenes**
    - given cost of each step is lower-bounded by $\epsilon$
- **time (and space) complexity**
- $O(b^{1+\frac{C*}{\epsilon}})$
    - $C*$ is the path cost of optimal goal state

## DFS
- expand the deepest node - **LIFO**
    - implemented recursively
- backtracking
    - modify current state rather then generate all child nodes
- **problem**: inifinite search spaces
    - cycling
- **solution**
    - depth limit
    - but we may have no idea what the right depth-limit is

## Iterative deepening
- iterative depth-limited DFS

## Bidirectional search
- search from root and goal node at the same time
    - hope the searches meet in the middle
- problem: 
