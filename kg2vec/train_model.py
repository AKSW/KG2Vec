#!/usr/bin/env python
import os
import sys
import logging

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)

def learn(inp, outp, size):
    from gensim.models.word2vec import LineSentence
    import multiprocessing
    from gensim.models import Word2Vec
    logger.info("running %s" % ' '.join(sys.argv))
    model = Word2Vec(LineSentence(inp), size=int(size), window=3, sample=0, negative=5, min_count=1, workers=multiprocessing.cpu_count())
    # trim unneeded model memory = use (much) less RAM
    model.init_sims(replace=True) 
    model.wv.save_word2vec_format(outp)
    return model

learn(sys.argv[1], sys.argv[1] + '.w2v', int(sys.argv[2]))
