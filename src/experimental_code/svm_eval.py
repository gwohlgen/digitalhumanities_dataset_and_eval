import numpy as np
from numpy import array
from numpy import asarray
from numpy import zeros
from sklearn import svm

NUM_TRAIN=9000

class SVMEval:

    def __init__(self):
        pass

    def load_model(self, path_to_model):

        # load the whole embedding into memory
        embeddings_index = dict()
        print("Path to model:", path_to_model)

        f = open(path_to_model)
        for line in f:
            values = line.split()
            word = values[0]
            coefs = asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()

        print("Model loaded: Number of words", len(embeddings_index), '\n\n')
        self.embeddings_index = embeddings_index

    def load_training_data(self, path_to_data):
        # get training docs and labels
        raw_data = open(path_to_data).readlines() 
        
        ### find labels
        docs, labels = [], []


        for line in raw_data:
            elements = line.strip().split(" ")
            terms, correct = elements[0:4], elements[5]
            labels.append( terms.index(correct) )
            docs.append(" ".join(terms))



        self.docs = docs
        self.labels = labels
    
        print("Number of docs:", len(docs), "Number of labels", len(labels))

    def prepare(self):

        print(self.docs[0:10])
        print(self.labels[0:10])
        not_found_indices = []

        X = [] 
       
        all_docs = [] 
        for (i, doc) in enumerate(self.docs):

            concat = np.array
            try:
                words= [w for w in doc.split(' ')]  
                concat = np.append( self.embeddings_index[words[0]],  self.embeddings_index[words[1]])
                concat = np.append(concat, self.embeddings_index[words[2]])
                concat = np.append(concat, self.embeddings_index[words[3]])
                all_docs.append(concat)
            except:
                #print("Error, index:", i)
                not_found_indices.append(i)

        print("Number of KeyErrors", len(not_found_indices))
        sane_labels = [i for j, i in enumerate(self.labels) if j not in not_found_indices]


        ## split train/test
        train_docs,   test_docs = all_docs[:NUM_TRAIN], all_docs[NUM_TRAIN:]  
        self.train_labels, self.test_labels = sane_labels[:NUM_TRAIN], sane_labels[NUM_TRAIN:]  

        self.train_docs = np.array(train_docs)
        self.test_docs = np.array(test_docs)



    def train(self):
        print(self.train_docs.shape, self.test_docs.shape)
        print(len(self.train_labels), len(self.test_docs))


        cl = svm.SVC()

        cl.fit(self.train_docs, self.train_labels)

        s = cl.score(self.test_docs, self.test_labels)
        print("accuracy", s)

    # Train Shape (5000, 784): accuracy with Logistic Regression 0.8571

#    test_pred = cl.predict(d2_test_dataset)
    #confusion_matrix = confusion_matrix(test_labels, test_pred)
    #print(confusion_matrix)


    

if __name__ == "__main__":

    svm_eval = SVMEval()
    svm_eval.load_model("../../models/asoif_glove_w12-bash.model")
    svm_eval.load_training_data("keras_input.raw")
    svm_eval.prepare()
    svm_eval.train()
