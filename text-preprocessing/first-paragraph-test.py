import stanfordnlp
import numpy as np


def get_summary_sentences(txt, mean):
    current = 0
    summary_sentences = []
    for sent in txt:
        if abs(mean - (current + len(sent))) < abs(mean - current):
            summary_sentences.append(sent)
            current += len(sent)
        else:
            break
    return summary_sentences

            
# load neural pipeline
nlp = stanfordnlp.Pipeline(lang='sl')

# load data
sta = open('preprocessed/sta-first-paragraph-add-text.txt', encoding='utf-8').readlines()

# tokenize
s = [nlp(paragraph) for paragraph in sta]

paragraph_tokenized = []
for p in s:
    sentence_tokenized = []
    for sent in p.sentences:
        tmp = [word.text for word in sent.words]
        sentence_tokenized.append(tmp)
    paragraph_tokenized.append(sentence_tokenized)

print(paragraph_tokenized)


n = []  # lengths of sentences
for article in paragraph_tokenized:
    txt = []
    for sent in article:
        s = " ".join([word for word in sent])
        s += '\n'
        txt.append(s)
        n.append(len(s))

    mean = 292  # provided by first paragraph statistics
    summary_sentences = get_summary_sentences(txt, mean)
    with open('output/test-added-text.txt', 'a') as file:
        all = " ".join([s.strip() for s in summary_sentences])
        file.write(all + '\n')

print(np.mean(n))
