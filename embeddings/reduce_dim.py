from gensim.models import KeyedVectors
from sklearn.decomposition import PCA

# load vectors
sl = KeyedVectors.load_word2vec_format('wiki.sl.vec')
vec = sl[sl.index2entity]

pca = PCA(n_components=128)
result = pca.fit_transform(vec)
sl.vectors = result

sl.save_word2vec_format('wiki-sl.128d.300k.vec')
