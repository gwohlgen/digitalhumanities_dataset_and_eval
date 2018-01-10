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
#from SVD_doesntmatch import *
#from ppmi_doesnt_match import *

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

def evaluate_doesnt_match(method, emb_type, term_freq=None):
    """ create task_results which contains the judgements of all input questions (task units) """

    task_results = []
   
    if method == 'ppmi':

        ## currently not included into the public version   
        ## just use standard ppmi, or ask github owner for sending the file        
        ppmi = create_matrix()
    
    else:
        # load model and init our data capture variables
        model, _ = load_models(method, emb_type)
     
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
        if method == 'ppmi':
            found_outlier = solve_task( ppmi, task_terms) #, on_error='skip') 
            if not found_outlier: continue
            #found_outlier = solve_task_2( ppmi, task_terms) 
        else:
            found_outlier = model.doesnt_match( task_terms ) 


        ## judge correctness of candidate 
        correct=0.0 # False
        if found_outlier == correct_outlier:
            correct=1.0 # True

        if DO_FREQ_EVAL:
            ## compute avg term frequency of the task_terms
            try:
                list(term_freq[t] for t in task_terms)
            except KeyError, e:
                print("""
        Looks like you modified the evaluation questions.
        You either need to update freq_ files in datasets directory,
        or set DO_FREQ_EVAL=False.
                    """)
                sys.exit()

            avg_tf = sum(term_freq[t] for t in task_terms) / len(task_terms)
            #print(list(term_freq[t] for t in task_terms))
            #print (avg_tf)

            task_results.append( (task_type, task_terms, found_outlier, correct_outlier, term_freq[found_outlier], term_freq[correct_outlier], avg_tf, difficulty, correct) )
        else:
            task_results.append( (task_type, task_terms, found_outlier, correct_outlier, difficulty, correct) )

        # if DO_FREQ_EVAL and not correct:
        #     print('XXX: {:50} {:10} {:10} {:5} {:5} {:8} {:5} {:5}'.format(task_terms, found_outlier, correct_outlier, term_freq[found_outlier], term_freq[correct_outlier], avg_tf, difficulty, correct))


    return task_results


def analyze_with_pandas(method, task_results):

        df = pd.DataFrame(task_results)
        if DO_FREQ_EVAL:
            df.columns = ['task_type', 'task_terms', 'found_outlier', 'correct_outlier', 'found_tf', 'correct_tf', 'avg_tf', 'difficulty', 'correct']
        else:
            df.columns = ['task_type', 'task_terms', 'found_outlier', 'correct_outlier', 'difficulty', 'correct']

        ### 1.) collect the generate percentage of correct answers per section and in total
        results = OrderedDict()

        ## in the analysis of percentages we don't want the frequency information to confuse the results, so we remove frequency data :) 
        tmp_df = df[['task_type', 'task_terms', 'found_outlier', 'correct_outlier', 'difficulty', 'correct']].copy()
        gb_tt = tmp_df.groupby('task_type')
        #print (gb.mean(), gb_tt.count())
        for name, group in gb_tt:
            print ("YYYYY", group.mean())
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

        print('Number of categories',  len(gb_tt))

        if DO_FREQ_EVAL:
            # ------------------------------------------- NEW ---------------------------------------------------------------------------#
            ## bin frequency into brackets
            #bins = [0, 10, 25, 50, 100, 500, 1000, 1000000]
            bins = [0, 20, 50, 125, 500, 1000000]
            #group_names = ['1', '2', '3', '4', '5', '6', '7']
            group_names = ['1', '2', '3', '4', '5']
            df['found_tf_category'] = pd.cut(df['found_tf'], bins, labels=group_names)
            df['avg_tf_category'] = pd.cut(df['avg_tf'], bins, labels=group_names)
            #print(df.head())

            ## correlations 
            print("correlation between difficulty and correct result", df['difficulty'].astype(int).corr(df['correct']))
            print("correlation between correct-term frequency and correctness", df['correct_tf'].corr(df['correct']))
            print("correlation between   found-term frequency and correctness", df['found_tf'].corr(df['correct']))
            print("correlation between average term frequency and correctness", df['avg_tf'].corr(df['correct']))
            print("correlation between frequency bin and correctness", df['found_tf_category'].astype(int).corr(df['correct']))
            print("correlation between avg_frequency bin and correctness", df['avg_tf_category'].astype(int).corr(df['correct']))

            print("\n***************************************************Total values of accuracy per **tf_category** for: " + method)

            gb_tf_c = df.groupby('found_tf_category')
            print (gb_tf_c.mean())
            print (gb_tf_c.size())

            gb_avg_tf_c = df.groupby('avg_tf_category')
            print (gb_avg_tf_c.mean())
            print (gb_avg_tf_c.size())

        return results

    

if __name__ == "__main__":

    term_freq = pickle.load(open(FREQ_FILE))
    print(term_freq)

    # evaluate each of the embedding methods defined in config.py
    for (method,emb_type) in METHODS:
        task_results = evaluate_doesnt_match(method, emb_type, term_freq)
        results = analyze_with_pandas(method, task_results)

        pprint(dict(results))
        #sys.exit()
        #print(results)
        print_latex_version(results, method, DOESNT_MATCH_SECTIONS)

        df =  pd.DataFrame(task_results)

