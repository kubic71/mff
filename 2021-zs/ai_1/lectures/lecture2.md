## Agent
- percieves its environments through sensors
- acts through actuators
- examples:
    - humans (eyes, ears, nose -> hands legs, mouth)
    - robot (camera, lidar -> arms, wheels)
    - software agent (keyboard, recieving packets -> screen, sending packets)
- formal def:
    - agent determined by the agent function (table)
    - $V^* \rightarrow A$
    - $V^*$ is the set of all posible histories (sequences) of percepts
- the agent function (infinite table) is implement by agent program (finite)

### Vacuum-cleaner
- percepts:
    - location (A, B)
    - property (clean, dirty)

## Performance measure
- who defines it?
    - agent designer
    - environment (external reward)
- how to set the performance measure?
    - function of the state of the environment
- example (vacuum cleaner)
    - such up as much dirt as possible
    - consequence: suck up, dump, suck up, dump...
        - paperclip maximizer

## Rational agent
*Agent maximizing expected performance measure*
- different from omniscience
    - rational agent doesn't know the entire state of the world, has only limited information
- should be **autonomous** - compensating for incomplete knowledge and learning
- **task environment** - sensors + actuators + performance measure + environment

## Environment
- fully / partially observable
- deterministic / stochastic
    - strategic - only agents modify the environment
- episodic
- static / dynamic
    - static - environment is not changing
    - semidynamic - environment static, but performance score changes
- discrete / continuous
- single / multi agent
    - competitive vs cooperative
    - which entities are viewed as agents?

- **easiest** - fully observable, deterministic, episodic, static, discrete, single-agent
- **most challenging** - partially observable, stochastic, sequential, dynamic, continous, multi-agent

## Structure of agents
- agent = architecture (hardware) + program (software)
- takes in percepts and return action

### Table-driven agent
- uses entire percept history to index its action table

```python
def table_agent(percept) -> action
    history.append(percept)
    return table.lookup(history)
```

### Simple reflex agent
```python
def percept_agent(percept) -> action
    return table.lookup(percept)
```
- if the environment is partially observable, agent may end up in an infinite loop
- example:
    - Eliza


### Model-based agent
- reflex agent with internal memory modelling environment state

```python
def percept_agent(percept) -> action
    # the state update depends on the enviroment and sensor model
    state.update(percept, last_action)
    action = table.lookup(state)
    last_action = action
    return action
```
- makes decisions based only on the past

### Goal-based agent
- goal guides actions
    - performance measure (reward function) - more fine-grained goal description (heuristic)
- considers future (planning, search)
    - MCTS

### Utility-based agent
- encodes the goal in the utility function (reward-function - like discounted return)
- $u(state) \rightarrow reward$
- maximizes its own expected reward


### Detour: Environment representation
- atomic
    - discrete
    - 1D array
- factored representation
    - multi-dimensional attribute vector
- structured representation
    - used in first-order logic

### General learning agent
- can improve its own program
- performance element
    - the agent with its program
- learning element
    - responsible for making improvements
- critic
    - feedback on how well the agent is doing
- problem generator
    - responsible for exploration
    - intrinsic motivation

