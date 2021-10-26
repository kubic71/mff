## Golden rule of statistical NLP
- interested in $\argmax_A \, p(A|B)$
	- probability of next word in a sentence (for instance in MT)
- from Bayes rule, $p(A|B) = \frac{p(B|A) \cdot p(A)}{p(B)}$
	- the context senctence is kept constant when changing A
	- therefore $\argmax_A \frac{p(B|A) \cdot p(A)}{p(B)} = \argmax_A \, p(B|A) \cdot p(A)$

# Information Theory
## Entropy
- measure of uncertainty
-  in stat nlp, we're trying to get low entropy (and be less uncertain)
-  Let $p_X(x)$ be a distribution of random variable X
-  $\frac{1}{p(x)}$ - amount of information in an event $X=x$
	-  $\log_2 \frac{1}{p(x)}$ - number of bits of information in that event
- entropy is the expected number of bits of information in an event
-  $H(X) = \sum_{x \in \Omega} p(x) \log_2 \frac{1}{p(x)} = - \sum_{x \in \Omega} p(x) \log_2 p(x) = - \sum_{x \in X} p_X(x) \log_2 p_X(x)$
-  another interpretation of entropy is that from **coding theory**
	-  $p(x)$ is the distribution of words we want to encode
	-  encoding - $en(x) \rightarrow \{0, 1\}^k$
		-  assigns unique binary strings to each word
	-  if we use optimal binary coding scheme (Huffman tree), the entropy $H(p)$ is the expected lenght of the encoded binary string (in bits)

### Perplexity
- $G(p) = 2^{H(p)}$

## Joint Entropy and Conditional Entropy
- **Joint entropy**
	- $H(X, Y) =  - \underset{x \in X, y \in Y}\sum p_{X,Y}(x, y) \log_2 p_{X, Y}(x, y)$
	- note: for simplicity, we will denote $p_{X, Y}(x, y)$ just by $p(x, y)$
- **Conditional entropy**
	- what is the entropy of Y, when we already know X?
		- we want to compute the entropy of distribution $p(y|x)$, where $x$ is constant
		- $H(Y | X=x) = - \sum_{y \in Y} p(y|x) \log_2 p(y|x)$
	- conditional entropy is the expected value weighted by $p(x)$
	$$H(Y|X) = \sum_{x \in X} p(x) (-\sum_{y \in Y} p(y|x) \log_2 p(y|x)) =  - \underset{x \in X, y \in Y}{\sum} p(x) p(y | x) \log_2 p(y | x)=$$
	$$=-\underset{x \in X, y \in Y}{\sum} p(x, y) \log_2 p(y | x)$$
- joint and conditional entropy relation
	- $p(x,y) = p(x | y)p(y)$
	$$H(X, Y) = - \sum_{x \in X, y \in Y} p(x, y) \log p(x, y) = -\sum_{x \in X, y \in Y} p(x, y) \log p(x|y)p(y)=$$
	$$= -\sum_{x \in X, y \in Y} p(x, y) (\log p(x|y) + \log p(y))=$$
	$$=-\sum_{x \in X, y \in Y} p(x, y) \log p(x|y) -\sum_{x \in X, y \in Y} p(x, y) \log p(x|y) = H(X|Y) + H(Y)$$
	- by symmetry
	$$H(X,Y) = H(X|Y) + H(Y) = H(Y|X) + H(X)$$
	
## Cross entropy
- recall, that $H(q)$ is the average number of bits needed to encode each message, given some word distribution $q(x)$
	- $H(q) = - \mathbb{E}_q[\log q]$
- cross entropy $H(p, q)$ is the number of bits we'll need, if we code optimally with respect to $q(x)$, but change the generating distribution to $p(x)$
	- $H(p, q) = - \sum_{x \in \Omega} p(x) \log_2 q(x) = - \mathbb{E}_p [ \log q ]$
	
## Kullback-Leibler divergence
- extra message length of coding optimized for $q$ compared to the optimal message length for $p$
	$$D_{KL}(p || q) = H(p, q) - H(p) = \mathbb{E}_p [-\log q] - \mathbb{E}_p [-\log p]$$
- $D_{KL}(p || q) \geq 0$
	- **Gibbs' inequality**
	- or equivalently: $H(p, q) \geq H(p)$
	- extra message lenght is always positive, because there cannot be better coding for $p$ than the optimal one for $p$
	- $D_{KL}(p || q) = 0$ only if $p = q$
		- $H(p, p) - H(p) = \mathbb{E}_p [-\log p] - \mathbb{E}_p [-\log p] = 0$
		- $D_{KL}(p || q)$ is similar to distance of $q(x)$ to $p(x)$
		- but only similar, doesn't satistfy triangle inequality, not symmetric)
- equivalent formulation
$$D_{KL}(p || q) = -\sum_{x \in \Omega} p(x)\log q(x) + \sum_{x \in \Omega} p(x)\log p(x)= \sum_{x \in \Omega} p(x)(\log p(x) - \log q(x)) =$$
$$= \sum_{x \in \Omega} p(x)\log \frac{p(x)}{q(x)} = \mathbb{E}_p[\log \frac{p(x)}{q(x)}]$$