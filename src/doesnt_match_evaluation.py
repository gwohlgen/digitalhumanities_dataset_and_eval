from __future__ import division, print_function
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from collections import OrderedDict
from pprint import pprint
from config import * 
from w2v_dataset_helpers import load_models, print_details, print_latex_version

SEP_I = 4 ## position of the seperator symbol in the input data

"""
    evaluation script for the doesnt_match() task 
    @author: Gerhard Wohlgenannt (2017), ITMO University, St.Petersburg, Russia   

    what happens: a) read evaluation data, 
                  b) for any word embedding collect the number of correct / incorrect results
                  c) Collect and analyse results with pandas dataframes
"""

# read the doesnt_match evaluation data from the path defined in config.py

doesnt_match_data = open(DOESNT_MATCH_FILE).readlines()

def evaluate_doesnt_match(method, emb_type):
    """ create task_results which contains the judgements of all input questions (task units) """

    # load model and init our data capture variables
    model, _ = load_models(method, emb_type)
    task_results = []

    for line in doesnt_match_data:

        # those are the section (or :end) markers
        if line.startswith(":"): 
            task_type = line.strip()  
            continue
        
        ### get information from the input line
        ### input line format is: task-terms :: outlier
        line_list = line.strip().split()
        assert(len(line_list)) == 6

        ## just split up and a assign the input data
        task_terms, difficulty, correct_outlier = line_list[:SEP_I], line_list[SEP_I][2], line_list[SEP_I+1:][0]

        ## call gensim model to find the outlier candidate
        found_outlier = model.doesnt_match( task_terms ) 

        ## judge correctness of candidate 
        correct=0.0 # False
        if found_outlier == correct_outlier:
            correct=1.0 # True

        task_results.append( (task_type, task_terms, found_outlier, correct_outlier, difficulty, correct) )

    return task_results


def analyze_with_pandas(method, task_results):

        df = pd.DataFrame(task_results)
        df.columns = ['task_type', 'task_terms', 'found_outlier', 'correct_outlier', 'difficulty', 'correct']

        ### 1.) collect the generate percentage of correct answers per section and in total
        results = OrderedDict()
        gb_tt = df.groupby('task_type')
        #print (gb2.mean(), gb_tt.count())
        for name, group in gb_tt:
            results[name] = {'counts': group['task_terms'].count(), 'perc': group.mean()[0]}

        results['TOTAL'] = {'counts': df['correct'].count(), 'perc': df['correct'].mean() }

 
        #for section in set(df['task_type'].tolist()):
        #     print(section)
        #     a = df[df.task_type == section]
        #     print  a[a.correct == True].shape[0]
        #     print  a[a.correct == False].shape[0]


        print("\nTotal values of accuracy per **difficulty** category for: " + method)        
        gb_diff = df.groupby('difficulty')
        print (gb_diff.mean())

        ## analyze data from the most difficult class // per section
        print("\nDeeper look into difficulty data, here only check out data for difficulty level: 1")
        tt = gb_diff.get_group('1').groupby('task_type')
        print (tt['correct'].count())
        print (tt.mean())
        tt.mean()

        ##### deeper overview
        print("\nDeeper look into difficulty data, here check out data for all difficulty levels")
        deep = df.groupby( ['task_type', 'difficulty'] )
        print(deep.mean())
   
        print("\ndf.describe -- closer statistical look at global data")
        print(df.describe())

        #sys.exit()
        return results

    

if __name__ == "__main__":

    # evaluate each of the embedding methods defined in config.py
    for (method,emb_type) in METHODS:
        task_results = evaluate_doesnt_match(method, emb_type)
        results = analyze_with_pandas(method, task_results)

        pprint(dict(results))
        print_latex_version(results, method, DOESNT_MATCH_SECTIONS)

        df =  pd.DataFrame(task_results)

