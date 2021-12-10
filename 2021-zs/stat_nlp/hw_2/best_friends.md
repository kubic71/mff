# Best Friends
In this task you will do a simple exercise to find out the best word association pairs using the pointwise mutual information method.

First, you will have to prepare the data: take the same texts as in the previous assignment, i.e.

**TEXTEN1.txt** and **TEXTCZ1.txt**

(For this part of Assignment 2, there is no need to split the data in any way.)

Compute the pointwise mutual information for all the possible word pairs appearing consecutively in the data, disregarding pairs in which one or both words appear less than 10 times in the corpus, and sort the results from the best to the worst (did you get any negative values? Why?) Tabulate the results, and show the best 20 pairs for both data sets.

Do the same now but for distant words, i.e. words which are at least 1 word apart, but not farther than 50 words (both directions). Again, tabulate the results, and show the best 20 pairs for both data sets.

## Best bigram friends

### Czech
![](results/best_bigram_friends_czech.png)

### English
![](results/best_bigram_friends_english.png)


## Best with distance no greater than 50
### Czech
![](results/best_distanced_friends_czech.png)

### English
![](results/best_distanced_friends_english.png)