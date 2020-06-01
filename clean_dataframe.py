import os
import pandas as pd


def clean_df(data_file, dump_file):
    df = pd.read_csv(data_file, encoding='utf-8')

    # sort df
    df = df.reset_index()
    df = df.sort_values(['file_id', 'index'])
    df = df.drop(['index'], axis=1)

    # transform bert results
    df['bert_P'] = df['bert_P'].apply(lambda x: float(x[7:-1]))
    df['bert_R'] = df['bert_R'].apply(lambda x: float(x[7:-1]))
    df['bert_F'] = df['bert_F'].apply(lambda x: float(x[7:-1]))

    df.to_csv(dump_file, index=False, encoding='utf-8')

if __name__ == '__main__':
    for model in os.listdir('models'):
        print(model)
        data_file = os.path.join('post_processing', 'data_frames', model, 'df-bert.csv')
        dump_file = os.path.join('post_processing', 'data_frames', model, 'df-bert-cleaned.csv')

        print('Cleaning model ...')
        clean_df(data_file, dump_file)
