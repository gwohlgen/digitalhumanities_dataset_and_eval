
BOOK_SERIES="ASIOF" ## new
#BOOK_SERIES="HP" ## new

# ------------------------------------------------------------

if BOOK_SERIES == "ASIOF":

    METHODS = [('coo_chapters','xxx'), ('coo_paragraphs','xxx'), ('coo_sentences','xxx'), 
               ('asoif_w2v-default','bin'), ## word 2 vec default settings
               ('asoif_w2v-ww12-300','bin'), ## default and: window-size 12, 300dim, hier.softmax, iter 15 
               ('asoif_w2v-ww12-300-ns','bin'), ## default and: window-size 12, 300dim, hier.softmax, iter 15 
               ('w2v_SG12_300_hs','bin'), 
               ('asoif_w2v-CBOW', 'bin'),
               ('w2v_CBOW0_300_hs_disamb', 'bin'),
               ('test', 'bin'), 
               ('glove', 'vec'), 
               ('asoif_glove', 'vec'), 
               ('asoif_lexvec', 'vec'), 
               ('asoif_fastText', 'vec'), # default and: -epoch 25 -ws 12
               ('doc2vec', 'bin')]

    MODEL_PATH="../asoif_models/"
    BOOKS_PLAIN="../got_data/soiaf4books.txt"

if BOOK_SERIES == "HP":
    METHODS = [
        ('coo_chapters', 'xxx'),
        ('coo_paragraphs', 'xxx'),
        ('coo_sentences', 'xxx'),
        ('hp_lexvec', 'vec'),
        ('hp_fasttext_default', 'vec'), 
        ('hp_fasttext', 'vec'),  # for paper!, 25 epoch
        ('hp_glove', 'vec'), 
        ('hp_w2v-default', 'bin'),
        ('hp_w2v-ww12-300', 'bin'),
        ('hp_w2v-ww12-300-ns', 'bin'),
        ('hp_w2v-CBOW', 'bin'),
    ]


    MODEL_PATH="../harry_potter_models/"

# -----------------------------------------------------
# for "doesnt_match" evaluation script
# -----------------------------------------------------

if BOOK_SERIES == "ASIOF":
    DOESNT_MATCH_FILE = "../datasets/questions_soiaf_doesn_match.txt"
    ANALOGIES_FILE = "../datasets/questions_soiaf_analogies.txt"

    ### which sections to show in the paper..
    ANALOGIES_SECTIONS = ['firstname-lastname', 'child-father', 'husband-wife', 'geo-name-location', 'houses-seats']
    DOESNT_MATCH_SECTIONS = [': family-siblings',  ': names-of-houses', ': archmaesters', ': rivers', ': free cities']


if BOOK_SERIES == "HP":
    DOESNT_MATCH_FILE = "../datasets/questions_hp_doesn_match.txt"
    ANALOGIES_FILE = "../datasets/questions_hp_analogies.txt"
    
    ANALOGIES_SECTIONS = ['firstname-lastname', 'child-father', 'husband-wife', 'pets-of-Hagrid', 'total']
    DOESNT_MATCH_SECTIONS = [': family-siblings', ': Hogwarts-houses', ': professors', ': wizarding-equipment', ': magic-creatures'] 

