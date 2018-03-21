#!/usr/bin/env bash

# arguments: <dataset_id> <training_data> <dimensions> <test_data>
echo "KG2Vec: dataset_id=$1 training_data=$2 dimensions=$3 test_data=$4 verbalization_type=$5 scoring=analogy"

# learning
python make_dictionary.py $2 $1 $4
python train_model.py $1_$5.txt $3

# prediction
python analogy_predict.py $1 $5
