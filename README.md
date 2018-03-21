# KG2Vec
KG2Vec: Expeditious Generation of Knowledge Graph Embeddings

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
sh kg2vec_analogy.sh aksw-bib aksw-bib-train+valid.nt 10 aksw-bib-test.nt
```

## Citing

* arXiv: TBA

```bib
@proceedings{soru-kg2vec-2018,
    author = "Tommaso Soru, Stefano Ruberto, Diego Moussallem, Edgard Marx, Diego Esteves, Axel-Cyrille Ngonga Ngomo",
    title = "Expeditious Generation of Knowledge Graph Embeddings",
    year = "2018",
}
```
