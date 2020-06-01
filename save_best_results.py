import string

import pandas as pd
import argparse
import copy
import json
import os
from collections import Counter
from itertools import product


from cytoolz import curry
from tqdm.auto import tqdm


def make_n_grams(seq, n):
    """ return iterator """
    ngrams = (tuple(seq[i:i + n]) for i in range(len(seq) - n + 1))
    return ngrams


def _n_gram_match(summ, ref, n):
    summ_grams = Counter(make_n_grams(summ, n))
    ref_grams = Counter(make_n_grams(ref, n))
    grams = min(summ_grams, ref_grams, key=len)
    count = sum(min(summ_grams[g], ref_grams[g]) for g in grams)
    return count


@curry
def compute_rouge_n(output, reference, n=1, mode='f'):
    """ compute ROUGE-N for a single pair of summary and reference"""
    assert mode in list('fpr')  # F-1, precision, recall
    match = _n_gram_match(reference, output, n)
    if match == 0:
        score = 0.0
    else:
        precision = match / len(list(make_n_grams(output, n)))
        recall = match / len(list(make_n_grams(reference, n)))
        f_score = 2 * (precision * recall) / (precision + recall)
        if mode == 'p':
            score = precision
        elif mode == 'r':
            score = recall
        else:
            score = f_score
    return score


def _lcs_dp(a, b):
    """ compute the len dp of lcs"""
    dp = [[0 for _ in range(0, len(b) + 1)]
          for _ in range(0, len(a) + 1)]
    # dp[i][j]: lcs_len(a[:i], b[:j])
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def _lcs_len(a, b):
    """ compute the length of longest common subsequence between a and b"""
    dp = _lcs_dp(a, b)
    return dp[-1][-1]


@curry
def compute_rouge_l(output, reference, mode='f'):
    """ compute ROUGE-L for a single pair of summary and reference
    output, reference are list of words
    """
    assert mode in list('fpr')  # F-1, precision, recall
    lcs = _lcs_len(output, reference)
    if lcs == 0:
        score = 0.0
    else:
        precision = lcs / len(output)
        recall = lcs / len(reference)
        f_score = 2 * (precision * recall) / (precision + recall)
        if mode == 'p':
            score = precision
        if mode == 'r':
            score = recall
        else:
            score = f_score
    return score


def remove_all_punctuations(text):
    return [word for word in text if word not in string.punctuation]


def add_rouge_scores(df):
    """function in progress"""
    rouge_3_r = []
    rouge_l_f = []
    for can, ref in zip(tqdm(df['cands']), df['refs']):
        can = remove_all_punctuations(str(can).split())
        ref = remove_all_punctuations(str(ref).split())
        rouge_3_r.append(compute_rouge_n(can, ref, n=3, mode='r'))
        rouge_l_f.append(compute_rouge_l(can, ref, mode='f'))
    df['rouge_3_r'] = rouge_3_r
    df['rouge_l_f'] = rouge_l_f
    df.to_csv('results-rouge.csv', index=False, encoding='utf-8')


def parameter_permutation(parameters_dict):
    items = sorted(parameters_dict.items())
    keys, values = zip(*items)
    return [dict(zip(keys, v)) for v in product(*values)]


def get_final_score(df, first, second, first_num, second_num, opt='rouge_l_f'):
    """get best scores"""
    q = df \
        .sort_values(['file_id', 'model', 'sentence_num', first, second]) \
        .groupby(['file_id', 'model', 'sentence_num'], sort=False) \
        .tail(first_num) \
        .sort_values(['file_id', 'model', 'sentence_num', second]) \
        .groupby(['file_id', 'model', 'sentence_num'], sort=False) \
        .tail(second_num)

    # check if the extraction was correct
    df_val = df[(df['file_id'] == 0) & (df['sentence_num'] == 0) & (df['model'] == 'model_full')].sort_values(
        [first, second]).tail(first_num)[second].max()
    q_val = q[(q['file_id'] == 0) & (q['sentence_num'] == 0) & (q['model'] == 'model_full')][second].max()
    assert df_val == q_val

    return q[q['model'] != 'model_zero'][opt].mean()


def get_best_hypotheses(df, first, second, first_num, second_num):
    # get best scores
    q = df \
        .sort_values(['file_id', 'model', 'sentence_num', first, second]) \
        .groupby(['file_id', 'model', 'sentence_num'], sort=False) \
        .tail(first_num) \
        .sort_values(['file_id', 'model', 'sentence_num', second]) \
        .groupby(['file_id', 'model', 'sentence_num'], sort=False) \
        .tail(second_num)

    # check if the extraction was correct
    df_val = df[(df['file_id'] == 0) & (df['sentence_num'] == 0) & (df['model'] == 'model_full')].sort_values(
        [first, second]).tail(first_num)[second].max()
    q_val = q[(q['file_id'] == 0) & (q['sentence_num'] == 0) & (q['model'] == 'model_full')][second].max()
    assert df_val == q_val

    return q


def cross_validate_params(df, param):
    results = []  # max: 0.421
    for param in tqdm(param_permutations):
        score = get_final_score(df=df, **param)
        results.append((score, param))
    results.sort(key=lambda x: x[0], reverse=True)
    return results


def save_to_disk(q, params):
    p = "_".join([params['first'], str(params['first_num']), params['second'], str(params['second_num'])])
    for model in q['model'].unique():
        path = 'decoded/{}/{}'.format(p, model)
        os.makedirs(path, exist_ok=True)
        for num in range(5000):
            file = '{}.dec'.format(str(num))
            with open(os.path.join(path, file), 'w', encoding='utf-8') as f:
                subset = q[(q['model'] == model) & (q['file_id'] == num)]
                for can in subset['cands']:
                    f.write(str(can) + "\n")
                f.close()


# # test computations
# print(compute_rouge_n('the cat was found under the bed'.split(), 'the cat was under the bed'.split(), n=2, mode='r')) # should be recall 0.8, precision 0.67
# print(compute_rouge_l('the cat was found under the bed'.split(), 'the cat under was the bed'.split(), mode='r'))

# load and clean df
print('Results are loading ... ')
df = pd.read_csv("results-rouge.csv", encoding='utf-8')
df['file_id'] = df['file_id'].apply(lambda x: int(x[:-5]))
df['lm_loss'] = df['lm_loss'].apply(lambda x: -x)

# setup parameters and crossvalidate
parameters = {
        'first': ['bert_F', 'lm_loss', 'rouge_3_r', 'sum_log_prob', 'rouge_l_f'],
        'second': ['bert_F', 'lm_loss', 'rouge_3_r', 'sum_log_prob', 'rouge_l_f'],
        'first_num': [4, 12, 24],
        'second_num': [1]
    }

#parameters = {
#        'first': ['bert_P'],
#        'second': ['bert_P'],
#        'first_num': [4, 12],
#        'second_num': [1]
#    }

param_permutations = parameter_permutation(parameters)
print('Cross-validating results ... ')
results = cross_validate_params(df, param_permutations)
# print(results)  # 0.42150689598184515

for result, dic in tqdm(results):
    print("Retrieving best hypotheses ... ")
    print(dic)
    best_hypotheses = get_best_hypotheses(df=df, **dic)

    # save to disk
    print("Writing to disk ...")
    save_to_disk(best_hypotheses, dic)
