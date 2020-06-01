"""Get each STA report into a file with one sentence per line and tokenized sentences"""

import xml.etree.ElementTree as ET
import os
import pickle


def paragraph_id(tree, ns):
    # find all paragraph ids
    d = []
    for i in tree.iter(ns + 'p'):
        for key, value in i.items():
            if "." in value:
                paragraph = value.split('.')[1]
                d.append(paragraph)
    return d


def combine_paragraph_id(d):
    # combine paragraph ids to get full text id
    combined = []
    tmp = []
    for num in d:
        num = int(num)
        if not tmp:
            tmp.append(num)
        elif num - tmp[-1] == 1:
            tmp.append(num)
        else:
            combined.append(tmp)
            tmp = []
            tmp.append(num)
    combined.append(tmp)
    return combined


def extract_text(tree, ns):
    # extract text from paragraphs and save it into dict with "paragraph id: text" structure
    sets = dict()
    for i in tree.iter(ns + 'p'):
        if i.attrib:
            # get paragraph id
            v = [v for k, v in i.attrib.items()][0]
            # check if it is a valid paragraph
            if v.startswith('GF'):
                paragraph_text = []
                for s in i.iter():
                    # check if paragraph contains sentence
                    if s.tag == ns + 's':
                        # get sentence id and store values
                        # sentence_id = [v for k, v in s.attrib.items()][0]
                        sentence_text = []
                        for el in s.iter():
                            if el.tag == ns + 'w':
                                sentence_text.append(el.text)
                            elif el.tag == ns + 'pc':
                                sentence_text.append(el.text)
                        paragraph_text.append(sentence_text)
                sets[v] = paragraph_text
    return sets


def construct_texts(combined, sets, document):
    # construct full text and save it into a list
    full_texts = []
    for textnum in combined:
        full_text = ''
        for pnum in textnum:
            list_of_sentences = sets[document + '.' + str(pnum)]
            for sentence in list_of_sentences:
                full_sentence = " ".join(sentence)
                full_text += full_sentence + '\n'
        full_texts.append(full_text)
    return full_texts


def write_texts(full_texts, num):
    # write texts to disk (one text, one file)
    for b in full_texts:
        with open('sta-news-new/sta-{}.txt'.format(str(num)), 'w') as f:
            f.write(b)
        num += 1
    return num


# load sta files
with open('publishers.pkl', 'rb') as fp:
    sta_files = pickle.load(fp)['sta.si']

paths = [os.path.join('tei', file[:4], file) for file in sta_files]
ns = "{http://www.tei-c.org/ns/1.0}"

num = 0
file_num = 0
for path in paths:
    tree = ET.parse(path)
    document = path[9:18]
    d = paragraph_id(tree, ns)
    combined = combine_paragraph_id(d)
    sets = extract_text(tree, ns)
    full_texts = construct_texts(combined, sets, document)
    num = write_texts(full_texts, num)

    file_num += 1
    print(file_num)
