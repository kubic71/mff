# Knoledge-based agents

	
## Formal language
- we need **formal language** to
	- represent knowledge
	- reason with knowledge
- facts are described via **data structures**
- **programs** describe how to change the data structures
- inference
	- procedural (imperative)
	- declarative
		- prolog

### Natural languages
- no formal semantics
- natural language is more suitable for **communication** rather than for **reasoning**
- meaning is context-dependent
- ambiguity
	- not ideal for knowledge-representation
- *if thought corrupts language, language can corrupt thought*

### Propositional logic
- compositional semantic, declarative, context-independent, unambigous
- some properties are cumbersome to model
	- we don't have functions, relations

### Logical frameworks
- Propositional logic
- First-Order predicate logic
- Temporal logic
- Fuzzy logic

## First-order logic

### Syntax
- constants
- function symbols
- terms - recursive application of functions
- predicate symbols - connects terms (objects)


### Knowledge-base
- operations
	- **TELL** - add sentence (formula) to knoledge base
		- `TELL(KB, forall x (King(x) -> Person(x))`
	- **ASK** - querying sentences entailed by KB
		- output - True/False, listing all satisfying objects

### Axioms
- plain facts
	- Male(Jim)
- definitions
	- represented by equivalence relationships
- general info
	- usually implications (left to right, right to left)
- theorems
	- compressed, cached representation
	
### Knowledge engineering
- construction of the knowledge-base
- KB designed by the *real expert* - **knowledge engineer**
	- investigates a domain
	- learns what *concepts* are important
	- creates *formal representations of objects*
	- opimizes all of the above for the future queries

#### Process
1. identify the task
	- what is the range of questions?
2. knowledge acquisition
	- understand the domain, how it works
3. decide on suitable vocabulary of predicates, functions and constants
	- how to translate domain-level concepts to logic-level names
	- result -> **ontology** of the domain
4. encode general domain knowledge
	- which axioms hold in the domain?
5. encode description of a specific problem instance
6. pose queries
7. debug


### Hidden assumptions
- closed world assumption
	- True is only what is mentioned (like in prolog)
- unique name assumption 
	- unique constants have unique values


	