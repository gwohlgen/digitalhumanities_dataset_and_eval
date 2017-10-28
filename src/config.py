
"""
    This is the central config file
    @author: Gerhard Wohlgenannt (2017), ITMO University, St.Petersburg, Russia

    Here you can change pathes, add models, add new BOOK_SERIES, new dataset (towards the end of the file).
    But just to start with existing datasets and models, no change is needed
"""


import sys

NGRAMS=True

## use the input parameter to select the book series
if len(sys.argv) < 2:
    raise Exception("We need two command line arguments!")
if sys.argv[1].lower() == 'asoif':
    BOOK_SERIES="ASIOF"
elif sys.argv[1].lower() == 'hp':
    BOOK_SERIES="HP" ## new
else:
    raise Exception("the book series must be either *ASOIF* or *HP*")


MODEL_PATH="../models/"


if BOOK_SERIES == "ASIOF":
    METHODS = [
        ('ppmi_svd', 'bin'), #ppmi+svd with 300 dim
        ('asoif_w2v-default','bin'), ## word 2 vec default settings
        ('asoif_w2v-ww12-300','bin'), ## default and: window-size 12, 300dim, hier.softmax, iter 15 
        ('asoif_w2v-ww12-300-ns','bin'), ## default and: window-size 12, 300dim, hier.softmax, iter 15 
        ('asoif_w2v-CBOW', 'bin'),
        ('asoif_glove', 'vec'), 
        ('asoif_lexvec', 'vec'), 
        ('asoif_fastText', 'vec'), # default and: -epoch 25 -ws 12
        ('asoif_w2v-ww12-300-ns-ngram','bin'), ## Skip-gram, window-size 12, 300dim, hier.softmax, iter 15, -negative 15
    ]

    if NGRAMS:
        METHODS = [
            ('asoif_w2v-ww12-300-ngram','bin'), ## Skip-gram, window-size 12, 300dim, hier.softmax, iter 15, no neg-sampling
            ('asoif_w2v-ww12-300-ns-ngram','bin'), ## Skip-gram, window-size 12, 300dim, hier.softmax, iter 15, -negative 15
            ('asoif_fastText_ngram', 'vec'), # default and: -epoch 25 -ws 12
            ('asoif_lexvec_ngram', 'vec'), # default and: -epoch 25 -ws 12
        ]

if BOOK_SERIES == "HP":
    METHODS = [
        ('hp_lexvec', 'vec'),
        ('hp_fasttext', 'vec'),  # for paper!, 25 epoch
        ('hp_glove', 'vec'), 
        ('hp_w2v-default', 'bin'),
        ('hp_w2v-ww12-300', 'bin'),
        ('hp_w2v-ww12-300-ns', 'bin'),
        ('hp_w2v-CBOW', 'bin'),
    ]

    if NGRAMS:
        METHODS = [
        ('hp_lexvec_ngram', 'vec'),
        ('hp_fastText_ngram', 'vec'),  # for paper!, 25 epoch
        # ('hp_glove_ngrams', 'vec'), 
        # ('hp_w2v-default_ngrams', 'bin'),
        # ('hp_w2v-ww12-300_ngrams', 'bin'),
        # ('hp_w2v-ww12-300-ns_ngrams', 'bin'),
        # ('hp_w2v-CBOW_ngrams', 'bin'),
    ]




# -----------------------------------------------------
# for "doesnt_match" evaluation script
# -----------------------------------------------------

if BOOK_SERIES == "ASIOF":
    PRINT_DETAILS = False ## verbose debugging of eval results

    if NGRAMS:
        ANALOGIES_FILE = "../datasets/questions_soiaf_analogies_ngram.txt"
        DOESNT_MATCH_FILE = "../datasets/questions_soiaf_doesnt_match_ngram.txt"
        ANALOGIES_SECTIONS = ['name-nickname', 'total']
        DOESNT_MATCH_SECTIONS = [': seas',  ': bays', ': gods', ': Maesters', ': Houses', 'TOTAL']


    else:
        ANALOGIES_FILE = "../datasets/questions_soiaf_analogies.txt"
        DOESNT_MATCH_FILE = "../datasets/questions_soiaf_doesnt_match.txt"
        ANALOGIES_SECTIONS = ['firstname-lastname', 'child-father', 'husband-wife', 'geo-name-location', 'houses-seats', 'total']
        DOESNT_MATCH_SECTIONS = [': family-siblings',  ': names-of-houses', ': archmaesters', ': rivers', ': free cities', 'TOTAL']



    ### which sections to show in the paper..

if BOOK_SERIES == "HP":
    PRINT_DETAILS = False ## verbose debugging of eval results

    
    if NGRAMS: 
            ANALOGIES_FILE = "../datasets/questions_hp_analogies_ngram.txt"
            DOESNT_MATCH_FILE = "../datasets/questions_hp_doesnt_match_ngram.txt"
            ANALOGIES_SECTIONS = ['Gryffindor-Quidditch-team', 'Yule_ball-gentleman-lady', 'character-where_they_work', 'character-creature', 'total']
            DOESNT_MATCH_SECTIONS = [': geographical-objects', ': closest-friends', ': unforgivable-curses', ': members-of-Order_of_the_Phoenix', ': ministers-for-magic', 'TOTAL'] 
    else: 
            ANALOGIES_FILE = "../datasets/questions_hp_analogies.txt"
            DOESNT_MATCH_FILE = "../datasets/questions_hp_doesnt_match.txt"
            ANALOGIES_SECTIONS = ['firstname-lastname', 'child-father', 'husband-wife', 'pets-of-Hagrid', 'wizard-faculty', 'total']
            DOESNT_MATCH_SECTIONS = [': family-siblings', ': Hogwarts-houses', ': professors', ': wizarding-equipment', ': magic-creatures', 'TOTAL'] 


