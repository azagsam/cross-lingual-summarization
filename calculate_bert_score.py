import os

from utils.bert_score.bert_score import score
import pandas as pd

def calculate_bert(data_file, dump_file):
    df = pd.read_csv(data_file, encoding='utf-8')
    cands = [line.strip() for line in df['cands'].astype(str)]
    refs = [line.strip() for line in df['refs'].astype(str)]
    # split list due to memory errors
    # memory error split list
    n = 128 * 2000 
    cands_chunks = [cands[i:i + n] for i in range(0, len(cands), n)]
    refs_chunks = [refs[i:i + n] for i in range(0, len(cands), n)]
    
    bert_P = []
    bert_R = []
    bert_F = []
    for cand, ref in zip(cands_chunks, refs_chunks):
        (P, R, F), hashname = score(cand, ref, verbose=True, batch_size=128, lang='sl', return_hash=True, idf=False)
        print(f'{hashname}: P={P.mean().item():.6f} R={R.mean().item():.6f} F={F.mean().item():.6f}')
        bert_P.extend(P)
        bert_R.extend(R)
        bert_F.extend(F)
    
    assert len(cands) == len(bert_P)

    df['bert_P'] = bert_P
    df['bert_R'] = bert_R
    df['bert_F'] = bert_F

    df.to_csv(dump_file, index=False, encoding='utf-8')

if __name__ == '__main__':
    for model in os.listdir('models'):
        print(model)
        data_file = os.path.join('post_processing', 'data_frames', model, 'df.csv')
        dump_file = os.path.join('post_processing', 'data_frames', model, 'df-bert.csv')

        print('Directories are created!')
        calculate_bert(data_file, dump_file)
