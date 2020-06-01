from tqdm import tqdm
import numpy as np

lst = []
for line in tqdm(open("output/split_characters/language-model-characters-train.txt")):
    lst.append(len(line))

np.median(lst)  # returns 214
np.mean(lst) # returns 242
np.percentile(lst, 95)  # returns 528


# stats for perplexity measure
lst = []
for line in tqdm(open("output/50k.txt")):
    line = line.strip()
    lst.append(len(line))

sum(lst) / len(lst)  # 7.960
