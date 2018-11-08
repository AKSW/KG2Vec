#!/usr/bin/env python
from gensim.models import KeyedVectors as kv
import sys

TRAINING = sys.argv[1]
TEST = TRAINING + '-test'
VERB_TYPE = sys.argv[2]

model = kv.load_word2vec_format(TRAINING + '_' + VERB_TYPE + '.txt.w2v')

# # collect properties
# props = set()
# with open(TRAINING + '_output.txt') as f:
#     for line in f:
#         triple = line[:-1].split(' ')
#         props.add(triple[1])

uri2id = {'&': '-2', '^': '-1'}
id2uri = {'-2': '&', '-1': '^'}
with open(TRAINING + '_dictionary.txt') as f:
    for line in f:
        sp = line.find(' ')
        line = [line[:sp], line[sp + 1:-1]]
        id2uri[line[0]] = line[1]
        uri2id[line[1]] = line[0]

training = set()
with open(TRAINING + '_output.txt') as data:
    for dline in data:
        training.add(dline)


def is_in_training(s, p, o):
    string = "{} {} {}\n".format(s, p, o)
    if string in training:
        return True
    return False


# c = 0
with open(TEST + '_output.txt') as test:
    for tline in test:
        ttriple = tline[:-1].split(' ')
        s_uri = id2uri[ttriple[0]]
        p_uri = id2uri[ttriple[1]]
        # print [id2uri[x] for x in ttriple]

        # dict() object -> occurrences
        occur = dict()
        with open(TRAINING + '_output.txt') as data:
            for dline in data:
                dtriple = dline[:-1].split(' ')
                if dtriple[1] == uri2id[p_uri]:
                    msim = model.most_similar(positive=[uri2id[s_uri], dtriple[2]], negative=[dtriple[0]], topn=1)
                    # print ":", [train_id2uri[x] for x in dtriple]
                    # print "  {} : {} = {} : {}".format(s_uri, train_id2uri[dtriple[0]], "x", train_id2uri[dtriple[2]])
                    for asim in msim:
                        obj, sim = asim[0], asim[1]
                        if is_in_training(uri2id[s_uri], dtriple[1], obj):
                            continue
                        # print "  x =", train_id2uri[obj], sim
                        if obj not in occur:
                            occur[obj] = 0
                        occur[obj] += 1

        # compute triples confidence
        maxval = None
        for key, value in sorted(occur.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[:20]:
            if maxval is None:
                maxval = value
            print("{}\t<{}> <{}> <{}>".format(float(value) / maxval, s_uri, p_uri, id2uri[key]))

        # c += 1
        # if c > 10:
        #     break
