# Information Theory (part 2)
## Mutual Information I(X, Y)
- we are given two random variables $X, Y$ with distributions $p_X(x)$, $p_Y(y)$ and their joint distribution $p_{X, Y}(x, y)$
	- we shorten $p_X(x), p_Y(y), p_{X, Y}(x, y)$  to $p(x), p(y), p(x, y)$
$$I(X, Y) = D_{KL}(p(x, y)\, || \, p(x)p(y)) = \sum_{x \in X, y \in Y} p(x,y) \log \frac{p(x, y)}{p(x)p(y)}$$
- if $X$ and $Y$ would be independent, $p(x, y)=p(x)p(y)$ and the mutual information $I(X, Y)=0$
- $I(X, Y)$ is symmetric
- because $\frac{p(x, y)}{p(y)} = p(x | y)$, we have

$$I(X, Y)= \sum_{x \in X, y \in Y} p(x,y) \log \frac{p(x | y)}{p(x)} = -\sum_{x \in X, y \in Y}{p(x,y) \log p(x)} + \sum_{x \in X, y \in Y} p(x,y) \log p(x | y) =$$
$$=H(X) - H(X|Y)$$
- interpreted as ***the number of bits the knowledge of Y lowers the entropy of X***

### Properties
- symmetry
$$I(X, Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$$
- mutual information as intersection
	- because 
		$$H(X, Y) = H(X|Y) + H(Y) \rightarrow H(X|Y)=H(X,Y) - H(Y)$$
	- then
		$$I(X,Y) = H(X) + H(Y) - H(X,Y)$$
	- can be viewed as intersection of information
		- $|A \cap B| = |A| + |B| - |A \cup B|$
		- $H(X, Y)$ represents the union (all) of information of X and Y