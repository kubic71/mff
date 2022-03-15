# Word Classes
## The data
Get **TEXTEN1.ptg** and **TEXTCZ1.ptg**

These are your data. They are almost the same as the .txt data you have used so far, except they now contain the part of speech tags in the following form:
```
rady/NNFS2-----A----
,/Z:-------------
```

where the tag is separated from the word by a slash (`'/'`). Be careful: the tags might contain everything (including slashes, dollar signs and other weird characters). It is guaranteed however that there is no slash-word.

Similarly for the English texts (except the tags are shorter of course).

## The Task
Compute a full class hierarchy of words using the first 8,000 words of those data, and only for words occurring 10 times or more (use the same setting for both languages). Ignore the other words for building the classes, but keep them in the data for the bigram counts and all the formulas that use them (including the Mutual Information, the interim sums in the "Tricks", etc.). For details on the algorithm, use the Brown et al. paper available form SIS; some formulas are wrong in the paper, however, so please see the corrections in the slides (formulas for Trick #4). Note the history of the merges, and attach it to your homework. Now run the same algorithm again, but stop when reaching 15 classes. Print out all the members of your 15 classes and attach them too.

## Hints
The initial mutual information is (English, words, limit 8000):

`4.99726326162518` (if you add one extra word at the beginning of the data)
`4.99633675507535` (if you use the data as they are and are carefull at the beginning and end).

NB: the above numbers are finally confirmed from an independent source :-).

The first 5 merges you get on the English data should be:
```
case subject
cannot may
individuals structure
It there
even less
```

The loss of Mutual Information when merging the words `case` and `subject`:

`Minimal loss: 0.00219656653357569 for case+subject`


## Solution
### Algorithm
I implented the $O(V^3)$ version of the algorithm, incorporating most of the tricks, except the **skip-zero-bigrams** one.
It runs reasonably fast and it was enough for this assignment.


### Full history of word class merges
The full history for both datasets is computed by running the following commands:

```shell
$ python word_classes.py --dataset_path datasets/TEXTEN1.ptg --target_num_classes 1 --N 8000
$ python word_classes.py --dataset_path datasets/TEXTCZ1.ptg --target_num_classes 1 --N 8000 
```

The merge histories are exported to the `results` folder:

- [merge_results_words_CZ_N-8000_target_num-1.txt](results/merge_results_words_CZ_N-8000_target_num-1.txt) for Czech 
- [merge_results_words_EN_N-8000_target_num-1.txt](results/merge_results_words_EN_N-8000_target_num-1.txt) for English


#### Correctness
The first five merges for English with 8000 word limit are:
```
|112. I(D, E): 4.997263261625193, loss: 0.0021965665335752504, merging:
subject
case

|111. I(D, E): 4.995066695091618, loss: 0.002669139511099594, merging:
may
cannot

|110. I(D, E): 4.992397555580518, loss: 0.0026748091526132, merging:
individuals
structure

|109. I(D, E): 4.989722746427905, loss: 0.003479400370452801, merging:
It
there

|108. I(D, E): 4.986243346057452, loss: 0.0036556390622299872, merging:
less
even
```

The computed initial mutual information `I(D,E) = 4.997263261625193` is the same as the one in the **Hint** (`4.99726326162518`) up to 14 decimal places.

The computed loss of the first merge (`case` and `subject`) is  `0.0021965665335752504`, which equals the **Hint** (`0.00219656653357569`) up to 15 decimal places.

The first 5 merges also agree with the hint.
So I believe my implementation is correct.


### Stopping at 15 classes 
We run the `word_classes.py` again, but this time with `--target_num_classes 15` parameter.

```shell
$ python word_classes.py --dataset_path datasets/TEXTEN1.ptg --target_num_classes 15 --N 8000
$ python word_classes.py --dataset_path datasets/TEXTCZ1.ptg --target_num_classes 15 --N 8000 
```

The merge histories with the final 15 classes are again in the `results`:

- [merge_results_words_CZ_N-8000_target_num-15.txt](results/merge_results_words_CZ_N-8000_target_num-15.txt) for Czech
- [merge_results_words_EN_N-8000_target_num-15.txt](results/merge_results_words_EN_N-8000_target_num-15.txt) for English.


#### Final 15 Czech classes
Each class is on seperate line with the words separated by spaces.
```
,
a
o
před byl ? k po si při včera
nás státu J to jeho zákona NATO &slash; ČSFR jsou )
ve pro u za ale aby který které že
v
na
s Na OKD listopadu V "
i bylo jako však musí bude být budou pouze by
už mezi od ze : (
-
se
je z do
.
```

#### Final 15 English classes
```
.
its an wild same been
all some these each one distinct certain what
it they will we can there It must
of
in
the
by with at on has or is that
more under for domesticated domestic long slight short as which this
varieties races facts only me plants animals ; individuals structure most nature variation breeds state subject case conditions our several many
,
and
to my different their great ( any very such manner a
be I have from : between nearly how In The cannot may could would
are do see shall believe when if even less other not so but ) cases than differ much often species
```


# Tag classes
Use the same original data as above, but this time, you will compute the classes for tags (the strings after slashes). Compute tag classes for all tags appearing 5 times or more in the data. Use as much data as time allows. You will be graded relative to the other student's results. Again, note the full history of merges, and attach it to your homework. Pick three interesting classes as the algorithm goes (English data only; Czech optional), and comment on them (why you think you see those tags there together (or not), etc.).

## Solution
The classes for tags were computed on **all** given data, without any limit.

```shell
$ python word_classes.py --dataset_path datasets/TEXTCZ1.ptg --target_num_classes 1 --mode tags
$ python word_classes.py --dataset_path datasets/TEXTEN1.ptg --target_num_classes 1 --mode tags
```

Tag merge histories are again in the `results` directory:

- [merge_results_tags_CZ_N-224538_target_num-1.txt](results/merge_results_tags_CZ_N-224538_target_num-1.txt) for Czech
- [merge_results_tags_EN_N-221098_target_num-1.txt](results/merge_results_tags_EN_N-221098_target_num-1.txt) for English


### Three interesting merges
1. VBD (Verb, past tense) + VBN (Verb, past participle)
   - It makes sense to merge verbs that talk about the past, either in ordinary past tense or in past participle, into one general _Verb, past_ class
2. NN (Noun, singular or mass) + NNPS (Proper noun, plural)
   - Merging together different types of nouns
3. PRP$ (Possesive pronoun) + DT (Determiner)
   - The possesive pronoun can be often exchanged with determiner, while keeping the sentence grammatically correct
     - `My house` vs. `The house`

