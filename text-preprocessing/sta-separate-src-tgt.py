"""
Separate summaries and bodies for STA news articles
"""

import os
import re


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


for n, file in enumerate(os.listdir('sta-news')):
    sta = open(os.path.join('sta-news', file)).readlines()

    # remove date and time in the first sentence
    first_sentence = sta[0]
    try:
        clean_first_sentence = re.findall(r',.*?- (.*)', first_sentence)[0]
        sta[0] = clean_first_sentence + '\n'
    except IndexError:
        pass

    mean = 292  # provided by first paragraph statistics
    summary_sentences = get_summary_sentences(sta, mean)
    with open("sta-news-sep/tgt/tgt-{}.txt".format(str(n).zfill(6)), "a") as myfile:
        myfile.write("".join(summary_sentences))
    with open("sta-news-sep/src/src-{}.txt".format(str(n).zfill(6)), "a") as myfile:
        myfile.write("".join(sta[len(summary_sentences):]))

    print(n)

