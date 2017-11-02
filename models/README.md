# Models for: A Dataset for Relations in Digital Humanities and its Evaluation with Word Embeddings

As mentioned,
we used different well-known techniques to create word-embedding models, for example word2vec, GloVe, fastText, and LexVec.
The models having names staring with `asoif_` are trained on the first for books of *A Song of Ice and Fire*,
and the models starting with `hp_` are trained on the complete *Harry Potter*. For copyright reasons the plain-text of
the books can not be included here.
**NEW:** the models with `_ngram` in their name are trained on n-gram data (created with Word2vec preprocessing tools).

The **method and parameters used for training**:
* \*`_w2v-default`: This is a word2vec model trained with the default settings: 200 vector dimensions, skip-gram, etc `-cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12`.
* \*`_w2v-ww12-300`: word2vec model with default settings, except: window size of 12, 300-dim.~vectors
* \*`_w2v-ww12-300-ns`: like the previous model, but with negative sampling on.
* \*`_w2v-CBOW:` same settings like w2v-ww12-300, but using CBOW instead of skip-gram method.
* \*`_glove`: Using the defaults (window size 15). Only change: 200-dim vectors instead of 50-dim.
* \*`_fasttext`: We used the default settings, except: 25 epochs, window size of 12
* \*`_lexvec`: We used the default settings, except: 25 epochs, window size of 12



