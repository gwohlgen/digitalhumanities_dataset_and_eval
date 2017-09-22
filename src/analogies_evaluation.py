from __future__ import division
import pickle
from config import * 
import w2v_helpers

"""
    evaluation script for the analogies task 
    
    what happens: a) read evaluation data, 
                  b) for any word embedding collect the number of correct / incorrect results
                  c) print the number of correct / incorrect results 

"""

PRINT_DETAILS = False

# read the doesnt_match evaluation data from the path defined in config.py
analogies_data = open(ANALOGIES_FILE).readlines()

def print_details(task_res, msg):
    print "\n" + msg
    for res in task_res:
        print "Task: %s -- Found: %s -- Correct: %s\n" % (res[0], res[1], res[2])

# evaluate each of the embedding methods defined in config.py
for (method,emb_type) in METHODS:

    if method.startswith("coo_"): continue # script the co-occ methods

    # load model and init our data capture variables
    model, _ = w2v_helpers.load_models(method, emb_type)
    acc_res = model.accuracy(ANALOGIES_FILE)

    results, counts = [], []
    
    for res in acc_res:
        print "\n\tSection:", res['section']
        perc = len(res['correct']) / ( len(res['correct'])+len(res['incorrect']))
        print "\tNumber correct: %d \tNumber incorrect: %d \tPercentage correct %.4f" % ( 
                len(res['correct']), 
                len(res['incorrect']), perc )

        if res['section'] in ANALOGIES_SECTIONS:
            results.append( str(round(perc,3)) )
            counts.append(str( len(res['correct'])+len(res['incorrect']) ))

        print results
        print method

    print 'Number of tasks:     &', " & ".join(counts) , " \\\\ \hline \hline"
    print method, "            & ", " & ".join(results) , " \\\\ \hline"

