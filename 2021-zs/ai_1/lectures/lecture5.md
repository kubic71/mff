## Finding suitable heuristics

### Relaxation
- finding **admisible heuristic**
	- lower bound on the distance to the goal
- cost of optimal solution to a relaxed problem is a lower bound for the solution to the original problem

### Pattern database
- heurisitc takes the worst cost of a pattern that matches the current state

### Heuristic domination
- taking maxium of multiple admissible heuristics

## Local search
- we are not interested in the path, but only in the goal state
	- e.g. 8-queens
- somewhat eleviates memory consumption
- keep only a single state in memory
- action changes somehow this state
- **objective function** - guides the search
- **examples**
	- **SGD** - objective 
- may get stuck in local optimum
- may get stuck cycling in a plateaux

### Hill climbing
- greedy algorithm, doesn't look ahead
- always pick best state in a local neighborhood

#### stochastic HC
- prefers steepest ascent, but can also go down


#### First-choice HC
- pick first better neighbor than current current-state

#### Random-restart HC
- restart when stuck in local-optimum
- if HC has a probability *p* of success, then the expected number of restarts required is $\frac{1}{p}$
- very efficient method for the N-queens problems ($p \approx 0.14$, i.e. 7 restarts)

#### Simulated annealing
- combines HC and random walk
- pick a radnom move
	- if it's better, go there
	- if it's worse, then pick it with a probability given by a *temperature*
		- $e^{\Delta E / T}$
		- $\Delta E = Value(current) - Value(next)$
- *temperature* is gradually decreased

### Local Beam search
- better exploit avaialble memory
- keep track of *k* states rather than only 1
- generate neighbors of each of the *k* states
- select (stochastically) k best next states
	- almost like evolutionary algorithm, but without crossover

### Genetic algorithms
- Local beam search + crossover


## Stochastic environment
### And-Or search
- TODO


## Offline vs. online
- **offline**
	- we solve the problem, then execute sequence of actions
- **online**
	- interleaving of computing and acting
		- select an action
		- execute an action
		- observe the environment
	- RL agent
- **competitive ratio**
	- quality of the online solution / quality of the best solution
	- but can be very bad, if some actions are **irreversible** - game over
- **claim** - no algorithm can avoid dead-ends in all state spaces


### Online-DFS
- unexplored and unbacktracked stacks
- all actions are reversible


### Learning real-time A*
- remember visited states and hence leave optima
- learn better value of the heuristic online
- Hillclimbing with updated heuristic


