# A Dataset for Relations in Digital Humanities and its Evaluation with Word Embeddings

### Summary
Here you find the following:
    * **2 datasets each** for evaluating language models about the books **A Song of Ice and Fire** (GRR Martin) and **Harry Potter** (JK Rowling)
    * The dataset contain a large of number of task of type **analogy** and **doesnt-match**.
    * Your model can be tested especially easy if it is of type KeyedVector, ie. a [Gensim](https://radimrehurek.com/gensim) Word-Vectors model (eg. create with word2vec).
    * Furthermore, here you find scripts to create / extend the datasets -- by creating permutations of input data.
    * Finally, you can re-use the scripts to evaluate the data.

 
## The Datasets
The datasets are found in folder [datasets](datasets).
Like in the original word2vec-toolkit, the files to be evaluated are name `questions`\*.
There are four dataset:
* questions_soiaf_analogies.txt
* questions_soiaf_doesn_match.txt
* questions_hp_analogies.txt
* questions_hp_doesn_match.txt





