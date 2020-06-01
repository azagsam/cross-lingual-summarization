from tqdm import tqdm

for line in tqdm(open("output/language-model-tokenized.txt")):
    chars = [char if char is not " " else "_" for char in list(line.strip())[:-2]]  # remove punctuation and last /check again
    # print(" ".join(chars).lower())
    full_line = " ".join(chars).lower()
    with open("output/language-model-characters.txt", 'a') as f:
        f.write(full_line)
        f.write("\n")


from collections import Counter
c = Counter()
for line in tqdm(open("output/language-model-characters.txt")):
    c.update(list(line))

print(c.most_common(len(c)))

with open("/home/ales/Documents/magisterij/gigafida/output/split_characters/characters-list.txt", mode="a", encoding='utf-8') as f:
    for char, num in c.most_common(len(c))[1:]:
        line = char + "\t" + str(num)
        print(line)
        f.write(line)
        f.write("\n")


