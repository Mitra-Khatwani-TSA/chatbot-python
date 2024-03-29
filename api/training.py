import random
import json
import pickle 
import numpy as np
import nltk

from keras.models import Sequential
from nltk.stem import WordNetLemmatizer
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer() # This instantiates object that will convert words to root form

intents = json.loads(open("intents.json").read())

#lists
words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]

for intent in intents["intents"]:
    for pattern in intent["patterns"]:

        #seperates words in the patterns into tokens
        word_list = nltk.word_tokenize(pattern)

        #appends to word list
        words.extend(word_list)

        #associate the pattern list with its tag and append it as a tuple to document list
        documents.append(((word_list), intent['tag']))

        #append the tags to the list of classifications
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

new_words = []
for w in words:
    if w in ignore_letters:
        continue
    else:
        new_words.append(lemmatizer.lemmatize(w))
        
words = new_words
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))



#classification
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(
        word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])



#model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ),
                activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), 
                activation='softmax'))

#compile
sgd = SGD(lr = 0.01, decay=1e-6, momentum = 0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
    optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y),
    epochs=1000, batch_size=5, verbose=1)

model.save('chatbotmodel.h5', hist)

