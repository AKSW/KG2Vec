#!/usr/bin/env bash

# Adapted from: https://github.com/facebookresearch/fastText/blob/master/scripts/kbcompletion/data.sh

echo "preparing WN18"
wget -P . https://github.com/mana-ysh/knowledge-graph-embeddings/raw/master/dat/wordnet-mlj12.tar.gz
tar -xzvf wordnet-mlj12.tar.gz
DIR=wordnet-mlj12
for f in ${DIR}/wordnet-ml*.txt;
do
  fn=${DIR}/kg2vec_$(basename $f)
  awk '{print "id_"$1,"pr_"$2, "id_"$3}' < ${f} > ${fn};
done
cat ${DIR}/kg2vec_* > ${DIR}/kg2vec_wordnet-mlj12-full.txt
cat ${DIR}/kg2vec_*train.txt ${DIR}/kg2vec_*valid.txt > ${DIR}/kg2vec_wordnet-mlj12-valid+train.txt

# -- create WN18 dictionary: ENTITIES then (dummy) RELATIONS
awk '{print "id_"$1" "$2}' < wordnet-mlj12/wordnet-mlj12-definitions.txt > wordnet-mlj12/kg2vec_wordnet-mlj12-dictionary.txt
awk '{print $2" "$2}' < wordnet-mlj12/kg2vec_wordnet-mlj12-valid+train.txt >> wordnet-mlj12/kg2vec_wordnet-mlj12-dictionary.txt