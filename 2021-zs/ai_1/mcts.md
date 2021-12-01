- jak vybiram leaf pri expanzi?


Outcome result
- simulation
    - need simple agent policy
    - don't want to neccesarily want to use super-inteligent agent
- heuristic function


# MCTS


## Pseudo-code
```
while got time:
    node = select(root)
    lef = expand(node)
    outcome = simulate(leaf) # rollout
    propagate(outcome)

```

## Select
- $UCB(node) = exploit(node) + c \cdot explore(node)$
- jdu podle UCB, az narazim na leaf, ten selectnu
- definitions of leaf:
    - not all child nodes expanded
    - doesn't have any children
        - wrong definition, would end up with linked-list, not a tree
