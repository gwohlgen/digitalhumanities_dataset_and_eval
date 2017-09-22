
from config import *
import gensim.models

def load_models(mode=None, emb_type=None):

    if emb_type == "vec": binary = False
    elif emb_type == "bin": binary = True
    else: raise Exception()

    print "\n\n**** Model:", mode, " binary:", binary

    if mode == "doc2vec":  
        word_model = gensim.models.doc2vec.Doc2Vec.load(MODEL_PATH + mode + ".model")
    else:
        word_model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_PATH + mode + ".model", binary=binary)
        #word_model = gensim.models.Word2Vec.load_word2vec_format(MODEL_PATH + mode + ".model", binary=binary)   

    word_model.init_sims(replace=True) # clean up RAM

    # not used currently!
    bigram_model = None
   
    return word_model, bigram_model 


if __name__ == "__main__":
    model, crap = load_models(mode='asoif_w2v-default', emb_type='bin')
    print '\n\nMODEL', model
 
