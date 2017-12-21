""" 
    This file creates the datasets to be used with word2vec or Gensim 
    analogy task evaluation scripts.

    The domain of the data is the "A song of ice and fire" book series by GRR Martin.

    This script creates the various permutations (per relation type)
    for the input SOURCEFILE and writes them into OUTFILE

    You can then directly use the OUTFILE with word2vec or Gensim to evaluate the quality
    of your model on these specific analogy tasks.

    In the SOURCEFILE we use the convention to group relation types into blocks
    with starting a block with the string ": "

    @author Gerhard Wohlgenannt, ITMO University, St. Petersburg, Russia
"""

import random, math, itertools


def create_and_write_last_block(blockentries, ofh, mode, filter_same_target=True):
    """
        write the individual block to the output file
        combine (permuation) each entry with each other
    """
    if len(blockentries) == 0: return

    if mode == "analogies":

        # ok, so we combine every entry with every other entry
        for entry1 in blockentries:
            assert(len(entry1) == 2)

            for entry2 in blockentries:
                if entry1 == entry2: 
                    continue 

                if filter_same_target and (entry1[1] == entry2[1]):
                    continue 
        
                outline = " ".join(entry1) + " " +" ".join(entry2) + "\n"
                ofh.write(outline)

    elif mode == "doesnt_match":

        # index of seperator
        for entry in blockentries:
            sep_i = entry.index("::")  # where is the seperator element?
            matches   = entry[:sep_i]
            outsiders = entry[sep_i+1:]

            print(matches, '::::', outsiders)
            assert len(matches) >= 3
            assert len(outsiders) == 20

            for combination in list( itertools.combinations(matches, 3) ):
                create_doesnt_match_line(list(combination), outsiders, ofh)

                    

def create_doesnt_match_line(matches3, outsiders, ofh):
    """
        for a item of 3 related terms and a list of outsiders:
            write the combinations of terms and outsiders to the file
    """

    for position, outsider in enumerate(outsiders):
        print position
        tmp = matches3[:] # slicing gives out a copy (!) of the list
        tmp.append(outsider)

        ### new: categorize tasks from 1-4 according to difficulty (position in the list)
        difficulty = int( math.floor(position/5.0)+1 )

        random.shuffle(tmp) # random order of items per line
        ofh.write( " ".join(tmp) + " ::"+str(difficulty)+": " + outsider + "\n")



def create_dataset(sourcefile=None, outfile=None, mode=None):
    """ 
        steps here:
            a) INIT: read sourcefile, open outfile, init blockentries
            b) iterator over the file, collect data, and when a new section starts:
               create and write the last one 
    """

    blockentries = [] 

    with open(sourcefile) as f:
        source_lines = f.readlines()
 
    ofh = open(outfile, 'w')
    if mode == "doesnt_match":
        ofh.write("::: Format of this file: terms-of-the-task :: the outlier-to-find\n")

    # iterate over source file
    for line in source_lines:
        if line.startswith('"') or not line.strip():
            continue # these are comments or empty lines

        # read the file block by block
        if line.startswith(':'):
            # new block detected
            create_and_write_last_block(blockentries, ofh, mode)

            blockheader=line
            if line.strip() != ":end":
                ofh.write(line)

            blockentries = [] # reset

        else:
            # fill blocks
            blockentries.append( line.strip().split(" ") )

    print("** Writing output (all permutations) file: %s\nDone\n\n" % (outfile,))





if __name__ == "__main__":

    create_dataset(sourcefile="soiaf_analogies.txt",          outfile="questions_soiaf_analogies.txt",   mode="analogies")
    create_dataset(sourcefile="soiaf_doesnt_match.txt",       outfile="questions_soiaf_doesnt_match.txt", mode="doesnt_match")
    create_dataset(sourcefile="soiaf_analogies_ngram.txt",    outfile="questions_soiaf_analogies_ngram.txt",   mode="analogies")
    create_dataset(sourcefile="soiaf_doesnt_match_ngram.txt", outfile="questions_soiaf_doesnt_match_ngram.txt", mode="doesnt_match")

    create_dataset(sourcefile="hp_analogies.txt",          outfile="questions_hp_analogies.txt",   mode="analogies")
    create_dataset(sourcefile="hp_doesnt_match.txt",       outfile="questions_hp_doesnt_match.txt", mode="doesnt_match")
    create_dataset(sourcefile="hp_analogies_ngram.txt",    outfile="questions_hp_analogies_ngram.txt",   mode="analogies")
    create_dataset(sourcefile="hp_doesnt_match_ngram.txt", outfile="questions_hp_doesnt_match_ngram.txt", mode="doesnt_match")

    ## student datasets
    #create_dataset(sourcefile="hp_analogies_topalov.txt",       outfile="questions_hp_analogies_topalov.txt", mode="analogies")
    #create_dataset(sourcefile="hp_doesnt_match_topalov.txt",       outfile="questions_doesnt_match_topalov.txt", mode="doesnt_match")
