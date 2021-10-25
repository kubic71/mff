## RAM $\rightarrow$ Turing machine
- 4-tape TM
	- input tape
		- number in binary, seperated by #
	- output tape - same format
	- RAM memory tape
	- auxiliary tape

### Transition function
- index of current instruction stored in the state
- state stored in the current state of M
- **TODO**

### Memory tape
- $(i_1)|([r_{i_1}])\#(i_2)|([r_{i_2}])\#(i_3)|([r_{i_3}])\#(i_4)|([r_{i_4}])...\#(i_n)|([r_{i_n}])$

### Simulating RAM operations (Addition)
- `add(r_i, r_j, r_k)`
	- $r_k \leftarrow [r_i] + [r_j]$
- $i, j, k$ hardcoded in the TM state
- copies contents or $r_i$ and $r_j$ to auxiliary tape
	- memory content may not have $r_i$ or $r_j$ initialized
	- in that case adds the register to the memory tape
- performs the addition on auxiliary tape
- finds $r_k$ position on the memory tape and copies the results
- overhead - polynomial time
- similarly other operations

## Decidability
- Language $L \subset \Sigma^\star$ is:
	- partially decidable if it is accepted by some TM
	- decidable if partially decidable and computation on any input terminates
- are all languages over a finite alphabet $\Sigma$ decidable
	- spoiler alert: No


### Lexicographical ordering of strings $\Sigma^\star$
- shorter strings first
- equal-lenght strings alphabetically
- $u \prec v$
- strings represented by the binary encoding of their indices

### Cardinality of the set of all languages
- Set of all languages $\{L | L \subset \Sigma^\star\}$ over finite alphabet $\Sigma$ is uncountable
	- Cantor theorem

### Numbering turing machines
- encoding turing machine as a natural number
- we restrict ourselves to only binary turing machines (not really a restriction)
- only necessary to encode transition function as natural number
- $\delta(q_i, X_j) = (q_k, X_l, Z)$ encoded as a string $C_i$
- TM code - $C_1\#C_2 ... \#C_n$
	- we convert that into binary (3 bits)
- **Godel number**
	- index of the binary code string of all valid TM codes
- not all strings are valid TM (code lenght divisible by 3)
	- one TM has infinite number of valid encodings (and inifinite number of Godel numbers)
		- by changing the numbers of the states
		- by having larger alphabet than we need
- **only countable number of TM**
	- $\rightarrow$ not all languages are partially decidable
- $\langle M \rangle$ is the binary encoding of the TM $M$


## Universal turing machine
- Universal turing machine $\mathcal{U}$ simulates $\mathcal M(x)$
	- 3 tape machine
- **input** - $\langle M, x \rangle$
	- 1st tape
- **universal language**
	- language accepted by $\mathcal U$
- 2nd tape
	- contains contents of $M$ (so also the output of $M$)
- 3rd tape
	- current state of $M$

### Computation
1. initialization
2. simulation
3. finalization

#### Initialization
- syntactic check
	- if input not valid TM encoding, reject
- determine block length $b$ for a symbol encoding on the 2nd tape
- Rewrite input of $M$ to the 2nd tape

#### Simulation
1. search $\langle M \rangle$ for current instruction
2. ...

#### Finalization
- accept if we are in the final state of $M$ (on the 3rd tape)
- convert the content of the 2nd tape

### Properties of Universal language
- partially decidable, but not decidable
	- partial decidability follows from the existence of $\mathcal U$

- **TODO**
	- universal language as a matrix

### Diagonal language
- complement of the universal language matrix diagonal
	- $DIAG = \{w_i | w_i \notin L(M_i)\}$
- not decidable
	- proof
		- by contradiction
		- TODO

