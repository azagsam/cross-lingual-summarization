import json

import pandas as pd
import os


def create_dataframe(model, data_dir, dump_dir):
    df = pd.DataFrame()
    for i, file in enumerate(os.listdir(data_dir)):
        if i % 100 == 0:
            print(i)
        if 'log' in file:
            continue

        full_path = os.path.join(data_dir, file)

        # open a file and correct sentences
        with open(full_path) as f:
            article = json.load(f)

            for num in sorted(article):
                cands = article[num]['hypotheses']
                refs = article[num]['sentence']*len(cands)
                sum_logprob = article[num]['summarizer_logprob']
                #bert_score = article[num]['bert_score_f']
                rouge_score = article[num]['rouge_r3']

                df_tmp = pd.DataFrame(
                    {'file_id': [file]*len(cands),
                     'sentence_num': [num]*len(cands),
                     'refs': refs,
                     'cands': cands,
                     'sum_log_prob': sum_logprob,
                     #'bert_score': bert_score,
                     'rouge_r3': rouge_score,
                     }
                )

                df = pd.concat([df, df_tmp])
    path_to_save = os.path.join(dump_dir, 'df.csv')
    df.to_csv(path_to_save, index=False, encoding='utf-8')


if __name__ == '__main__':
    for model in os.listdir('models'):
        print(model)
        data_dir = os.path.join('post_processing', 'rouge_score', model)
        dump_dir = os.path.join('post_processing', 'data_frames', model)
        os.makedirs(dump_dir, exist_ok=True)
        print('Directories are created!')
        create_dataframe(model, data_dir, dump_dir)
