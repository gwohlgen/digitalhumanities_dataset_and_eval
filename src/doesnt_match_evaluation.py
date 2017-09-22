from __future__ import division
import pickle
from config import * 
import w2v_dataset_helpers

"""
    evaluation script for the doesnt_match() task 
    
    what happens: a) read evaluation data, b) for any word embedding collect the number of correct / incorrect results
                  c) print the number of correct / incorrect results 

"""

PRINT_DETAILS = False

# read the doesnt_match evaluation data from the path defined in config.py
doesnt_match_data = open(DOESNT_MATCH_FILE).readlines()

def print_details(task_res, msg):
    print "\n" + msg
    for res in task_res:
        print "Task: %s -- Found: %s -- Correct: %s\n" % (res[0], res[1], res[2])

# evaluate each of the embedding methods defined in config.py
for (method,emb_type) in METHODS:

    if method.startswith("coo_"): continue # script the co-occ methods

    # load model and init our data capture variables
    model, _ = w2v_dataset_helpers.load_models(method, emb_type)
    tot_correct, tot_incorrect, correct, incorrect = 0, 0, 0, 0
    correct_tasks, incorrect_tasks = [], []
    results, counts = [], []

    for line in doesnt_match_data:

        # those are the section (or :end) markers
        if line.startswith(":"): 

            # print the results for the last section, and reset variables
            if correct + incorrect > 0:
                perc = correct/(correct+incorrect)
                if last_task_type in DOESNT_MATCH_SECTIONS: 
                    results.append(perc)
                    counts.append(str(correct+incorrect))

                print DOESNT_MATCH_SECTIONS
                print "\tTask type:", last_task_type
                print last_task_type in DOESNT_MATCH_SECTIONS
                print "\tNumber correct: %d, incorrect: %d, total: %d, percentage: %f\n" % (correct, incorrect, correct+incorrect, perc) 
            
                tot_correct += correct
                tot_incorrect += incorrect
    
                if PRINT_DETAILS:
                    print_details(correct_tasks, "CORRECT RESULTS")
                    print_details(incorrect_tasks, "WRONG_RESULTS")

                correct, incorrect = 0, 0
                correct_tasks, incorrect_tasks = [], []

            print '*************',line
            last_task_type = line.strip() # remember the new section header
            continue 
            
        
        ### get information from the input line
        ### input line format is: task-terms :: outlier
        line_list = line.strip().split()
        sep_i = line_list.index('::')
        task_terms = line_list[:sep_i]
        correct_outlier = line_list[sep_i+1:][0]

        found_outlier = model.doesnt_match( task_terms ) 

        if found_outlier == correct_outlier:
            #print "correct", found_outlier
            correct += 1
            correct_tasks.append( (task_terms, found_outlier, correct_outlier) )
            
        else:
            #print "incorrect", found_outlier, correct_outlier
            incorrect += 1
            incorrect_tasks.append( (task_terms, found_outlier, correct_outlier) )

    ## total stats
    tot_perc = tot_correct/(tot_correct+tot_incorrect)
    print "\nTOTAL Number correct: %d, incorrect: %d, percentage: %f\n" % (tot_correct, tot_incorrect, tot_perc) 

    # tex style output
    results.append(tot_perc)
    counts.append(str(tot_correct+tot_incorrect))
    rounded = [str( round(r,3) ) for r in results] 
    print method, "            & ", " & ".join(rounded) , " \\\\ \hline"
    print 'Number of tasks:       &', " & ".join(counts) , " \\\\ \hline \hline"
