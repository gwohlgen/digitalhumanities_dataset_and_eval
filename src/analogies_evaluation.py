from __future__ import division
import pickle
from pprint import pprint
from config import * 
from w2v_dataset_helpers import load_models, print_details, print_latex_version
from collections import OrderedDict

"""
    evaluation script for the analogies task 
    @author: Gerhard Wohlgenannt (2017), ITMO University, St.Petersburg, Russia   

    what happens: a) read evaluation data, 
                  b) for any word embedding collect the number of correct / incorrect results
                  c) print the number of correct / incorrect results 
"""

# read the analogies evaluation data from the path defined in config.py
analogies_data = open(ANALOGIES_FILE).readlines()

# evaluate each of the embedding methods defined in config.py
def evaluate_analogies(method, emb_type):

    # load model and init our data capture variables
    model, _ = load_models(method, emb_type)
    acc_res = model.accuracy(ANALOGIES_FILE)
    results = OrderedDict()

    for res in acc_res:

        ## collect data about this task
        sec = res['section']
        print("\n\tSection:", sec)
        results[sec]={}
        results[sec]['perc'] = len(res['correct']) / ( len(res['correct'])+len(res['incorrect']))
        results[sec]['correct']  = len(res['correct'])
        results[sec]['incorrect'] = len(res['incorrect'])
        results[sec]['counts'] = str( len(res['correct'])+len(res['incorrect']) )

    return results


if __name__ == "__main__":

    # evaluate each of the embedding methods defined in config.py
    for (method,emb_type) in METHODS:
        results = evaluate_analogies(method, emb_type)
        pprint(dict(results))
        print ("Number of sections:", len(results)-1)
        print_latex_version(results, method, ANALOGIES_SECTIONS)
