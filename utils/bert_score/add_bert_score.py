import os
from bert_score import score
import json
import copy
import time

def add_bert_score(data_dir, dump_dir):
    start_time = time.time()
    for i, file in enumerate(os.listdir(data_dir)):
        if i % 10 == 0:
            print(i)
            print("--- %s seconds ---" % (time.time() - start_time))
            start_time = time.time()
        if 'log' in file:
            continue

        full_path = os.path.join(data_dir, file)

        # open a file and correct sentences
        with open(full_path) as f:
            article = json.load(f)
            file_copy = copy.deepcopy(article)

            for sentence, values in article.items():
                cands = values['hypotheses']
                refs = values['sentence']*len(cands)
                (P, R, F), hashname = score(cands, refs, verbose=True, lang='sl', idf=False, return_hash=True, batch_size=512)
                print(f'{hashname}: P={P.mean().item():.6f} R={R.mean().item():.6f} F={F.mean().item():.6f}')

                #s = [(float(value), key) for key, value in zip(cands, F)]
                #s.sort()
                #for val, sent in s:
                #    print(val, sent)

                file_copy[sentence]['bert_score_f'] = [float(value) for value in F]
                f.close()

            # save corrected text
            with open(os.path.join(dump_dir, file), 'w') as new_file:
                json.dump(file_copy, new_file, ensure_ascii=False)
            new_file.close()


if __name__ == '__main__':
    for model in os.listdir('models'):
        print(model)
        data_dir = os.path.join('post_processing', 'rouge_score', model)
        dump_dir = os.path.join('post_processing', 'bert_score', model)
        os.makedirs(dump_dir, exist_ok=True)
        print('Directories are created!')
        add_bert_score(data_dir, dump_dir)

# with open("hyps.txt") as f:
#     cands = [line.strip() for line in f]
#
# with open("refs.txt") as f:
#     refs = [line.strip() for line in f]
#
# (P, R, F), hashname = score(cands, refs, lang='sl', idf=False, return_hash=True)
# print(f'{hashname}: P={P.mean().item():.6f} R={R.mean().item():.6f} F={F.mean().item():.6f}')

# import matplotlib.pyplot as plt
# from bert_score import plot_example
#
# plot_example(cands[0], refs[0], lang="sl")
# plot_example(cands[1], refs[1], lang="sl")
# plot_example(cands[-1], refs[-1], lang="sl")
#
# plt.hist(F, bins=20)
# plt.show()
