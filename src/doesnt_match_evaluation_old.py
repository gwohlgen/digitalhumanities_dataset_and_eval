from __future__ import division
import pickle
import pandas as pd
from collections import OrderedDict
from pprint import pprint
from config import * 
from w2v_dataset_helpers import load_models, print_details, print_latex_version



"""
    evaluation script for the doesnt_match() task 
    @author: Gerhard Wohlgenannt (2017), ITMO University, St.Petersburg, Russia   

    what happens: a) read evaluation data, 
                  b) for any word embedding collect the number of correct / incorrect results
                  c) print the number of correct / incorrect results 
"""

ANALYZE_PER_DIFFICULTY = True

# read the doesnt_match evaluation data from the path defined in config.py
doesnt_match_data = open(DOESNT_MATCH_FILE).readlines()

def evaluate_doesnt_match(method, emb_type):

    # load model and init our data capture variables
    model, _ = load_models(method, emb_type)
    tot_correct, tot_incorrect = 0, 0
    correct_tasks, incorrect_tasks = [], []
    results = OrderedDict() 

    for line in doesnt_match_data:

        # those are the section (or :end) markers
        if line.startswith(":"): 

            # print the results for the last section, and reset variables
            if len(correct_tasks) + len(incorrect_tasks) > 0:
                counts = len(correct_tasks) + len(incorrect_tasks)
                perc = len(correct_tasks) /counts

                ## collect data about this task
                results[last_task_type]={}
                results[last_task_type]['perc'] = perc
                results[last_task_type]['correct']  = len(correct_tasks) 
                results[last_task_type]['correct']  = len(incorrect_tasks) 
                results[last_task_type]['counts'] = counts 
            
                tot_correct += len(correct_tasks) 
                tot_incorrect += len(incorrect_tasks)
    
                if PRINT_DETAILS:
                    print_details(correct_tasks,   "CORRECT RESULTS")
                    print_details(incorrect_tasks, "WRONG_RESULTS")

                if ANALYZE_PER_DIFFICULTY:
                    analyze_difficulty(correct_tasks, incorrect_tasks)

                correct_tasks, incorrect_tasks = [], []

            last_task_type = line.strip() # remember the new section header
            continue 
            
        
        ### get information from the input line
        ### input line format is: task-terms :: outlier
        line_list = line.strip().split()
        assert(len(line_list)) == 6
        #sep_i = line_list.index('::') 
        sep_i = 4
        task_terms = line_list[:sep_i]
        difficulty = line_list[sep_i][2]
        correct_outlier = line_list[sep_i+1:][0]

        found_outlier = model.doesnt_match( task_terms ) 

        if found_outlier == correct_outlier:
            correct_tasks.append( (task_terms, found_outlier, correct_outlier, difficulty) )
            
        else:
            incorrect_tasks.append( (task_terms, found_outlier, correct_outlier, difficulty) )

    # tex style output
    results['TOTAL'] = {}
    results['TOTAL']['perc'] =  tot_correct/(tot_correct+tot_incorrect)
    results['TOTAL']['correct']  = tot_correct
    results['TOTAL']['incorrect'] = tot_incorrect 
    results['TOTAL']['counts'] = tot_correct + tot_incorrect

    return results

def analyze_difficulty(correct_tasks, incorrect_tasks):
    res={} 

    for task in correct_tasks:
        difficulty  = task[3]
        if difficulty in res:
           TODO .. use pandas dataframe or internal SQL table for data analysis


if __name__ == "__main__":

    # evaluate each of the embedding methods defined in config.py
    for (method,emb_type) in METHODS:
        results = evaluate_doesnt_match(method, emb_type)

        pprint(dict(results))
        print_latex_version(results, method, DOESNT_MATCH_SECTIONS)
