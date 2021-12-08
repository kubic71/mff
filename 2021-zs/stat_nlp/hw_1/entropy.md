# Problem statement - Entropy of a Text
In this experiment, you will determine the conditional entropy of the word distribution in a text given the previous word. To do this, you will first have to compute $P(i,j)$, which is the probability that at any position in the text you will find the word $i$ followed immediately by the word $j$, and $P(j|i)$, which is the probability that if word $i$ occurs in the text then word $j$ will follow. Given these probabilities, the conditional entropy of the word distribution in a text given the previous word can then be computed as:

$$H(J|I) = -\sum_{i \in I,j \in J}P(i,j)\log_{2}P(j|i)$$

Perplexity is then computed simply as:

$$PX(P(J|I)) = 2^{H(J|I)}$$

Compute this conditional entropy and perplexity fo the file **TEXTEN1.txt**

## What to discuss
- how many words are there?
- number of unique tokens (EN vs. CZ)
- frequency of the most frequency word, number of words occuring only once
    - maybe plot hist



# Solution
We can compute $P(i, j)$  simply as $\frac{\#\text{bi-grams}(i, j)}{\#\text{all bi-grams}}$, and similarly $P(i)$ as $\frac{\#\text{uni-grams}(i)}{\#\text{all uni-grams}}$


$P(j | i)$ can therefore be computed as:

$$P(j | i) = \frac{P(i, j)}{P(i)} = \frac{\#\text{bi-grams(i, j)}}{\#\text{all bi-grams}}\cdot \frac{\#\text{all uni-grams}}{\#\text{uni-grams(i)}}$$ 

And because $\#\text{all uni-grams} = \#\text{all bi-grams}+1$, the difference is negligible, so we can compute $P(j|i)$ as follows:

$$P(j | i) = \frac{\#\text{bi-grams}(i, j)}{\#\text{uni-grams}(i)}$$

sidenote: The problems basically stems from the fact, that the language data are essentially infinite, but we are always working with some finite training set. In the extreme case, we can imagine a training comprising of only two words: $w_1, w_2, w_1$

The true $P(w_2 | w_1)=\frac{1}{2}$, because from two occurences of word $w_1$, the word $w_2$ follows only in one case. But according to our formula it would be $P(w_2 | w_1) = \frac{\#\text{bi-grams}(w_1, w_2)}{\#\text{uni-grams}(w_1)} =\frac{1}{2}$


If we would really want to nitpick, and we would want:

$$c_2(x, y) = \sum_{z}{c_3(x, y, z)}$$

Because then (in the case of trigram model):

$$1 = \sum_{z \in J}{P(z | x, y)}= \sum_{z \in J}{\frac{c_3(x, y, z)}{c_2(x, y)}} = \frac{1}{c_2(x, y)} \sum_{z \in J}{c_3(x, y, z)} = \frac{\sum_{z \in J}{c_3(x, y, z)}}{\sum_{z \in J}c_3(x, y, z)} = 1$$

If we didn't pad our training data $w_2, w_1, w_2, w_1$, then: 
$$c_1(w_1) = 2 \neq \sum_{y \in {w_1, w_2}} {c_2(w_1, y)} = 1$$

and:

$$c_1(w_2) = 2 \neq \sum_{y \in {w_1, w_2}} {c_2(w_2, y)} = c_2(w_2, w_2) + c(w_2, w_1) = 0 + $$


Therefore, we have to pad the training data with sufficient number of special symbols $\#$, resulting (for bigram model) in the following trainset $\#,w_2, w_1, w_2, w_1,\#$

Then:



## Language statistics



## Results

### Czech

Messup type|Messup prob|Entropy mean|Entropy min|Entropy max|Perplexity mean|Perplexity min|Perplexity max
|-|-|-|-|-|-|-|-|
character|0.0|4.747830945558377|4.747830945558377|4.747830945558377|26.868259177620114|26.868259177620114|26.868259177620114
character|1e-05|4.74771182112168|4.747587951770265|4.747796199591923|26.86604076505493|26.86373412547998|26.867612088412976
character|0.0001|4.746895248999014|4.7466662435906875|4.747200646064727|26.85083892365767|26.84657691971887|26.85652325919384
character|0.001|4.7382511991094685|4.736907205758305|4.739110579233642|26.69044268462023|26.665587441564174|26.70634389793559
character|0.01|4.6581428396786455|4.655832200022488|4.660712595310665|25.24881474638167|25.20839219291679|25.293812354173056
character|0.05|4.336964415307164|4.334520375552728|4.339747306481703|20.209556754136145|20.17533013102757|20.248558580930087
character|0.1|4.009074595548222|4.003593999186806|4.013968437147944|16.100992965486082|16.039908415144563|16.15566730880703
word|0.0|4.747830945558377|4.747830945558377|4.747830945558377|26.868259177620114|26.868259177620114|26.868259177620114
word|1e-05|4.747817580507374|4.747761585746187|4.747872015884386|26.868010278767873|26.866967475242877|26.869024068216905
word|0.0001|4.747757785717636|4.7476087882908695|4.747864509674422|26.866896750320524|26.86412211516313|26.868884271512947
word|0.001|4.7470695033988735|4.746727647892731|4.747481056852172|26.85408238357443|26.847719593917926|26.86174376008998
word|0.01|4.739222303586763|4.737809577135863|4.740582010083204|26.708417598550255|26.68227134838171|26.733596077791358
word|0.05|4.698993892777226|4.69691122479825|4.701762279097213|25.973970077400036|25.936487804101635|26.02384589278968
word|0.1|4.638169173409364|4.633841550413742|4.642131299518176|24.90168074401169|24.827060458710562|24.970127790754663

![](results/TEXTCZ1_entropy.png)

### English

Messup type|Messup prob|Entropy mean|Entropy min|Entropy max|Perplexity mean|Perplexity min|Perplexity max
|-|-|-|-|-|-|-|-|
character|0.0|5.2874846405274205|5.2874846405274205|5.2874846405274205|39.05633421084705|39.05633421084705|39.05633421084705
character|1e-05|5.287458284521222|5.287365141815407|5.287518542286584|39.05562072789242|39.05309930103211|39.05725200286547
character|0.0001|5.287033508626451|5.286644105210353|5.2872426345037935|39.04412342164779|39.03358604433767|39.049783224560464
character|0.001|5.283812864627775|5.2824584382303845|5.284926841368938|38.95706258878103|38.92050267710131|38.98715136077336
character|0.01|5.250066457057137|5.247225744592146|5.252239212048611|38.05641213886297|37.98152018909365|38.113738262596975
character|0.05|5.058783843507143|5.05389154096547|5.064145702475497|33.330877446249396|33.217959301303615|33.454901755551404
character|0.1|4.732797542581993|4.725116864500953|4.740007446063153|26.589878947648835|26.44855254063063|26.722951344320855
word|0.0|5.2874846405274205|5.2874846405274205|5.2874846405274205|39.05633421084705|39.05633421084705|39.05633421084705
word|1e-05|5.2874932946907|5.287448294002151|5.2875276108201446|39.05656849998282|39.0553502578172|39.05749751082365
word|0.0001|5.2876990908301975|5.287605017305358|5.287836680943516|39.062140238683284|39.05959316141203|39.06586573721266
word|0.001|5.289390107808867|5.288790317599533|5.289901934317892|39.107953949912584|39.09169722347897|39.121829530437765
word|0.01|5.307607790228046|5.305000483980068|5.309055604832067|39.60493660345087|39.5334096503095|39.644686298323194
word|0.05|5.379988385368776|5.378007951926059|5.382309861261614|41.642625338238545|41.58547921107922|41.70966619723279
word|0.1|5.457836045908288|5.453280339469338|5.460902566780672|43.95143229453386|43.812794741319685|44.04488455445509

![](results/TEXTEN1_entropy.png)
