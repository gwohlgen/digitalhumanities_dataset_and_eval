import sys, glob, pickle
from operator import itemgetter

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


all_words = list(set(all_words)) # make unique

print(all_words)

### ok, now we have the words, get the counts from the book
book_text = open(BOOK).read()

word_counts = [] 
for word in all_words:
    count = book_text.count(word)
    word_counts.append( (word, count) )


words_sorted = sorted(word_counts,key=itemgetter(1))

for w in words_sorted:
    if w[1] <= MIN_NUM*3:
        print(w)

dw = dict(words_sorted)

pickle.dump(dw, open('freq_XX', 'wb'))
