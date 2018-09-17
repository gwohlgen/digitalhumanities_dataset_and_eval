from numpy import array
from numpy import asarray
from numpy import zeros
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.utils import to_categorical

class KerasEval:

    def __init__(self):
        pass

    def load_model(self, path_to_model):
        """
            this loads a (txt) model from the *file system* to a *embeddings_index* (dict)
        """

        # load the whole embedding model into memory
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
        """ load training data as:
            self.docs   .. (a list of) the 4 word intrusion terms as one string ("doc")
            self.labels .. the indexes of the intruders in the "docs" 
        """

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

    def train(self):
        """
            step 1: transform the 'docs' into keras padded_docs (with int-ids instead of words, and fixed length)
            step 2: create matrix of weights of words in training docs
            step 3: create and train Keras model
        """

        # step 1:
        # prepare tokenizer
        t = Tokenizer()
        t.fit_on_texts(self.docs)
        vocab_size = len(t.word_index) + 1
        # integer encode the documents
        encoded_docs = t.texts_to_sequences(self.docs)
        print("Number of encoded_docs:", len(encoded_docs))
        # pad documents to a max length of 4 words
        # pad documents to a max length of 4 words
        max_length = 4
        padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
        print("Number of padded:", len(padded_docs))
          

        # step 2: create a weight matrix for words in training docs
        embedding_matrix = zeros((vocab_size, 300))
        for word, i in t.word_index.items():
            embedding_vector = self.embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        # step 3: create and train Keras model
        # define model
        model = Sequential()
        e = Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=4, trainable=False)
        model.add(e)
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        # compile the model
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
        #model.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])
        # summarize the model
        print(model.summary())
        # fit the model
        model.fit(padded_docs, self.labels, epochs=25, verbose=0)
        # evaluate the model
        loss, accuracy = model.evaluate(padded_docs, self.labels, verbose=0)
        print('Accuracy: %f' % (accuracy*100))
        print('Loss: %f' % (loss,))




if __name__ == "__main__":

    keras_eval = KerasEval()
    keras_eval.load_model("../../models/asoif_glove_w12-bash.model")
    keras_eval.load_training_data("keras_input.raw")
    keras_eval.train()
