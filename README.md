# KG2Vec
🏎 KG2Vec: Expeditious Generation of Knowledge Graph Embeddings

## Usage

* Download data from http://tsoru.aksw.org/kg2vec/

```bash
sh kg2vec_<scoring>.sh <dataset_id> <training_data> <dimensions> <test_data> <verbalization_type> <neg_sampling> <training_epochs>
```

### LSTM-based scoring function
```bash
sh kg2vec_lstm.sh aksw-bib aksw-bib-train+valid.nt 10 aksw-bib-test.nt output random 100
```

### Analogy-based scoring function
```bash
sh kg2vec_analogy.sh aksw-bib aksw-bib-train+valid.nt 10 aksw-bib-test.nt output
```

## Cite

* Presented at the 5th European Conference on Data Analysis (ECDA 2018) as _"A Fast and Simple Approach to Knowledge Graph Embedding"_.
* Working paper: https://arxiv.org/abs/1803.07828

```bib
@proceedings{soru-kg2vec-2018,
    author = "Tommaso Soru and Stefano Ruberto and Diego Moussallem and Edgard Marx and Diego Esteves and Axel-Cyrille {Ngonga Ngomo}",
    title = "Expeditious Generation of Knowledge Graph Embeddings",
    year = "2018",
}
```
