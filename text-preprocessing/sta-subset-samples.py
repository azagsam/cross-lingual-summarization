"""
Get appropriate samples for STA dataset
"""

import os

for n, sample in enumerate(os.listdir('sta-news-sep/src')):
    file_id = sample.split('-')[1]
    src = open('sta-news-sep/src/src-{}'.format(file_id)).read()
    tgt = open('sta-news-sep/tgt/tgt-{}'.format(file_id)).read()

    """skip very short or long reports AND summaries with less than 70 characters:
    e.g. "Pregled dogodkov, povezanih z evropskimi volitvami, do 15. ure.", 
    "Vreme in temperature po Evropi ob 20. uri.",
    "Pregled dogodkov v svetu v torek, 14. maja.", .... """

    if 1000 < len(src) < 3000 and len(tgt) > 70:
        with open("sta-subset/tgt/tgt-{}".format(file_id), "a") as myfile:
            myfile.write(tgt)
        with open("sta-subset/src/src-{}".format(file_id), "a") as myfile:
            myfile.write(src)

    if n % 1000 == 0:
        print(n)
