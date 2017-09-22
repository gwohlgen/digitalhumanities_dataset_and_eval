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
* `datasets/questions_soiaf_analogies.txt`: Analogies relation test data for *A Song of Ice and Fire*
* `datasets/questions_soiaf_doesn_match.txt`: Doesnt_match task test data for *A Song of Ice and Fire*
* `datasets/questions_hp_analogies.txt`: Analogies relation test data for *Harry Potter*
* `datasets/questions_hp_doesn_match.txt`: Doesnt_match task test data for *Harry Potter*

If you want to extend or modify the test data, edit the respective source files in the folder [datasets](datasets):
`hp_analogies.txt`, `hp_does_not_match.txt`, `soiaf_analogies.txt`,`soiaf_does_not_match.txt`.

After modifying the test data run the following command to re-create the datasets.
```
    cd datasets 
    python create_analogy_questions.py
```







