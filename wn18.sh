#!/usr/bin/env bash

# -- build vectors for WN18
python train_model.py wordnet-mlj12/kg2vec_wordnet-mlj12-train.txt 10

# -- run WN18 eval model
python lstm_neural_net.py \
    wordnet-mlj12/kg2vec_wordnet-mlj12-train.txt.w2v \
    wordnet-mlj12/kg2vec_wordnet-mlj12-train.txt \
    wordnet-mlj12/kg2vec_wordnet-mlj12-test.txt \
    wordnet-mlj12/kg2vec_wordnet-mlj12-dictionary.txt \
    random \
    100