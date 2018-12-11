import sys, glob, pickle
from operator import itemgetter

"""
With this file, you can check how often the terms from your datasets appear in the given book corpus.
All terms should appear at least 5 times (or whatever is the min_count setting which you used to train the word embedding model).

Usage:
    sys.argv[1]     the dataset file for which you want to check the frequencies
    sys.argv[2]     the book corpus to check the frequencies of terms in

Example:
    python check_frequencies.py hp_analogies.txt harry_potter_all_books.txt 

"""

INFILE = sys.argv[1]
BOOK = sys.argv[2]

MIN_NUM = 5

all_words = [] 


for name in glob.glob(INFILE+'*'):

    for line in open(name):
        if line.startswith(':') or line.startswith('"') or not line.strip():
            continue

        words = line.split(' ')
        words = [word.strip() for word in words]
        all_words.extend(words)


# get the set of all words from the dataset (for which we will check the frequencies)
all_words = list(set(all_words)) # make unique

print('All words in dataset:', all_words)

### ok, now we have the words, get the counts from the book
book_text = open(BOOK).read()

word_counts = [] 
for word in all_words:
    count = book_text.count(word)
    word_counts.append( (word, count) )


words_sorted = sorted(word_counts,key=itemgetter(1))

## print words that appear only few times
for w in words_sorted:
    if w[1] <= MIN_NUM*3:
        print(w)

dw = dict(words_sorted)

#pickle.dump(dw, open('freq_XX', 'wb'))
