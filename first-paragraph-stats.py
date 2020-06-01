import statsmodels.stats.api as sms
import stanfordnlp
import logging

logging.basicConfig(filename='logs/first_paragraph_stats.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')

# load neural pipeline
nlp = stanfordnlp.Pipeline(lang='sl')

# load data
sta = open('data/sta-first-paragraph.txt', encoding='utf-8').readlines()

# tokenize
s = [nlp(paragraph) for paragraph in sta]

paragraph_tokenized = []
for p in s:
    sentence_tokenized = []
    for sent in p.sentences:
        tmp = [word.text for word in sent.words]
        sentence_tokenized.append(tmp)
    paragraph_tokenized.append(sentence_tokenized)

# print mean, sd, and confidence intervals for paragraphs
lengths = []
for p in paragraph_tokenized:
    count = 0
    for sent in p:
        count += len(" ".join([word for word in sent]))
    lengths.append(count)

prf = sms.DescrStatsW(lengths)

logging.info(f'Paragraph statistics: ')
logging.info(f'Max length: {max(lengths)}')
logging.info(f'Max length: {min(lengths)}')
logging.info(f'Mean: {prf.mean}')
logging.info(f'Std: {prf.std}')
low, high = prf.tconfint_mean()
logging.info(f'Confidence interval (low, high): {low}, {high}')

