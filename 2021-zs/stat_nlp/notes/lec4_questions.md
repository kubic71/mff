# Noisy channel method
## Noisy channel
- We have:
	-  some generating input distribution $p(input)$
	-  noisy channel encoder (transformation) model
		- $p_{enc}(\text{output}| \text{input})$
	-  encoded noisy output
- $f_{\text{enc}}(\text{input}, \text{noise}) \rightarrow \text{output}$
- can model some fuzzy transformation process we're interested in:
	- **OCR**
		- text -> print, scan -> image
	- **Handwriting**
		- text -> neurons, muscles -> paper -> scan -> image
	- **Speech**
		- text -> conversion to muscle contractions -> acoustic waves
	- **Machine translation**
		- text in target language -> translation -> source language
	- **PoS tagging**
		- sequence of tags and lemmas -> selection of inflected word forms -> text
- knowing 


It was presented mainly as an inverse (decoding) scheme.
In other words we want to estimate $p(\text{input} | \text{output})$
We can invert the probabilities using Bayes formula, assuming we have a the translation model $p(output|input)$ and the respective input and output distributions.
$$ p(input | output) = \frac{p(output | input) p(input)}{p(output)}$$
Moreover, if we aren't interested in the probabilities, but only in the most likely input, we can leave out $p(output)$, because it stays constant across one decoding.

- **p(input)** - ***the language model***

