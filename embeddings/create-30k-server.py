"""
Creates 30-k slo embeddings file
"""
import numpy as np
import os

EMB_SRC_FILE = os.environ['EMB_SRC_FILE']
EMB_TGT_FILE = os.environ['EMB_TGT_FILE']
VOCAB_FILE = os.environ['VOCAB_FILE']
FILE_NAME = os.path.split(EMB_SRC_FILE)[1]
EMB_30K_SRC_FILE = os.path.join(os.path.split(EMB_SRC_FILE)[0], '30k.' + FILE_NAME)

# load dictionary of the most common words
word_list = {word.strip() for word in open(VOCAB_FILE).readlines()}

# write special tokens GO, EOS, ... from original file
with open(EMB_TGT_FILE, 'r') as en:
    en = en.readlines()[1:]
    with open(EMB_30K_SRC_FILE, 'a') as file:
        for i in range(4):
            file.write(en[i])

# extract most common words from ALIGNED embeddings
count = 0
for line in open(EMB_SRC_FILE).readlines():
    word, vec = line.split(" ", 1)
    if word in word_list:
        vec = np.array([float(num) for num in vec.split(" ")])
        vec = vec.round(7)
        line = word + " " + " ".join([str(num) for num in vec])
        with open(EMB_30K_SRC_FILE, 'a') as f:
            f.write(line)
            f.write("\n")
            count += 1
    if count == 30000:
        break

