# Models for: A Dataset for Relations in Digital Humanities and its Evaluation with Word Embeddings

As mentioned,
we used different well-known techniques to create word-embedding models, for example word2vec, GloVe, fastText, and LexVec.
The models having names staring with `asoif_` are trained on the first for books of *A Song of Ice and Fire*,
and the models starting with `hp_` are trained on the complete *Harry Potter*. For copyright reasons the plain-text of
the books can not be included here.

**NEW:** the models with `_ngram` in their name are trained on n-gram data (created with Word2vec preprocessing tools).

The **method and parameters used for training**:
* \*`w2v-default`: This is a word2vec model trained with the Gensim default settings, which are CBOW, word window of 5 words, negative sampling (5 samples), 5 epochs. The only change made to the defaults: 300-dim vectors instead of 100-dim.
* \*`w2v-ww12-i15-ns`: word2vec with skip-gram algorithm, window size of 12, 15 epochs, and negative sampling with 15 noise words, 300 dimensions.
* \*`w2v-ww12-i15-hs`: Like the previous model, but with hierarchical softmax instead of negative sampling.
* \*`w2v-CBOW`: Same settings like `w2v-ww12-i15-ns`, but using CBOW instead of skip-gram method.
* \*`GloVe`: Using the defaults. Only changes: 300-dim vectors instead of 50-dim, window size 12.
* \*`fastText-default`: We used the default settings, which are CBOW algorithm, 5 epochs, word window size of 5, negative sampling (5 samples). Exception from default: 300-dim. vectors.
* \*`fastText-ww12-i15-ns`: Same settings like in `w2v-ww12-i15-ns`.
* \*`LexVec`: We used the default settings, except: 25 epochs, window size 5 (instead of default: 2).

