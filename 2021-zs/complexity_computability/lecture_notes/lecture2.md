### TM recap
- language of palindromes $\in$ TM
    - deletes outermost characters recursively

## Problems and languages
### Decision problem
- does given instance $x$ satisfies given condition
- $d(x) \rightarrow \{yes, no\}$
- defines equivalence relation over $\Sigma^\star$ 

#### Helloworld problem
- instance: source code $P$ of program in C and an input file $I$
- question: does $P$ with input $I$ print `Hello world`?


### Turing-decidable languages
- TM $M$ accepts word $w$
- $L(M)$ - language of words accepted by TM
- $M(w)\downarrow$ - the computation of TM $M$ over $w$ terminates
- $M(w)\uparrow$ - the computation of TM $M$ over $w$ doesn't terminate
- language $L$ is partially (Turing) decidable if it is accepted by some TM

### Turing computable functions
- $f(w)$ = what TM leaves on tape
- only partial function, because TM may not terminate
- inifinite number of TM that compute specific function $f(w)$

### Variants of TM
- nondeterministic TM
- one-sided tape
- TM with binary alphabet
- ...

They are equivalent

### 3-tape TM
- input tape (read-only), work-tape (RAM), output tape
- $\delta: Q \times \Sigma^k \rightarrow Q \times \Sigma^k \times \{L, N, R\}^k$

#### Palindromes
1. copy the string on the work tape
2. check

### Reducing the number of tapes
- theorem: each $k$-tape TM can be simulated by single-tape TM
- k tracks, 1 head track
- single-tape head movement simulated by moving whole track content


## Random Access Machine (RAM)
- can work only with **natural numbers**
- input
- program
    - instructions
        - READ($r_i$)
        - LOAD($n$, $r_i$)
        - JNZ($r_i$, $n$)
        - ADD($r_i$, $r_j$, $r_k$)
            - $r_k \leftarrow [r_j] + [r_k]$
        - SUB($r_i$, $r_j$, $r_k$)
            - if x - y < 0 -> SUB(...) = 0
        - COPY([$r_i$], $r_j$)
            - $r_j \leftarrow$ [$r_i$]
        - COPY($r_i$, [$r_j$])
            - $r_{[r_j]} \leftarrow r_i$


```
1. READ(r0)
2. READ(r1)
3. LOAD(1, r3)
4. JNZ(r0, 6)
5. JNZ(r3, 9)
6. ADD(r2, r1, r2)
7. PRINT(r2)
```
- memory
    - unbounded number of registers addressed 
    - initialialized by 0s
- indirect adressing
    - [$r_i$] - value of register $r_i$
    - $r_i$ - indirection
    - if we didn't have that, we couldn't really use the unbounded memory


### Programming on RAM
- variables
- cycles (for, while)
    - implemented using JNZ and (possibly) counter
- functions
    - inlining pieces of function code (no stack, but using preprocessor)
- recursion
    - while loop + stack
- storing $p$ arrays $A_1, A_2, ... A_j$ and scalar variables
    - zipping
        - $A_i[j]$ stored in $r_{i + j*(p+1)}$

### Languaages decidable with RAM
- alphabet $\Sigma = \{\sigma_1, \sigma_2, ... \sigma_k \}$
- input
    - indices to alphabet terminated with 0
- decision
    - PRINT(1) or PRINT(0)


### Arithmetic functions on RAM
- easy

### String functions on RAM
- PRINT(...) the characters

## Turing Machine $\rightarrow$ RAM
- for every TM $M$ there is RAM $R$ simulating it
    - $R$ simulates $M$ instruction by instruction
    - $R$ computes the same function as $M$
    - $R$ accepts the same language

- first convert to left-bounded TM
- Display
    - pair $(q,a)$ where $q \in Q$ is the current state, $a \in \Sigma$ is the symbol bellow head
- Configuration
    - tape content - array $T$
    - head position - variable $h$
    - state - variable $q$

