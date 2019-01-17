#!/usr/bin/env python
# LSTM for sequence classification
import numpy
# from keras.callbacks import Callback
from keras.models import Sequential
from keras.layers import Dense, LSTM
# from keras.preprocessing import sequence
import sys

# dsid = sys.argv[1]
# verb_type = sys.argv[2]
# neg_sampling = sys.argv[3]
# epochs = sys.argv[4]

# embeddings = "{}_{}.txt.w2v".format(dsid, verb_type)
# train_triples = "{}_output.txt".format(dsid)
# test_triples = "{}-test_output.txt".format(dsid)
# dictionary = "{}_dictionary.txt".format(dsid)

embeddings = sys.argv[1]
train_triples = sys.argv[2]
test_triples = sys.argv[3]
dictionary = sys.argv[4]
neg_sampling = sys.argv[5]
epochs = sys.argv[6]

# fix random seed for reproducibility
numpy.random.seed(7)
NEG_RATE = 1
N_EPOCHS = int(epochs)


# X_train = list()
# y_train = list()
# vectors = dict()
# training = dict()
# size = None

# -- Load KG Embeddings
def load_embeddings(embedding_file):
    _vectors = dict()
    _size = None
    with open(embedding_file) as f:
        for line in f:
            line = line[:-1].split(' ')
            if len(line) == 2:
                continue
            _vectors[line[0]] = line[1:]
            _size = len(line[1:])
    print("Embeddings loaded.")
    sys.stdout.flush()
    return _vectors, _size


# -- Read training triplets
def read_training_data(train_file):
    _training = dict()
    _X_train = list()
    _y_train = list()
    with open(train_file) as f:
        for line in f:
            try:
                line = line[:-1].split(' ')
                seq = [vectors[x] for x in line]
                key = (line[0], line[1])
            except KeyError:
                print(f'WARNING SAMPLE SKIPPED: {line}')

            if key not in _training:
                _training[key] = list()
            _training[key].append(line[2])
            _X_train.append(seq)
            _y_train.append(1.0)
    print("Training triples loaded and indexed.")
    sys.stdout.flush()
    return _training, _X_train, _y_train


# -- Read test triplets
def read_test_data(test_file):
    _X_test = list()
    _y_test = list()
    _idx_test = list()
    with open(test_file) as f:
        for line in f:
            line = line[:-1].split(' ')
            seq = [vectors[x] for x in line]
            _idx_test.append(line)
            _X_test.append(seq)
            _y_test.append(1.0)
    print("Test triples loaded and indexed.")
    sys.stdout.flush()
    return _X_test, _y_test, _idx_test


# -- Load Dictionary: Entities/Relations <--> URI
def load_dictionary(dict_file):
    _id2uri = dict()
    with open(dict_file) as f:
        for line in f:
            sp = line.find(' ')
            line = [line[:sp], line[sp + 1:-1]]
            _id2uri[line[0]] = line[1]
    print("Dictionary loaded.")
    return _id2uri


vectors, size = load_embeddings(embedding_file=embeddings)
training, X_train, y_train = read_training_data(train_file=train_triples)
X_test, y_test, idx_test = read_test_data(test_file=test_triples)
vkeys = list(vectors.keys())
id2uri = load_dictionary(dict_file=dictionary)


# -- CONSTRUCT NEGATIVE EXAMPLES
def negative_sampling():
    print("Negative sampling:", neg_sampling)
    sys.stdout.flush()
    if neg_sampling == "random":

        tr_size = len(y_train)
        lenv = len(vectors)
        for i in range(NEG_RATE * tr_size):
            idx0 = None
            idx1 = None
            idx2 = None
            while True:
                idx0 = vkeys[int(numpy.random.random() * lenv)]
                if idx0.startswith("id_"):
                    break
            while True:
                idx1 = vkeys[int(numpy.random.random() * lenv)]
                if idx1.startswith("pr_"):
                    break
            if (idx0, idx1) not in training:
                while True:
                    idx2 = vkeys[int(numpy.random.random() * lenv)]
                    if idx2.startswith("id_"):
                        break
            else:
                while True:
                    idx2 = vkeys[int(numpy.random.random() * lenv)]
                    if idx2.startswith("id_") and idx2 not in training[(idx0, idx1)]:
                        break
            idx = [idx0, idx1, idx2]
            # print [id2uri[x] for x in idx]
            sys.stdout.flush()

            seq = [vectors[idx[x]] for x in range(3)]
            X_train.append(seq)
            y_train.append(0.0)
            if i % 1000 == 0:
                print("{} negative triples sampled.".format(i + 1))
                sys.stdout.flush()

    elif neg_sampling == "corrupt":

        for key in training:
            idx_orig = key
            for j in range(len(training[key])):
                added = set()
                while len(added) < NEG_RATE:
                    random_obj = vkeys[int(numpy.random.random() * len(vectors))]
                    if random_obj not in training[key]:
                        added.add(random_obj)
                for random_obj in added:
                    idx = list(idx_orig)
                    idx.append(random_obj)
                    print([id2uri[x] for x in idx])
                    sys.stdout.flush()

                    seq = [vectors[idx[x]] for x in range(3)]
                    X_train.append(seq)
                    y_train.append(0.0)

    else:
        # will probably fail for having no negatives
        print("+++ WARNING: no negatives generated! +++")
        sys.stdout.flush()


negative_sampling()
# -- END OF NEGATIVE SAMPLES

print("dimensions:", size)
print("train size:", len(X_train))
# print "train y:", y_train
print("test size:", len(X_test))
# print "test y:", y_test
sys.stdout.flush()

# X_train = sequence.pad_sequences(X_train)
# X_test = sequence.pad_sequences(X_test)
X_train = numpy.asarray(X_train)
y_train = numpy.asarray(y_train)
X_test = numpy.asarray(X_test)
y_test = numpy.asarray(y_test)


# class TestCallback(Callback):
#     def __init__(self, test_data):
#         self.test_data = test_data
#
#     def on_epoch_end(self, epoch, logs={}):
#         x, y = self.test_data
#         loss, acc = self.model.evaluate(x, y, verbose=0)
#         print('\nTesting loss: {}, acc: {:.2f}\n'.format(loss, acc*100))

# -- Create Keras model
def lstm_model():
    model = Sequential()
    model.add(LSTM(size, input_shape=(3, size)))  # , return_sequences=True))
    # model.add(LSTM(size))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mean_squared_error', optimizer='adam')  # , metrics=['accuracy'])
    print(model.summary())
    sys.stdout.flush()
    return model


model = lstm_model()
model.fit(X_train, y_train, epochs=N_EPOCHS, batch_size=16)  # , callbacks=[TestCallback((X_test, y_test))])

hits1 = 0
hits3 = 0
hits10 = 0
for ttriple in idx_test:
    x = list()
    tpl = list()
    s_uri = id2uri[ttriple[0]]
    p_uri = id2uri[ttriple[1]]
    o_uri = id2uri[ttriple[2]]
    # target link
    x0 = [[vectors[ttriple[0]], vectors[ttriple[1]], vectors[ttriple[2]]]]
    confid_x0 = model.predict(numpy.asarray(x0), verbose=0)[0][0]
    # print "{}\t<{}> <{}> <{}>".format(confid_x0, s_uri, p_uri, o_uri)

    for key in vkeys:
        if key.startswith("pr_") or ttriple[2] == key:
            continue
        if (ttriple[0], ttriple[1]) in training:
            if key in training[(ttriple[0], ttriple[1])]:
                continue  # filtered hits@N
        x.append([vectors[ttriple[0]], vectors[ttriple[1]], vectors[key]])
        tpl.append("<{}> <{}> <{}>".format(s_uri, p_uri, id2uri[key]))
    confidence = model.predict(numpy.asarray(x), verbose=0)
    score = 1
    for c, t in zip(confidence, tpl):
        # print "{}\t{}".format(c[0], t)
        if c > confid_x0:
            score += 1
    if score <= 10:
        hits10 += 1
        if score <= 3:
            hits3 += 1
            if score <= 1:
                hits1 += 1

print("hits@1:", float(hits1) / len(idx_test))
print("hits@3:", float(hits3) / len(idx_test))
print("hits@10:", float(hits10) / len(idx_test))
