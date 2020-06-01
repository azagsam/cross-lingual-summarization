"""Get publishers for STA-news files"""

import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import pickle


def get_publishers(path):
    ns = "{http://www.tei-c.org/ns/1.0}"
    tree = ET.parse(path)
    pubs = []
    for publisher in tree.iter(ns + 'publisher'):
        pubs.append(publisher.text)
    return pubs[-1]


pubs = defaultdict(list)
doc_num = 0
for file in os.listdir('data/tei'):
    if file.startswith('GF'):
        path = os.path.join('tei', file)
        for doc in os.listdir(path):
            p = get_publishers(os.path.join(path, doc))  # path to each file
            doc_num += 1
            print(doc_num)
            pubs[p].append(doc)


with open('output/publishers.pkl', 'wb') as output:
    pickle.dump(pubs, output, pickle.HIGHEST_PROTOCOL)

with open('output/publishers.pkl', 'rb') as fp:
    dct = pickle.load(fp)
