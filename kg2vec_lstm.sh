#!/usr/bin/env bash

# arguments: <dataset_id> <training_data> <dimensions> <test_data> <verbalization_type> <neg_sampling> <training_epochs>
echo "KG2Vec: dataset_id=$1 training_data=$2 dimensions=$3 test_data=$4 verbalization_type=$5 neg_sampling=$6 epochs=$7 scoring=lstm"

# learning
python make_dictionary.py $2 $1 $4
python train_model.py $1_$5.txt $3

# prediction
python lstm_neural_net.py $1 $5 $6 $7
