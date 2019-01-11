from gensim.models import KeyedVectors

aksw_e = KeyedVectors.load_word2vec_format('aksw-bib_output.txt.w2v')

# -- Check results, e.g. first 4 keys in the dictionary
list(aksw_e.vocab.keys())[:4]
# ['pr_1', 'pr_10', 'pr_14', 'pr_4']


