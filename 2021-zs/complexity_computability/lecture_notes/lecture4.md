## Closure properties
- partially decidable languages closed under
	- complement
	- concatenation
- kleene star

### Post's theorem
- Language $L$ is decidable if and only if $L$ and $L_{complement}$ are partially decidable
- run machines in parallel


### Classes of languages
- PD - partially decidable languages
- co-PD - complement of partially decidable languages
- DEC
- Post: $DEC = PD \cap co \textendash PD$

### Computable functions
- characteristic functions of undecidable languages



### Enumerator
- PD - languages which we can enumerate
- enumerator isn't required to stop
- $NE = \{ \langle M \rangle | L(M) \neq \emptyset \}$
- language $L$ is decidable if an only if enumerator $E$ prints out $L$ in lexicographic order


# Reducibility and completeness
