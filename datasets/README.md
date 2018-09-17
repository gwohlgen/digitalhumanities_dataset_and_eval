
# Datasets

currently: 
* **hp:** Harry Potter
* **soiaf:** A Song of Ice and Fire
* Default datasets are with unigrams (single words), n-gram datasets have `_ngram` in their names.

## Task Types:
1. **Analogy Task:** 
    For example: Robb is to Stark what Cersei is to X (correct: Lannister).
    Classic example: man is to King what woman is to X (correct: Queen)


2. **`does not match` task:**
    The `doesnt_match()` function of Gensim takes a list of words (variable number of words) as input, an finds the one word that doesn't fit into the list.
    More formally this is called a **word intrusion** task.
    Here, we use a list of 4 items -- the algorithm has to find the ONE item that does not belong into the list.

    For **doesnt-match** task the dataset has provide 20 wrong candidates to be mixed in.
    Those 20 candidates are distributed equally of 4 categories of task difficulty. The first 5 candidates are
    hard to distinguish, in the second group the candidates are rather loosly semantically related to the task term,
    in the 3 group the relation is weak, for example only begin of the same term type (for example: named entity).
    The final group of 5 candidates is completly unrelated to the task terms.
    In the evaluations you measure the accuracy per difficulty category to better understand the performance
    of the system.


