"""
Json file for fast abs has to have 3 keys: id, abstract, article
Value is a list of sentences
"""

import json
import random
import string
import os
from collections import Counter


for file in os.listdir('sta-subset/src'):
    id = file[4:-4]
    full_path_src = os.path.join('sta-subset/src', 'src-{}.txt'.format(id))
    full_path_tgt = os.path.join('sta-subset/tgt', 'tgt-{}.txt'.format(id))

    with open(full_path_src) as src, open(full_path_tgt) as tgt:
        js_example = {}
        js_example['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)).lower()
        js_example['article'] = [sent.lower().strip() for sent in src.readlines()]
        js_example['abstract'] = [sent.lower().strip() for sent in tgt.readlines()]

        with open("sta-subset-json/{}.json".format(id), "w", encoding='utf-8') as out:
            json.dump(js_example, out, ensure_ascii=False)


