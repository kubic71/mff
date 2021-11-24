# Adversarial search (games)
- **classical search** - looking for the shortest path to the goal
- **game search** - multi-agent search, each agent has its own utility functions


## Minimax


## Alpha-beta pruning
- don't explore **very bad state**, which cannot possibly influence the final decision
- compared to minimax - the complexity depends on the ordering of the searched nodes
- **alpha** - best choice so far somewhere along the path for MAX player
- **beta** - best choice so far somewhere along the path for MIN player

## Evaluation function
- we cannot afford to search the whole tree, only to some level d -> imperfect search
- something like a heuristic functions from A*

- expected value
	- we want the evaluation function to capture the chance of winning for a player p
	- 
	
- **material value**
	- the numerical contribution of each feature
		- chess: pawn = 1, knight = bishop = 3, rook = 5, queen = 9
	- combine the contriubtions
		- weighted sum of features:  $w_1 f_1(s) + w_2 f_2(s) + ... + w_n f_n(s)$
	
	
### Problems with cut off
- **Quiescent search**
	- if the estimate is not stable, then keep exploring beoynd the search depth
- **hoziron effect**
	- unavoidable bad situation can be delayed after the cut-off limit (horizon) and hence is not recognized as a bad state (horizon effect)
- **Singular extension**
	- prefer the promising moves in the exploration
	
	
	
## Simulation approaches
- heuristic alpha-beta tree search - explores **wide** but **shallow** tree
	- problem when branching factor big (Go)
- solution -> **deep but narrow** search of the game tree -> only promising nodes

### Pure Monte Carlo search
- do N simulations from the current state and the move with highest win percentage

### Monte Carlo tree search
- **playout** - simulation till the end of the game 
- **simulate** 
- **select**
- **expand**
- **backpropagate**