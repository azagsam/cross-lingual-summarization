from tqdm import tqdm

for ind, line in enumerate(tqdm(open("output/language-model-characters.txt"))):
    mode = 'train'
    if ind % 20 == 0:
        mode = 'test'
    elif ind % 10 == 0:
        mode = 'valid'
    with open("output/split_characters/language-model-characters-{}.txt".format(mode), 'a') as f:
        f.write(line)
