#!/usr/bin/env python
from rdflib.plugins.parsers.ntriples import NTriplesParser, Sink
from rdflib.term import URIRef
import random
import math
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

N_CONTEXTS = 1
# SUBJECT_PRES = 0.2

filename = sys.argv[1]
dsid = sys.argv[2]
if len(sys.argv) > 3:
    filename2 = sys.argv[3]
else:
    filename2 = None

class MyParser(NTriplesParser):
    def parse(self, f):
        super(MyParser, self).parse(f)

class TrainingSink(Sink):
    
    def __init__(self):
        self.d = dict()
        self.f = open("{}_dictionary.txt".format(dsid), 'w')
        self.out = open("{}_output.txt".format(dsid), 'w')
        self.prox = dict()
        self.preds = dict()
    
    def finish(self):
        self.f.close()
        self.out.close()
    
    def triple(self, s, p, o):
        if not type(o) is URIRef:
            return # ignore literals
            
        # print s,p,o
        s_ = str(s)
        p_ = str(p)
        o_ = str(o)
        if s_ not in self.d:
            self.d[s_] = "id_" + str(len(self.d))
            self.f.write("{} {}\n".format(self.d[s_], s_))
        s_id = self.d[s_]

        if p_ not in self.d:
            self.d[p_] = "pr_" + str(len(self.d))
            self.f.write("{} {}\n".format(self.d[p_], p_))
        p_id = self.d[p_]

        if o_ not in self.d:
            self.d[o_] = "id_" + str(len(self.d))
            self.f.write("{} {}\n".format(self.d[o_], o_))
        o_id = self.d[o_]
        
        self.out.write("{} {} {}\n".format(s_id, p_id, o_id))
        
        # index proximities
        if s_id not in self.prox:
            self.prox[s_id] = list() # with repetition ~ weighted
        # self.prox[s_id].append(o_id)
        # self.prox[s_id].append("{} {} {}".format(s_id, p_id, o_id))
        self.prox[s_id].append("{} {} {}".format(s_id, p_id, o_id))
        if o_id not in self.prox:
            self.prox[o_id] = list()
        # self.prox[o_id].append(s_id)
        # self.prox[o_id].append("{} {} -1 {}".format(o_id, p_id, s_id))
        self.prox[o_id].append("{} {} {}".format(s_id, p_id, o_id))

        # # index predicates
        # if p_id not in self.preds:
        #     self.preds[p_id] = list()
        # self.preds[p_id].append((s_id, o_id))

class TestSink(Sink):
    
    def __init__(self, d):
        self.d = d
        self.out = open("{}-test_output.txt".format(dsid), 'w')
    
    def finish(self):
        self.out.close()
    
    def triple(self, s, p, o):
        if not type(o) is URIRef:
            return # ignore literals
            
        # print s,p,o
        s_ = str(s)
        p_ = str(p)
        o_ = str(o)
        try:
            s_id = self.d[s_]
            p_id = self.d[p_]
            o_id = self.d[o_]
        except KeyError:
            return # ignore resources not in training data
        
        self.out.write("{} {} {}\n".format(s_id, p_id, o_id))

src = TrainingSink()
src_n = MyParser(src)
with open(filename, "r") as anons:
    src_n.parse(anons)

if filename2 is not None:
    src2 = TestSink(src.d)
    src2_n = MyParser(src2)
    with open(filename2, "r") as anons:
        src2_n.parse(anons)

with open("{}_sentences.txt".format(dsid), 'w') as f:
    for subject in src.prox.keys():
        # print subject, src.prox[subject]
        sentences = set()
        for c in range(N_CONTEXTS):
            pool = list(src.prox[subject])
            sentence = ""
            # for j in range(int(math.ceil(SUBJECT_PRES * len(pool)))):
            #     pool.append(subject)
            for i in range(len(pool)):
                # extract a random object from pool
                extr = pool[int(len(pool) * random.random())]
                sentence += " " + str(extr)
                # sentence += " " + str(extr) + " -2"
                # sentences.add(extr)
                pool.remove(extr)
            sentences.add(sentence.strip())
        
        for s in sentences:
            f.write("{}\n".format(s))

