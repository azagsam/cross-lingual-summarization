import pandas as pd
import os

df = pd.DataFrame()
dump_file = 'results.csv'
for model in os.listdir('models'):
    print(model)

    # open
    data_file = os.path.join('post_processing', 'data_frames', model, 'df-bert-cleaned-lm.csv')
    df_model = pd.read_csv(data_file, encoding='utf-8')

    # add model name
    df_model['model'] = [model]*len(df_model)

    # remove wrong rouge score
    df_model = df_model.drop(['rouge_r3'], axis=1)

    # join
    df = pd.concat([df, df_model])
    
df.to_csv(dump_file, index=False, encoding='utf-8')
