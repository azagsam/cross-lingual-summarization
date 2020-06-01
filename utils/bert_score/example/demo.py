from bert_score import score

with open("hyps_long.txt") as f:
    cands = [line.strip() for line in f]

with open("refs_long.txt") as f:
    refs = [line.strip() for line in f]

(P, R, F), hashname = score(cands, refs, model_type='bert-base-multilingual-cased', verbose=True, batch_size=512, lang='en', return_hash=True)
print(f'{hashname}: P={P.mean().item():.6f} R={R.mean().item():.6f} F={F.mean().item():.6f}')
