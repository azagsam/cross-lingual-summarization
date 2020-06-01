"""
Prepare embeddings and dictionaries

export ABS_EMB=~/myfiles/vecmap/data/vecmap_output/30k.wiki.abs.src.sup.vec
export EXT_EMB=~/myfiles/vecmap/data/vecmap_output/30k.wiki.ext.src.sup.vec
export MODEL=fast_text
"""

import pickle as pkl
import torch
import os

# Insert paths
MODEL = os.environ['MODEL']
ABS_EMB_PATH = os.environ['ABS_EMB']
EXT_EMB_PATH = os.environ['EXT_EMB']

# create abstractor DICTIONARY and and save it on disk
vocab = {}
for ind, line in enumerate(open(ABS_EMB_PATH, 'r').readlines()):
    word, vec = line.split(" ", 1)
    vocab[word] = ind
with open('{}/pretrained/acl/abstractor/vocab.pkl'.format(MODEL), 'wb') as fp:
    pkl.dump(vocab, fp)

# save abstractor EMBEDDINGS
weights = []
for line in open(ABS_EMB_PATH).readlines():
    word, vec = line.split(' ', 1)
    weights.append([float(num) for num in vec.split()])
weights = torch.tensor(weights)
torch.save(weights, '{}/embeddings/abs-weights.pt'.format(MODEL))

# create extractor DICTIONARY and save it on disk
vocab = {}
for ind, line in enumerate(open(EXT_EMB_PATH, 'r').readlines()):
    word, vec = line.split(" ", 1)
    vocab[word] = ind
with open('{}/pretrained/acl/agent_vocab.pkl'.format(MODEL), 'wb') as fp:
    pkl.dump(vocab, fp)

# save extractor EMBEDDINGS
weights = []
for line in open(EXT_EMB_PATH).readlines():
    word, vec = line.split(' ', 1)
    weights.append([float(num) for num in vec.split()])
weights = torch.tensor(weights)
torch.save(weights, '{}/embeddings/ext-weights.pt'.format(MODEL))

# inspect dictionaries
#VOCAB = '3_models/fast_abs_rl_slo_model_weight_update_export_beams/pretrained_eng_model/agent_vocab.pkl'
#VOCAB = '1_data/pretrained/new/agent_vocab.pkl'
#
#with open(VOCAB, 'rb') as fp:
#    dic = pkl.load(fp)
#    d_view = [(v, k) for k, v in dic.items()]
#    d_view.sort()
