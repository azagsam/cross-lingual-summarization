import xml.etree.ElementTree as ET
import os

ns = "{http://www.tei-c.org/ns/1.0}"
n = 0
for file in os.listdir('tei'):
    # traverse files
    if file.startswith('GF'):
        path = os.path.join('tei', file)

        # open file
        for doc in os.listdir(path):
            n += 1
            print(n)  # should be approx. 38k when finished
            full_file = os.path.join(path, doc)
            tree = ET.parse(full_file)

            # extract all sentences from a file
            for sent in tree.iter(ns + 's'):
                full_sent = []
                for words in sent.iter():
                    # full_sent += words.text
                    if words.tag == ns + 'w':
                        full_sent.append(words.text)
                    elif words.tag == ns + 'pc':
                        full_sent.append(words.text)

                # write sentence to disk
                with open("language-model-tokenized.txt", "a") as myfile:
                    myfile.write(" ".join(full_sent))
                    myfile.write('\n')