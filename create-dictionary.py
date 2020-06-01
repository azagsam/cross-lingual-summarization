from collections import Counter
import os
import json

corpora_counter = Counter()
for file in os.listdir('preprocessed/sta-subset-json'):
    full_path = os.path.join('preprocessed/sta-subset-json', file)
    tokens = []
    with open(full_path) as f:
        json_file = json.load(f)
        for sent in json_file['article']:
            tokens.extend(sent.split())
        for sent in json_file['abstract']:
            tokens.extend(sent.split())
    corpora_counter.update(Counter(tokens))

words = 0
for token, _ in corpora_counter.most_common(len(corpora_counter)):
    if any(char.isdigit() for char in token):  # exclude numbers
        continue
    else:
        with open('output/50k.txt', 'a') as f:
            f.write(token)
            f.write('\n')
        words += 1
        if words == 50000:
            break